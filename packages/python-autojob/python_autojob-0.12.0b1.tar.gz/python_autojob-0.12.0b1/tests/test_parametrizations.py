from typing import Any

import pytest

from autojob.parametrizations import AttributePath
from autojob.parametrizations import VariableReference
from autojob.utils.schemas import Unset


class TestSetInputValue:
    @staticmethod
    @pytest.fixture(name="path_key")
    def fixture_path_key() -> str:
        path_key = "a"

        return path_key

    @staticmethod
    @pytest.fixture(name="set_path")
    def fixture_set_path(path_key: str) -> AttributePath:
        set_path = [path_key]
        return set_path

    @staticmethod
    def test_should_delete_unset_variable(
        set_path: AttributePath, path_key: str
    ) -> None:
        constant = Unset
        ref = VariableReference(set_path=set_path, constant=constant)
        context = {}
        shell = {path_key: None}
        res = {}
        ref.set_input_value(context=context, shell=shell)
        assert shell == res

    @staticmethod
    @pytest.mark.parametrize("constant", [1, 1.0, "", None, {}])
    def test_should_set_value_to_constant(
        constant: Any,
        set_path: AttributePath,
        path_key: str,
    ) -> None:
        ref = VariableReference(set_path=set_path, constant=constant)
        context = {}
        shell = {}
        res = {path_key: constant}
        ref.set_input_value(context=context, shell=shell)
        assert shell == res
