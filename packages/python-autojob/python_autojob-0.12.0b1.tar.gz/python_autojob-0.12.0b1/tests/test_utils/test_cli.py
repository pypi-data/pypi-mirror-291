from typing import Any

import pytest

from autojob import SETTINGS
from autojob.utils.cli import configure_settings
from autojob.utils.cli import mods_to_dict
from autojob.utils.schemas import Unset


@pytest.fixture(name="param_name")
def fixture_param_name() -> str:
    param_name = "opt"
    return param_name


@pytest.fixture(
    name="param_value",
    params=("Tight", "NoFreeze", "CalcAll", "Tight,CalcAll"),
)
def fixture_param_value(request: pytest.FixtureRequest) -> str:
    param_value: str = request.param
    return param_value


@pytest.fixture(name="cli_values")
def fixture_cli_values(param_name: str, param_value: str) -> tuple[str]:
    cli_value = f"{param_name}={param_value}"
    return (cli_value,)


@pytest.fixture(name="mods")
def fixture_mods(param_name: str, param_value: str) -> dict[str, Any]:
    mods = {param_name: param_value}
    return mods


class TestModsToDict:
    @staticmethod
    def test_should_return_correct_mods(
        cli_values: str, mods: dict[str, Any]
    ) -> None:
        assert mods_to_dict(None, None, cli_values) == mods

    @staticmethod
    @pytest.mark.parametrize("param_value", ["MaxCyles=250"])
    def test_should_parse_value_with_equals_sign(
        cli_values: str, mods: dict[str, Any]
    ) -> None:
        assert mods_to_dict(None, None, cli_values) == mods

    @staticmethod
    @pytest.mark.parametrize("param_value", [""])
    def test_should_set_empty_value_to_unset(
        param_name: str, cli_values: str
    ) -> None:
        assert mods_to_dict(None, None, cli_values)[param_name] == Unset


@pytest.fixture(name="setting", params=("SLURM_SCRIPT", "PYTHON_SCRIPT"))
def fixture_setting(request: pytest.FixtureRequest) -> str:
    setting: str = request.param
    return setting


@pytest.fixture(name="value", params=("run.sh", "test.sh"))
def fixture_value(request: pytest.FixtureRequest) -> str:
    value: str = request.param
    return value


class TestConfigureSettings:
    @staticmethod
    def test_should_set_settings(setting: str, value: Any) -> None:
        configure_settings({setting: value})
        assert getattr(SETTINGS, setting) == value
