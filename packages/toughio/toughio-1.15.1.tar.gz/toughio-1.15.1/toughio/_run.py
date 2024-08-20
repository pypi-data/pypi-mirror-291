import glob
import os
import pathlib
import platform
import secrets
import shutil
import signal
import subprocess
import tempfile

import psutil

_check_exec = True  # Bool to be monkeypatched in tests


def run(
    exec,
    input_filename,
    other_filenames=None,
    command=None,
    workers=None,
    docker=None,
    wsl=False,
    working_dir=None,
    use_temp=False,
    ignore_patterns=None,
    silent=False,
    petsc_args=None,
    docker_args=None,
    container_name=None,
    **kwargs,
):
    """
    Run TOUGH executable.

    Parameters
    ----------
    exec : str or pathlike
        Path to TOUGH executable.
    input_filename : str or pathlike
        TOUGH input file name.
    other_filenames : list, dict or None, optional, default None
        Other simulation files to copy to working directory (e.g., MESH, INCON, GENER) if not already present. If ``other_filenames`` is a dict, must be in the form ``{old: new}``, where ``old`` is the current name of the file to copy, and ``new`` is the name of the file copied.
    command : callable or None, optional, default None
        Command to execute TOUGH. Must be in the form ``f(exec, inp, [out])``, where ``exec`` is the path to TOUGH executable, ``inp`` is the input file name, and ``out`` is the output file name (optional).
    workers : int or None, optional, default None
        Number of MPI workers to invoke.
    docker : str, optional, default None
        Name of Docker image.
    wsl : bool, optional, default False
        Only for Windows. If `True`, run the final command as a Bash command.
    working_dir : str, pathlike or None, optional, default None
        Working directory. Input and output files will be generated in this directory.
    use_temp : bool, optional, default False
        If `True`, run simulation in a temporary directory, and copy simulation files to `working_dir` at the end of the simulation. This option may be required when running TOUGH through a Docker.
    ignore_patterns : list or None, optional, default None
        If provided, output files that match the glob-style patterns will be discarded.
    silent : bool, optional, default False
        If `True`, nothing will be printed to standard output.
    petsc_args : list or None, optional, default None
        List of arguments passed to PETSc solver (written to `.petscrc`).
    docker_args : list or None, optional, default None
        List of arguments passed to `docker run` command.
    container_name : str or None, optional, default None
        Name of Docker container.

    Other Parameters
    ----------------
    block : str {'all', 'gener', 'mesh', 'incon'} or None, optional, default None
        Only if ``file_format = "tough"``. Blocks to be written:

         - 'all': write all blocks,
         - 'gener': only write block GENER,
         - 'mesh': only write blocks ELEME, COORD and CONNE,
         - 'incon': only write block INCON,
         - None: write all blocks except blocks defined in `ignore_blocks`.

    ignore_blocks : list of str or None, optional, default None
        Only if ``file_format = "tough"`` and `block` is None. Blocks to ignore.
    space_between_blocks : bool, optional, default False
        Only if ``file_format = "tough"``. Add an empty record between blocks.
    space_between_blocks : bool, optional, default True
        Only if ``file_format = "tough"``. Add a white space between floating point values.
    eos : str or None, optional, default None
        Only if ``file_format = "tough"``. Equation of State.
        If `eos` is defined in `parameters`, this option will be ignored.
    mopr_10 : int, optional, default 0
        Only if ``file_format = "toughreact-solute"``. MOPR(10) value in file 'flow.inp'.
    mopr_11 : int, optional, default 0
        Only if ``file_format = "toughreact-solute"``. MOPR(11) value in file 'flow.inp'.
    verbose : bool, optional, default True
        Only if ``file_format`` in {"toughreact-solute", "toughreact-chemical"}. If `True`, add comments to describe content of file.

    Returns
    -------
    :class:`subprocess.CompletedProcess`
        Subprocess completion status.

    """
    from . import write_input

    other_filenames = (
        {k: k for k in other_filenames}
        if isinstance(other_filenames, (list, tuple))
        else other_filenames if other_filenames else {}
    )

    if command is None:
        command = lambda exec, inp, out: f"{exec} {inp} {out}"

    ignore_patterns = list(ignore_patterns) if ignore_patterns else []
    ignore_patterns += [".OUTPUT*", "TABLE", "MESHA", "MESHB"]

    # Executable
    exec = str(exec)
    exec = f"{os.path.expanduser('~')}/{exec[2:]}" if exec.startswith("~/") else exec

    if _check_exec:
        if not docker:
            if shutil.which(exec) is None:
                raise RuntimeError(f"executable '{exec}' not found.")

        else:
            # Check if Docker is in the PATH
            if shutil.which("docker") is None:
                raise RuntimeError("Docker executable not found.")

            # Check if Docker daemon is running
            status = subprocess.run(
                ["docker", "version"],
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )

            if "Server" not in status.stdout:
                raise RuntimeError(
                    "cannot connect to the Docker daemon. Is the Docker daemon running?"
                )

            # Check if Docker image exists
            status = subprocess.run(
                ["docker", "images", "-q", docker],
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )

            if not status.stdout:
                raise RuntimeError(f"image '{docker}' not found.")

            # Check if the executable exists inside the image
            status = subprocess.run(
                ["docker", "run", "--rm", docker, "which", exec],
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )

            if not status.stdout:
                raise RuntimeError(
                    f"executable '{exec}' not found in Docker image '{docker}'."
                )

    # Working directory
    working_dir = os.getcwd() if working_dir is None else working_dir
    working_dir = pathlib.Path(working_dir)
    working_dir.mkdir(parents=True, exist_ok=True)

    # Simulation directory
    if use_temp:
        temp_dir = tempfile.mkdtemp()
        simulation_dir = pathlib.Path(temp_dir)

        with open(working_dir / "tempdir.txt", "w") as f:
            f.write(temp_dir)

    else:
        simulation_dir = working_dir

    # Check if input file is in simulation directory, otherwise copy
    if not isinstance(input_filename, dict):
        input_path = pathlib.Path(input_filename)
        input_filename = simulation_dir / input_path.name

        if input_path.parent.resolve() != simulation_dir.resolve():
            shutil.copy(input_path, input_filename)

    else:
        write_input(simulation_dir / "INFILE", input_filename, **kwargs)
        input_filename = simulation_dir / "INFILE"

    # Copy other simulation files to working directory
    for k, v in other_filenames.items():
        filename = pathlib.Path(k)
        new_filename = pathlib.Path(v)

        if (
            filename.parent.resolve() != simulation_dir.resolve()
            or filename.name != new_filename.name
        ):
            shutil.copy(filename, simulation_dir / new_filename.name)

    # PETSc arguments
    petsc_args = petsc_args if petsc_args else []

    if petsc_args:
        with open(simulation_dir / ".petscrc", "w") as f:
            for arg in petsc_args:
                if arg.startswith("-"):
                    f.write(f"{arg} ")

                else:
                    f.write(f"{arg}\n")

    # Output filename
    output_filename = f"{input_filename.stem}.out"

    # TOUGH command
    cmd = command(exec, str(input_filename.name), str(output_filename))

    # Use MPI
    if workers is not None and workers > 1:
        cmd = f"mpiexec -n {workers} {cmd}"

    # Use Docker
    is_windows = platform.system().startswith("Win")

    if docker:
        container_name = (
            container_name if container_name else f"toughio_{secrets.token_hex(4)}"
        )

        if is_windows and os.getenv("ComSpec").endswith("cmd.exe"):
            cwd = '"%cd%"'

        else:
            cwd = "${PWD}"

        docker_args = docker_args if docker_args else []
        docker_args += [
            "--name",
            container_name,
            "--rm",
            # Sometime raises a duplicate mount point error, use old-school volume instead (but shell must be True in this case)
            # "--mount",
            # f"type=bind,source={simulation_dir},target=/shared",
            "--volume",
            f"{cwd}:/shared",
            "--workdir",
            "/shared",
        ]
        cmd = f"docker run {' '.join(str(arg) for arg in docker_args)} {docker} {cmd}"

    # Use WSL
    if wsl and is_windows:
        cmd = f"bash -c '{cmd}'"

    # Run simulation
    try:
        # See <https://www.koldfront.dk/making_subprocesspopen_in_python_3_play_nice_with_elaborate_output_1594>
        p = subprocess.Popen(
            cmd,
            shell=True,  # shell must be True as the command may contain quotes
            cwd=str(simulation_dir),
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            universal_newlines=False,
        )

        stdout = []
        cr = False
        for line in open(os.dup(p.stdout.fileno()), newline=""):
            # Handle carriage return
            # newline in open is converting \r\n as \r moving \r at the end of the previous string
            # This is only an issue for Spyder
            line = f"\r{line}" if cr else line
            cr = line.endswith("\r")
            line = line[:-2] if cr else line

            if not silent:
                print(line, end="", flush=True)
                stdout.append(line)

    except (KeyboardInterrupt, Exception) as e:
        # Stop Docker container
        if docker:
            status = subprocess.run(
                ["docker", "stop", container_name],
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )

        # Handle children process termination
        # See <https://stackoverflow.com/a/25134985/9729313>
        try:
            proc = psutil.Process(p.pid)
            for child_process in proc.children():
                child_process.send_signal(signal.SIGTERM)

            proc.send_signal(signal.SIGTERM)

        except psutil.NoSuchProcess:
            pass

        raise e

    p.wait()
    status = subprocess.CompletedProcess(
        args=p.args,
        returncode=p.returncode,
        stdout="".join(stdout),
    )

    # Copy files from temporary directory and delete it
    if use_temp:
        shutil.copytree(
            simulation_dir,
            working_dir,
            ignore=shutil.ignore_patterns(*ignore_patterns),
            dirs_exist_ok=True,  # Doesn't work with Python 3.7
        )
        shutil.rmtree(simulation_dir, ignore_errors=True)
        os.remove(working_dir / "tempdir.txt")

    # Clean up working directory
    patterns = [
        pathlib.Path(filename)
        for pattern in ignore_patterns
        for filename in glob.glob(f"{str(simulation_dir)}/{pattern}")
    ]

    for pattern in patterns:
        os.remove(pattern)

    return status
