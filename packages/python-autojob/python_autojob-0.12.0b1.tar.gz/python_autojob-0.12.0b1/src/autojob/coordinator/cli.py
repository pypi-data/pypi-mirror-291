"""Define the CLI function for the ``Coordinator`` GUI."""

import pathlib

import click

from autojob import SETTINGS
from autojob.coordinator.gui import gui


@click.group(
    name="harvest",
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "--template-dir",
    default=None,
    help="The directory from which to pull script templates. If not "
    "specified, autojob will use its own templates.",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
)
@click.option(
    "--dest",
    default=None,
    help="The root directory for study group creation.",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
)
@click.argument(
    "template",
    required=False,
    default=None,
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
)
def main(  # noqa: D417
    template: pathlib.Path | None,
    template_dir: pathlib.Path | None,
    dest: pathlib.Path | None,
):
    """Runs the GUI for 'Coordinator'.

    This is a graphical user interface that enables you to design arbitrarily
    large studies which are parametrized with respect to input structures, any
    input variable for an ASE calculator, or even SLURM parameter.

    Args:
        template: a previously configured study group, study, calculation, or
        job with which to populate the GUI. Defaults to None.
    """
    SETTINGS.TEMPLATE_DIR = template_dir
    gui.run(template, dest=dest)
