"""Utilities for CLI functions."""

from collections.abc import Iterable
from contextlib import suppress
import logging
import re
from typing import Any
from typing import ClassVar

import click

from autojob import SETTINGS
from autojob.coordinator.validation import val_to_native
from autojob.hpc import convert
from autojob.utils.schemas import Unset

logger = logging.getLogger(__name__)


class MemoryFloat(click.ParamType):
    """A float representing an amount of memory."""

    name: ClassVar[str] = "memory float"

    def convert(self, value: str | float, param, ctx) -> float:
        """Convert a memory specification into bytes."""
        if not isinstance(value, str | float):
            msg = f"{param.name} should be a string or a float: {value!r}"
            self.fail(msg, param=param, ctx=ctx)

        with suppress(ValueError):
            return float(value)

        if match := re.match(
            r"(?P<memory>\d+(?:\.\d+)?)(?P<units>(?:K|M|G)(?:B)?)", value
        ):
            memory = float(match.group("memory"))
            units = match.group("units")
            return convert(memory=memory, from_units=units, to_units="B")

        msg = f"'{value}' is not a valid memory specification"
        self.fail(msg, param=param, ctx=ctx)


def mods_to_dict(_: Any, param: str, value: Iterable[str]) -> dict[str, Any]:
    """Convert an iterable of key-value pairs to a dictionary.

    Args:
        _: The first argument is ignored but retained for `click`
            compatibility.
        param: The name of the parameter being set (e.g., `calc_mods` or
            `slurm_mods`).
        value: An iterable of key-value pairs should exist as a string in the
            form "key=value". Note that only those values supported by
            `~validation.val_to_native` can be correctly parsed.

    Returns:
        A dictionary mapping calculator parameter names to their Python values.
    """
    if not isinstance(value, Iterable):
        msg = f"Something is wrong. {param} should be an iterable: {value!r}"
        raise click.BadParameter(message=msg)

    mods = {}

    for x in value:
        if not isinstance(x, str):
            msg = (
                f"Something is wrong. Each item in {param} should be a "
                f"string: {x!r}"
            )
            raise click.BadParameter(message=msg)

        if "=" not in x:
            msg = (
                f"Something is wrong. Each item in {param} should be a "
                f"must have the form 'key=value'"
            )
            raise click.BadParameter(message=msg)

        parameter = x.split("=")[0]
        assignment_value = x.split("=", maxsplit=1)[1]

        if assignment_value == "":
            mods[parameter] = Unset
        else:
            mods[parameter] = val_to_native(assignment_value)

    return mods


# * Define a decorator (e.g., @reconstructed) which sets this as the object in
# * the context (e.g., ctx.obj = construct_cli_call(ctx=ctx, allowed=allowed))
def construct_cli_call(
    allowed: list[str] | None = None,
) -> str:
    """Construct the original CLI call.

    Args:
        allowed: A list of strings indicating which parameters are to be
            considered to reconstruct the CLI call.

    Returns:
        A string representing the command-line call that would produce the
        present behaviour.
    """
    logger.debug("Constructing CLI call")
    allowed = [] if allowed is None else allowed
    # This works so long as the CLI only accepts options
    ctx = click.get_current_context()
    args: list[str] = []

    for param, value in ctx.params.items():
        if (
            ctx.get_parameter_source(param)
            == click.core.ParameterSource.COMMANDLINE
            and param in allowed
        ):
            if isinstance(value, list | tuple):
                for element in value:
                    args.append(
                        f'--{param.rstrip("s").replace("_", "-")}'
                        f'="{str(element).split("/")[-1]}"'
                    )
            elif isinstance(value, dict):
                for key, element in value.items():
                    args.append(
                        f'--{param.rstrip("s").replace("_", "-")}'
                        f'="{key}={element!s}"'
                    )
            # This won't work if flag_value=False
            elif isinstance(value, bool) and value:
                args.append(f'--{param.replace("_", "-")}')
            elif param == "verbosity" and value > 0:
                args.append(f"-{'v'*value}")
            else:
                args.append(f'--{param.replace("_", "-")}="{value}"')

    command = f"{ctx.command.name} {' '.join(args)}".strip()
    logger.debug(f"Successfully constructed CLI call: {command}")
    return command


def configure_settings(config: dict[str, Any]) -> None:
    """Set redefine autojob settings.

    Args:
        config: A dictionary mapping autojob settings names to their desired
            values.
    """
    for setting, value in config.items():
        attr = setting.upper()
        if hasattr(SETTINGS, attr):
            setattr(SETTINGS, attr, value)
        else:
            logger.warning(
                f"Unknown setting provided for configuration: {value}"
            )
