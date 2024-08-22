"""Create a vibrational calculation from the command-line."""

import logging
import math
import pathlib
from typing import Any

import click

from autojob.cli.restart_relaxation import mods_to_dict
from autojob.next.vibration import create_vibration
from autojob.utils.cli import MemoryFloat
from autojob.utils.files import find_finished_jobs

logger = logging.getLogger(__name__)


@click.command(
    "run-vibration",
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

run-vibration -S

2. Copy the WAVECAR & CHGCAR, submit the new job upon creation, print
out all messages, unfreeze all atoms tagged with -99.

\b
run-vibration --carry-over WAVECAR --carry-over CHGCAR -S -vv --unfreeze -99

3. Submit the new job upon creation, print out all messages, unfreeze
all atoms tagged with -99, delete all files 1 gigabyte or larger,
reconfigure the calculator with ediff=1e-8.

\b
run-vibration -Svv ---unfreeze-tag -99 --file-size-limit 1GB -C "ediff=1e-8"

4. Submit the new job upon creation, unfreeze all atoms tagged with
-99, set the job name to the name of the structure file with the
suffix "-vib".

\b
run-vibration -S --unfreeze-tag -99 --slurm-mod="job-name={structure}-vib"
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
    "-I",
    "--infrared/--no-infrared",
    default=False,
    help="Whether or not to calculate infrared intensities.",
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
    "--carry-over",
    "files_to_carry_over",
    default=(),
    help="Indicate a file to copy from the directory of the completed job to "
    "the directory of the new job. This option can be repeated.",
    multiple=True,
    show_default=True,
)
@click.option(
    "--unfreeze-tag",
    "tags_to_unfreeze",
    default=(-99,),
    multiple=True,
    help="Unfreeze all atoms with this tag. This option can be repeated. Note "
    "that this will apply to all vibrational calculations started.",
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
    infrared: bool,
    file_size_limit: float,
    recursive: bool,
    calc_mods: dict[str, Any],
    slurm_mods: dict[str, Any],
    files_to_carry_over: tuple[str, ...],
    tags_to_unfreeze: tuple[int, ...],
) -> None:
    """Create a new vibrational calculation from an existing calculation.

    Aside from setting NSW=0 (in the case of a VASP calculation), no changes
    will be made to the original calculator configuration.
    """
    match verbosity:
        case 0:
            level = logging.WARNING
        case 1:
            level = logging.INFO
        case _:
            level = logging.DEBUG

    logging.basicConfig(level=level)

    if recursive:
        sub_dir_paths = set()

        for path in paths:
            sub_dir_paths.union(find_finished_jobs(path=path))

        paths = sub_dir_paths

    for old_job in paths:
        new_job = create_vibration(
            submit=submit,
            file_size_limit=file_size_limit,
            old_job=old_job,
            calc_mods=calc_mods,
            slurm_mods=slurm_mods,
            files_to_carry_over=files_to_carry_over or None,
            tags_to_unfreeze=tags_to_unfreeze,
            infrared=infrared,
        )
        click.echo(f"New job created {'/'.join(new_job.parts[-4:])}")
        new_calculation = new_job.parent
        click.echo(
            f"New calculation created: {'/'.join(new_calculation.parts[-3:])}"
        )
