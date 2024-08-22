"""Define the CLI function for the semi-automatic workflow manager."""

import logging
import math
import pathlib
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal

import click

from autojob import SETTINGS
from autojob.advance.advance import advance
from autojob.utils.cli import MemoryFloat
from autojob.utils.cli import mods_to_dict

if TYPE_CHECKING:
    from autojob.task import Task

logger = logging.getLogger(__name__)

STOP_FILE = "autojob.stop"


@click.command(
    "advance",
    epilog="""
Warning:

    All calculator parameters must be passed as keyword arguments to
    the ASE calculator. For example, this is acceptable:

    .. code:: python

        Vasp(label="vasp", directory=".")

But this is unacceptable::

    Vasp(atoms)

Example::

    1. Submit the new job upon creation.

        autojob advance
""",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "-n",
    "--next-step",
    default=None,
    type=click.Choice(["relaxation", "vibrational analysis"]),
    help="The next calculation to prep if this calculation is complete.",
)
@click.option(
    "-A",
    "--archive-mode",
    default="json",
    type=click.Choice(["json", "None"]),
    help="How to archive the completed task.",
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
    "--log-file",
    default=SETTINGS.LOG_FILE,
    help="The file name in which to log messages from autojob.",
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
    "-a",
    "--auto-restart/--no-auto-restart",
    default=True,
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
    help='Modify SLURM parameters (e.g., --slurm-mod="job-name=COOH-%'
    '{calculation-id}"). Recognized placeholders: ${structure}, '
    "%{study-group-id}, ${study-id}, ${calculation-id}, and ${job-id}. Value "
    "should be passed exactly as they should appear in a slurm submission "
    'file (e.g., --slurm-mod="partition=razi,cpu2022"). This option can be '
    "repeated; however, the use of placeholders is currently only supported "
    "for the job-name option.",
    show_default=True,
)
@click.option(
    "--to-copy",
    default=(),
    help="Indicate a file to copy from the directory of the completed job to "
    "the directory of the new job. This option can be repeated.",
    multiple=True,
    show_default=True,
    type=click.Path(path_type=pathlib.Path),
)
@click.option(
    "-p",
    "--path",
    "paths",
    default=(pathlib.Path.cwd(),),
    help="The path from which to create new job directories. This option can "
    "be repeated. Defaults to the current working directory.",
    multiple=True,
    type=click.Path(file_okay=False, exists=True, path_type=pathlib.Path),
)
def main(
    *,
    next_step: Literal["relaxation", "vibrational analysis"],  # noqa: ARG001
    archive_mode: Literal["json", None],
    submit: bool,
    file_size_limit: float,
    bader: bool,  # noqa: ARG001
    auto_restart: bool,  # noqa: ARG001
    calc_mods: dict[str, Any],  # noqa: ARG001
    slurm_mods: dict[str, Any],  # noqa: ARG001
    to_copy: tuple[str, ...],  # noqa: ARG001
    paths: tuple[pathlib.Path, ...],
):
    """Advance to the next in a series of calculations."""
    tasks_and_dirs: list[tuple[Task, pathlib.Path]] = []

    for path in paths:
        tasks_and_dirs.extend(
            advance(
                dir_name=path,
                file_size_limit=file_size_limit,
                submit=submit,
                archive_mode=archive_mode,
            )
        )

    num_new_tasks = len(tasks_and_dirs)
    if tasks_and_dirs:
        suffix = "" if num_new_tasks == 1 else "s"
        logger.info(f"{num_new_tasks} new task{suffix} created.")
    else:
        logger.info("No new tasks created. Workflow branch complete.")
