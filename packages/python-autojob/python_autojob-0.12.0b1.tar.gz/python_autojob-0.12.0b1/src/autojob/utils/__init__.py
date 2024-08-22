"""Miscellaneous `autojob` utility functions."""

from collections.abc import Callable
from collections.abc import Iterable
from typing import Any
from typing import TypeVar

from autojob.utils.files import get_slurm_job_id
from autojob.utils.files import get_uri
from autojob.utils.parsing import parse_job_error
from autojob.utils.parsing import parse_job_stats_file
from autojob.utils.parsing import reduce_sparse_vector
from autojob.utils.parsing import vectorize_underscored_data

__all__ = [
    "get_uri",
    "get_slurm_job_id",
    "parse_run_file",
    "parse_job_stats_file",
    "parse_job_error",
    "reduce_sparse_vector",
    "vectorize_underscored_data",
    "get_slurm_job_id",
    "validate_id",
    "alphanum_key",
    "alphanum_sort",
    "val_to_native",
    "iter_to_native",
]


PRIMITIVE_TYPE = bool | float | int | str | None
_T = TypeVar("_T")


def alphanum_key(val: str) -> tuple[str, PRIMITIVE_TYPE]:
    """Provides key to alphanumerically sort primitive types.

    Args:
        val: String representation of object for which to provide key.

    Raises:
        TypeError: The type of 'val' is invalid.

    Returns:
        A 2-tuple where the first element is a string indicating the type of
        the value (e.g., n = number, b = boolean, N = None, s = string) and
        the second element is the value.

    Note:
        Numbers are converted to floats.
    """
    if not isinstance(val, str):
        msg = (
            f"Type: {type(val)} not supported. alphanum_key "
            "only supports arguments of type: str."
        )
        raise TypeError(msg)

    try:
        val_key = float(val)
        type_key = "n"
    except ValueError:
        match val:
            case "True" | "False":
                type_key = "b"
                val_key = val == "True"
            case "None":
                type_key = "N"
                val_key = None
            case _:
                type_key = "s"
                val_key = val

    return type_key, val_key


def alphanum_sort(vals: Iterable[str]) -> list[str]:
    """Alphanumerically sorts an iterable of strings.

    Args:
        vals: an iterable to be sorted.

    Returns:
        Alphanumerically sorted copy of ``vals``.
    """
    return sorted(vals, key=alphanum_key)


def val_to_native(val: float | int | str | None) -> PRIMITIVE_TYPE:
    """Converts string representations to their native types.

    Only floats, ints, or strings are supported.

    Args:
        val: a value to be converted.

    Returns:
        The value converted into a :attr:`PRIMITIVE_TYPE`.
    """
    try:
        float_val = float(val)
        try:
            int_val = int(val)
            native_val = int_val if int_val == float_val else float_val
        except ValueError:
            native_val = float_val
    except (ValueError, TypeError):
        if val == "True":
            native_val = True
        elif val == "False":
            native_val = False
        elif val == "None":
            native_val = None
        else:
            native_val = val

    return native_val


def iter_to_native(
    vals: Iterable[float | int | str | None],
) -> Iterable[float | int | str | None]:
    """Converts values within an Iterable to their native types.

    Args:
        vals: an iterable of values to convert.

    Returns:
        Iterable: A shallow copy of the converted iterable.

    Example:
        >>> from autojob.utils import iter_to_native
        >>> iter_to_native(["0.1", "None", "-1", "dog"])
        [0.1, None, -1, "dog"]
    """
    new_vals = []
    constructor = type(vals)

    for val in vals:
        new_vals.append(val_to_native(val))

    try:
        return constructor(new_vals)
    except (TypeError, ValueError):
        return list(new_vals)
