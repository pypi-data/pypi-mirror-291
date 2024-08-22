"""Utilities for handling files and directories."""

import contextlib
import logging
import pathlib
import re
import socket
import subprocess
from typing import TextIO

from autojob.coordinator import job

logger = logging.getLogger(__name__)

JOB_STATS_FILE = "job_stats.txt"


def get_uri(dir_name: str | pathlib.Path) -> str:
    """Return the URI path for a directory.

    This allows files hosted on different file servers to have distinct
    locations.

    Adapted from Atomate2.

    Arg:
        dir_name: A directory name.

    Returns:
    -------
    str
        Full URI path, e.g., "fileserver.host.com:/full/path/of/dir_name".
    """
    fullpath = pathlib.Path(dir_name).absolute()
    hostname = socket.gethostname()
    with contextlib.suppress(socket.gaierror, socket.herror):
        hostname = socket.gethostbyaddr(hostname)[0]
    return f"{hostname}:{fullpath}"


def extract_structure_name(python_script: TextIO) -> str:
    """Determine the structure filename from a Python script file.

    The structure must appear in a call to ase.io.read as either:
        1) ase.io.read(structure_name)
        2) io.read(structure_name)
        3) read(structure_name)

    The structure present in the first such occurrence will be returned.

    Args:
        python_script: A stream containing the contents of the Python script
            used to run the calculation.

    Raises:
        RuntimeError: No structure name found.

    Returns:
        A string representing the filename of the structure read in the
        Python script.
    """
    logger.debug(f"Extracting structure filename from {python_script.name}")
    structure_re = re.compile(
        r'^atoms = (?:ase.)?(?:io.)?read\(["\'](?P<structure_name>.+)["\']\)$'
    )
    for line in python_script:
        match = structure_re.search(line)
        if match:
            structure_name = match.group("structure_name")
            logger.debug(
                "Successfully extracted structure filename from "
                f"{python_script.name}: {structure_name}"
            )
            return structure_name

    msg = f"Unable to determine structure name from {python_script.name}"
    raise RuntimeError(msg)


def find_slurm_file(dir_name: pathlib.Path) -> pathlib.Path:
    """Retrieves the path to the first slurm output file found.

    Args:
        dir_name: The directory in which to search.

    Returns:
        The path to the slurm output file. If multiple slurm output files
        exist, the one corresponding to the job with the highest slurm job ID
        will be returned.

    Raises:
        FileNotFoundError: No valid slurm file found.
    """
    try:
        slurm_files = sorted(dir_name.rglob("slurm-*.out"))
        return slurm_files[-1]
    except IndexError as err:
        msg = "No valid slurm file found."
        raise FileNotFoundError(msg) from err


def get_slurm_job_id(job_dir: pathlib.Path) -> int:
    """Returns the SLURM job id for the job run in the directory "job_dir".

    Args:
        job_dir: The directory containing the slurm output file.

    Raises:
        FileNotFoundError: SLURM output file not found.

    Returns:
        The SLURM job id.
    """
    slurm_re = re.compile(r"slurm-(\d+).out")
    for path in job_dir.iterdir():
        match = slurm_re.fullmatch(path.name)
        if match:
            return int(match[1])

    msg = f"No slurm output file found in {'/'.join(job_dir.parts[-4:])}"
    raise FileNotFoundError(msg)


def create_job_stats_file(
    slurm_job_id: int, job_dir: str | pathlib.Path
) -> pathlib.Path:
    """Creates file containing statistics from completed Slurm job.

    Args:
        slurm_job_id: The Slurm job ID for the job.
        job_dir: The job directory.

    Raises:
        RuntimeError: Unable to create job stats file.

    Returns:
        A pathlib.Path to the file containing the job statistics.
    """
    logger.debug(f"Creating job stats file for Slurm job: {slurm_job_id}")
    job_stats_file = pathlib.Path(job_dir).joinpath(JOB_STATS_FILE)

    slurm_cmd = [
        "/usr/bin/env",
        "sacct",
        f"--jobs={slurm_job_id}",
        f'--format={"%20,".join(job.JOB_STATS_FIELDS)}',
    ]

    try:
        process = subprocess.run(  # noqa: S603
            slurm_cmd,
            text=True,
            check=True,
            capture_output=True,
        )
        if process.stdout:
            with job_stats_file.open(mode="x", encoding="utf-8") as file:
                file.write(process.stdout)

    except subprocess.CalledProcessError as err:
        msg = f"Unable to create job stats file for job in {job_dir}"
        raise RuntimeError(msg) from err

    logger.debug(
        f"Successfully created job stats file for Slurm job: {slurm_job_id}"
    )
    return job_stats_file


def find_study_group_dirs(
    path: pathlib.Path | None = None,
) -> list[pathlib.Path]:
    """Find all study group directories in the directory tree below "path".

    Note that if a path matches the specified pattern, its subdirectories are
    not searched.

    Args:
        path: Top level directory to be searched. Defaults to
        current working directory.

    Returns:
        List[pathlib.Path]: All study group directories below "path".
    """
    return _find_template_dir(re.compile(r"g[a-zA-Z0-9]{9}"), path)


def find_study_dirs(path: pathlib.Path | None = None) -> list[pathlib.Path]:
    """Find all study directories in the directory tree below "path".

    Note that if a path matches the specified pattern, its subdirectories are
    not searched.

    Args:
        path: Top level directory to be searched. Defaults to current working
            directory.

    Returns:
        A list of Paths to all study directories below path.
    """
    return _find_template_dir(re.compile(r"s[a-zA-Z0-9]{9}"), path)


def find_calculation_dirs(
    path: pathlib.Path | None = None,
) -> list[pathlib.Path]:
    """Find all calculation directories in the directory tree below "path".

    Note that if a path matches the specified pattern, its subdirectories are
    not searched.

    Args:
        path: Top level directory to be searched. Defaults to current working
            directory.

    Returns:
        A list of Paths to all calculation directories below path.
    """
    return _find_template_dir(re.compile(r"c[a-zA-Z0-9]{9}"), path)


def find_job_dirs(path: pathlib.Path | None = None) -> list[pathlib.Path]:
    """Find all job directories in the directory tree below "path".

    Note that if a path matches the specified pattern, its subdirectories are
    not searched.

    Args:
        path: Top level directory to be searched. Defaults to current working
            directory.

    Returns:
        A list of all job directories below path.
    """
    return _find_template_dir(re.compile(r"j[a-zA-Z0-9]{9}"), path)


def find_last_submitted_jobs(
    path: pathlib.Path | None = None,
    ignore_unrun_jobs: bool = False,
) -> list[pathlib.Path]:
    """Returns the directories of the most recently submitted jobs.

    Only the directories in each calculation specified in "path" or
    subdirectories of "path" are returned.

    Args:
        path: The directory specifying or containing calculations. Defaults
            to current working directory.
        ignore_unrun_jobs: If true, no job will be reported for calculation
            directories containing jobs that have yet been run. Otherwise, the
            most recently submitted job will be reported. Defaults to False.

    Returns:
        A list of Paths to directories containing newest jobs for each
        calculation in path or subdirectories of path.
    """
    calc_dirs = find_calculation_dirs(path)

    newest_jobs: list[pathlib.Path] = []

    for calc_dir in calc_dirs:
        newest_job_dir = None
        newest_job_id = None

        for job_dir in calc_dir.iterdir():
            if not job_dir.is_dir():
                continue
            try:
                job_id = get_slurm_job_id(job_dir)
            except FileNotFoundError:
                if ignore_unrun_jobs:
                    break

                continue

            if newest_job_id is None or job_id > newest_job_id:
                newest_job_id = job_id
                newest_job_dir = job_dir

        if newest_job_dir is not None:
            newest_jobs.append(newest_job_dir)

    return newest_jobs


def check_job_status(
    job_id: int,
) -> str:
    """Determine the status of a SLURM job.

    Args:
        job_id: The Slurm job ID.

    Returns:
        A string indicating the job status.
    """
    output = subprocess.check_output(  # noqa: S603
        ["/usr/bin/env", "seff", str(job_id)],
        encoding="utf-8",
    )
    status_re = re.compile(r"^State: (?P<status>\w+) \(exit code \d*\)$")
    for line in output.splitlines():
        if match := status_re.match(line):
            return match.group("status")

    msg = (
        f"Unable to determine the status of job: {job_id}. Please verify "
        "that this is a valid SLURM job ID"
    )
    raise ValueError(msg)


def find_finished_jobs(path: pathlib.Path | None = None) -> list[pathlib.Path]:
    """Find the directories and subdirectories containing finished jobs.

    These jobs may have terminated due to errors, but they are no longer
    running.

    Args:
        path: The directory in which to search. Defaults to None (in which
            case the current working directory is searched).

    Returns:
        A list of Paths pointing to directories containing jobs that have
        finished.
    """
    last_submitted = find_last_submitted_jobs(
        path=path, ignore_unrun_jobs=True
    )
    finished_jobs = []

    for job_dir in last_submitted:
        job_id = get_slurm_job_id(job_dir=job_dir)
        status = check_job_status(job_id=job_id)
        if status.lower() != "idle":
            finished_jobs.append(job_dir)

    return finished_jobs


def _find_template_dir(
    pattern: re.Pattern, path: pathlib.Path | None = None
) -> list[pathlib.Path]:
    """Returns list of directories.

    Note that if the supplied path matches the specified pattern, its
    subdirectories are not searched.

    Args:
        path: The starting directory for the search.
        pattern: A regular expression to match with directory names.

    Returns:
        The list of directories matching pattern.
    """
    if path is None:
        path = pathlib.Path.cwd()

    if pattern.fullmatch(path.name):
        return [path]

    dirs: list[pathlib.Path] = []
    for sub_path in path.iterdir():
        if not sub_path.is_dir():
            continue
        if pattern.fullmatch(sub_path.name):
            dirs.append(sub_path)
        else:
            dirs.extend(_find_template_dir(pattern, sub_path))

    return dirs
