"""Utilities for templating strings."""

import logging

logger = logging.getLogger(__name__)


def substitute_placeholders(
    templated_value: str,
    /,
    **kwargs,
) -> str:
    """Subtitute values for placeholders.

    Args:
        templated_value: The templated value.
        **kwargs: Each keyword should be a valid Python identifier
            and the corresponding value is its replacement. Keywords will
            be converted by replacing hyphens with underscores.

    Returns:
        The original string with placeholders substituted.

    Example::

        >>> import pathlib
        >>> from autojob.next.relaxation import _substitute_placeholders

        >>> _substitute_placeholders(
                "This is the job id: %{job-id}",
                job_id="j123456789",
            )
        This is the job id: j123456789
    """
    logger.debug(f"Substituting placeholders in {templated_value}")
    value = templated_value
    for variable, replacement in kwargs.items():
        template = "%{" + variable.replace("_", "-").lower() + "}"
        value = value.replace(template, str(replacement))
    logger.debug(
        f"Successfully substituted placeholders in {templated_value}: {value}"
    )
    return value
