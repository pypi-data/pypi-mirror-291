from collections.abc import Iterable
from itertools import chain
from itertools import permutations
from itertools import product
from types import NoneType
from typing import Any
from typing import ClassVar

import pytest

from autojob.coordinator.validation import alphanum_key
from autojob.coordinator.validation import alphanum_sort
from autojob.coordinator.validation import iter_to_native
from autojob.coordinator.validation import val_to_native


class TestValidation:
    num_vals: ClassVar[list[float | int]] = [
        -1,
        0,
        34,
        -0.2,
        -10000.3,
        1,
        1e-2,
        -13e10,
    ]
    num_val_pairs: ClassVar[list[Any]] = [
        (str(val), ("n", float(val))) for val in num_vals
    ]

    str_vals: ClassVar[list[str]] = [
        "DOG",
        "d*g",
        "dog",
        "cat",
        "12dj",
        "check",
        "182.4529a",
        "*342.d",
        " ",
        "",
        "^#&",
    ]
    str_val_pairs: ClassVar[list[Any]] = [
        (val, ("s", val)) for val in str_vals
    ]

    bool_pairs: ClassVar[list[Any]] = [
        (str(True), ("b", True)),
        (str(False), ("b", False)),
    ]

    none_pair = (str(None), ("N", None))

    arg_result_pairs = num_val_pairs
    arg_result_pairs.extend(str_val_pairs)
    arg_result_pairs.extend(bool_pairs)
    arg_result_pairs.append(none_pair)

    @staticmethod
    @pytest.mark.parametrize(("arg", "result"), arg_result_pairs)
    def test_alphanum_key(arg, result):
        assert alphanum_key(arg) == result

    bad_vals: ClassVar[list[Any]] = [
        1,
        -1,
        1e-4,
        1000,
        True,
        [1],
        (1,),
        {"a": 1},
        None,
    ]

    @staticmethod
    @pytest.mark.parametrize("val", bad_vals)
    def test_alphanum_key_with_bad_vals(val: Any):
        with pytest.raises(TypeError) as exc_info:
            alphanum_key(val)

        assert f"Type: {type(val)} not supported." in exc_info.value.args[0]

    vals = num_vals[:3]
    vals.extend(str_vals[:3])
    vals.extend([True, False, None])
    unsorted: ClassVar[list[Any]] = list(permutations(vals, 2))
    unsorted.append([])

    @staticmethod
    @pytest.mark.parametrize("to_sort", unsorted)
    def test_alphanum_sort(to_sort: Iterable):
        alphanum_sorted = alphanum_sort([str(x) for x in to_sort])
        type_to_key = {
            bool: "b",
            float: "n",
            int: "n",
            str: "s",
            NoneType: "N",
        }
        to_sort = list(to_sort)
        if not to_sort:
            assert alphanum_sorted == to_sort
        elif type_to_key[type(to_sort[0])] == type_to_key[type(to_sort[1])]:
            to_sort.sort()
            assert alphanum_sorted == [str(x) for x in to_sort]
        else:
            key_to_val = {}
            for val in to_sort:
                key = type_to_key[type(val)]
                key_to_val[key] = val

            values = sorted(key_to_val.keys())
            sorted_ = [str(key_to_val[x]) for x in values]
            assert alphanum_sorted == sorted_

    to_convert = num_vals
    to_convert.extend(str_vals)
    to_convert.extend([True, False, None])

    @staticmethod
    @pytest.mark.parametrize("to_native", to_convert)
    def test_val_to_native(to_native: float | int):
        assert val_to_native(str(to_native)) == to_native

    iters: ClassVar[list[type]] = [set, tuple, list]
    pairs = product(chain(num_vals[:3], str_vals[:3], [None]), iters)
    func_val_pairs: ClassVar[list[tuple[Any, Any]]] = [
        (x, y) for x, y in pairs if not isinstance(x, bool)
    ]

    @staticmethod
    @pytest.mark.parametrize(("to_native", "func"), func_val_pairs)
    def test_iter_to_native(to_native, func):
        assert iter_to_native(func([str(to_native)])) == func([to_native])
