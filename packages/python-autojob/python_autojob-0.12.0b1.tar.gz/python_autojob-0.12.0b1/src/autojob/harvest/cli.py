"""CLI function for harvesting task results."""

from pathlib import Path
from typing import Literal

import click

from autojob.harvest.archive import archive
from autojob.harvest.harvest import harvest


# TODO: convert whitelist/blacklist from file paths into job directory strings
@click.group(
    "harvest",
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "--path",
    "dir_name",
    default=Path.cwd(),
    type=click.Path(
        exists=True, file_okay=False, readable=True, path_type=Path
    ),
)
@click.option(
    "--filename",
    default="harvested",
    help="The file stem to use to name the harvested data file.",
)
@click.option(
    "--archive-mode",
    default="csv",
    help="The mode with which to archive the harvested tasks.",
    type=click.Choice(("csv", "json", "both")),
)
@click.option(
    "--strict",
    "strictness",
    flag_value="strict",
    default="relaxed",
    help="Errors will immediately halt execution.",
)
@click.option(
    "--relaxed",
    "strictness",
    flag_value="relaxed",
    default="relaxed",
    help="Only jobs for which no errors are thrown during harvesting will be "
    "harvested.",
)
@click.option(
    "--atomic",
    "strictness",
    flag_value="atomic",
    default="relaxed",
    help="Every attempt will be made to harvest data from every directory. "
    "Incomplete data does not cause execution to halt.",
)
@click.option(
    "--whitelist",
    multiple=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
    help="Specify an exclusive list of jobs to harvest. Whitelists will be "
    "combined.",
)
@click.option(
    "--blacklist",
    multiple=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
    help="Specify a list of jobs not to harvest. Blacklists will be "
    "combined. When specified with --whitelist, --blacklist will take a "
    "higher priority.",
)
def main(
    *,
    dir_name: Path,
    strictness: Literal["strict", "relaxed", "atomic"],
    whitelist: tuple[Path],
    blacklist: tuple[Path],
    archive_mode: Literal["csv", "json", "both"],
    filename: str,
) -> None:
    """Harvest completed tasks from a directory."""
    harvested = harvest(
        dir_name=dir_name,
        strictness=strictness,
        whitelist=whitelist or None,
        blacklist=blacklist or None,
    )
    archive(filename=filename, archive_mode=archive_mode, harvested=harvested)
