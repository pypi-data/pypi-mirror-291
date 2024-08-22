"""Validate and convert values to desired types."""

from collections.abc import Iterable
from typing import TypeVar

_T = TypeVar("_T", bool, float, int, None, str)


def _validate_id(old_func):
    def new_func(new_id: str):
        if new_id.isdigit() and int(new_id) >= 0:
            old_func(new_id)
        else:
            msg = "ID string must represent a nonnegative integer."
            raise ValueError(msg)

    return new_func


def alphanum_key(val: str) -> tuple[str, _T]:
    """A key for alphanumerically sorting strings.

    Args:
        val (str): String representation of object for which to provide key.

    Raises:
        TypeError: The type of 'val' is invalid.

    Returns:
        Tuple[str, Union[bool, float, int, None, str]]: Key for 'val'.
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
    """Alphanumerically sorts 'vals'.

    Args:
        vals (Iterable): Iterable to be sorted

    Returns:
        List[str]: Alphanumerically sorted copy of 'vals'.
    """
    return sorted(vals, key=alphanum_key)


def val_to_native(val: float | int | str | None) -> _T:
    """Converts string representations of float/int/str to its native type.

    Args:
        val (Optional[Union[float, int, str]]): Parameter to be converted.

    Returns:
        PRIMITIVE_TYPE: The converted parameter.
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
    """Converts elements of an iterable to their native types.

    Args:
        vals (Iterable[Optional[float, int, str]]): Iterable to be converted

    Returns:
        Iterable: A shallow copy of the converted Iterable.

    Example:
        >>> from autojob.coordinator.validation import iter_to_native
        >>> vals = ["0.1", "None", "-1", "dog"]
        >>> iter_to_native(vals)
        [0.1, None, -1, 'dog']
    """
    new_vals = []
    constructor = type(vals)

    for val in vals:
        new_vals.append(val_to_native(val))

    try:
        return constructor(new_vals)
    except (TypeError, ValueError):
        return list(new_vals)
