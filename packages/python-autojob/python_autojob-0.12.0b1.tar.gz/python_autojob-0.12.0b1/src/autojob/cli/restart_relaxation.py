"""This module defines the command-line interface for restarting DFT jobs."""

import logging
import math
import pathlib
from typing import Any

import click

from autojob.cli.advance import STOP_FILE
from autojob.next.relaxation import restart_relaxation
from autojob.utils.cli import MemoryFloat
from autojob.utils.cli import configure_settings
from autojob.utils.cli import mods_to_dict
from autojob.utils.files import find_finished_jobs

logger = logging.getLogger(__name__)


@click.command(
    "restart-relaxation",
    epilog="""
Warning: All calculator parameters must be passed as positional arguments to
the ASE calculator. For example, this is acceptable:

    Vasp(label="vasp", directory=".")

But this is unacceptable:

    Vasp(atoms)

-------------------------------
EXAMPLES
-------------------------------

1. Submit the new job upon creation.

restart-relaxation -S

2. Copy the WAVECAR & CHGCAR, submit the new job upon creation, print
out all messages.

\b
restart-relaxation --carry-over WAVECAR --carry-over CHGCAR -S -vv

3. Submit the new job upon creation, enable auto-restart, run bader charge
upon completion, print out all messages, delete all files 1 gigabyte or
larger, reconfigure the calculator with ediff=1e-8.

\b
restart-relaxation -Sabvv --file-size-limit 1GB -C "ediff=1e-8"

4. Submit the new job upon creation, set the job name to the name of the
structure file with the suffix "-vib".

\b
restart-relaxation -S --slurm-mod="job-name={structure}-vib"
""",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    default=0,
    count=True,
    help="Controls the verbosity. 0: Show messages of level warning and "
    "higher. 1: Show messages of level info and higher. 2: Show all messages"
    "-useful for debugging.",
    show_default=True,
)
@click.option(
    "-S",
    "--submit/--no-submit",
    default=False,
    help="Whether or not to submit the newly created job.",
    show_default=True,
)
@click.option(
    "--file-size-limit",
    default=math.inf,
    help="Specify the file size above which all files in the old job larger "
    "than this will be deleted. Integers will be interpreted in bytes. The "
    "suffixes, KB, MB, and GB, will cause the value to be interpreted as "
    "kilobytes, megabytes, and gigabytes, respectively.",
    show_default=True,
    type=MemoryFloat(),
)
@click.option(
    "-b",
    "--bader/--no-bader",
    default=False,
    help="Whether or not to run bader charge analysis after relaxation is "
    "converged. Note that if the first import statement imports os or "
    "subprocees, no new logic will be added.",
    show_default=True,
)
@click.option(
    "-C",
    "--chargemol/--no-chargemol",
    default=False,
    help="Whether or not to run chargemol after relaxation is "
    "converged. Note that if the first import statement imports os or "
    "subprocees, no new logic will be added.",
    show_default=True,
)
@click.option(
    "-a",
    "--auto-restart/--no-auto-restart",
    default=False,
    help="Whether or not to add logic to vasp.sh to automatically resubmit "
    "a job on time out.",
    show_default=True,
)
@click.option(
    "-c",
    "--calc-mod",
    "calc_mods",
    default={},
    multiple=True,
    callback=mods_to_dict,
    help='Modify calculator parameters (e.g., --calc-mod="encut=500"). '
    "Values will be parsed into "
    "their native types, so string values should be passed without "
    'additional quotations (e.g., --calc-mod="algo=Fast"). This option can '
    "be repeated.",
    show_default=True,
)
@click.option(
    "-L",
    "--slurm-mod",
    "slurm_mods",
    default={},
    multiple=True,
    callback=mods_to_dict,
    help='Modify SLURM parameters (e.g., --slurm-mod="job-name=COOH-'
    '{calculation_id}"). Recognized placeholders: {structure}, '
    "{study_group_id}, {study_id}, {calculation_id}, and {job_id}. Value "
    "should be passed exactly as they should appear in a slurm submission "
    'file (e.g., --slurm-mod="partition=razi,cpu2022"). This option can be '
    "repeated; however, the use of placeholders is currently only supported "
    "for the job-name option. Note that only one of `mem` and `mem_per_cpu` "
    "can be set.",
    show_default=True,
)
@click.option(
    "--config",
    default={},
    multiple=True,
    callback=mods_to_dict,
    help="Configure autojob parameters (e.g., "
    '--config="slurm_script=gaussian.sh).  This option can be repeated.',
    show_default=True,
)
@click.option(
    "--carry-over",
    "files_to_carry_over",
    default=(),
    help="Indicate a file to copy from the directory of the completed job to "
    "the directory of the new job. This option can be repeated.",
    multiple=True,
    show_default=True,
)
@click.option(
    "-p",
    "--path",
    "paths",
    default=(pathlib.Path.cwd(),),
    help="The path from which to create new job directories. This option can "
    "be repeated. Defaults to the current working directory.",
    multiple=True,
    type=click.Path(path_type=pathlib.Path),
)
# TODO: change to -R
@click.option(
    "-r",
    "--recursive",
    default=False,
    help="Whether to search all subdirectories for jobs to restart in "
    "addition to those specified by the --path option.",
    show_default=True,
)
def main(
    *,
    paths: tuple[pathlib.Path, ...],
    verbosity: int,
    submit: bool,
    file_size_limit: float,
    bader: bool,
    chargemol: bool,
    auto_restart: bool,
    recursive: bool,
    calc_mods: dict[str, Any],
    slurm_mods: dict[str, Any],
    files_to_carry_over: tuple[str, ...],
    config: dict[str, Any],
) -> None:
    """Restart a DFT relaxation calculation."""
    match verbosity:
        case 0:
            level = logging.WARNING
        case 1:
            level = logging.INFO
        case _:
            level = logging.DEBUG

    logging.basicConfig(level=level)

    configure_settings(config)

    if recursive:
        sub_dir_paths: set[pathlib.Path] = set()

        for path in paths:
            sub_dir_paths.union(find_finished_jobs(path=path))

        paths = tuple(sub_dir_paths)

    # TODO: Add whitelist/blacklist filtering

    for old_job in paths:
        if pathlib.Path(old_job).joinpath(STOP_FILE).exists():
            click.echo(f"Stop file found. Aborting restart ({old_job})")
        else:
            new_job = restart_relaxation(
                submit=submit,
                file_size_limit=file_size_limit,
                old_job=old_job,
                bader=bader,
                chargemol=chargemol,
                auto_restart=auto_restart,
                calc_mods=calc_mods,
                slurm_mods=slurm_mods,
                files_to_carry_over=files_to_carry_over or None,
            )
            click.echo(f"New job created {'/'.join(new_job.parts[-4:])}")
