from collections.abc import Generator
from pathlib import Path
import stat
import subprocess

import pytest

from autojob import SETTINGS


@pytest.fixture(name="script_text")
def fixture_script_text(shared_datadir: Path) -> Generator[str, None, None]:
    with shared_datadir.joinpath("test.sh").open(
        mode="r", encoding="utf-8"
    ) as file:
        loc = file.tell()
        yield file.read()
        file.seek(loc)


@pytest.fixture(name="days", params=(0, 1))
def fixture_days(request: pytest.FixtureRequest) -> int:
    days: int = request.param
    return days


@pytest.fixture(name="hours", params=(0, 1))
def fixture_hours(request: pytest.FixtureRequest) -> int:
    hours: int = request.param
    return hours


@pytest.fixture(name="minutes", params=(0, 1))
def fixture_minutes(request: pytest.FixtureRequest) -> int:
    minutes: int = request.param
    return minutes


@pytest.fixture(name="seconds", params=(0, 1))
def fixture_seconds(request: pytest.FixtureRequest) -> int:
    seconds: int = request.param
    return seconds


@pytest.fixture(name="time")
def fixture_time(
    days: int | None,
    hours: int | None,
    minutes: int | None,
    seconds: int | None,
) -> str:
    if days is None:
        if seconds is None:
            return str(minutes)
        if hours is None:
            return f"{minutes}:{seconds}"
        return f"{hours}:{minutes}:{seconds}"

    if minutes is None:
        return f"{days}-{hours}"

    if seconds is None:
        return f"{days}-{hours}:{minutes}"

    return f"{days}-{hours}:{minutes}:{seconds}"


@pytest.fixture(name="time_seconds")
def fixture_time_seconds(
    days: int | None,
    hours: int | None,
    minutes: int | None,
    seconds: int | None,
) -> str:
    return (
        (days or 0) * 24 * 60 * 60
        + (hours or 0) * 60 * 60
        + (minutes or 0) * 60
        + (seconds or 0)
    )


@pytest.fixture(name="write_script")
def fixture_write_script(script_text: str, time: str, tmp_path: Path) -> Path:
    script = tmp_path.joinpath(SETTINGS.SLURM_SCRIPT)
    with script.open(mode="w", encoding="utf-8") as file:
        file.write(script_text.replace("{{ slurm_time }}", time))
    script.chmod(stat.S_IRUSR + stat.S_IXUSR)
    return script


@pytest.fixture(name="run_script")
def fixture_run_script(write_script: Path) -> str:
    output = subprocess.check_output(  # noqa: S603
        [str(write_script.resolve())],
        encoding="utf-8",
    )
    return output


class TestCalculateStopTime:
    @staticmethod
    @pytest.mark.parametrize(
        ("days", "hours", "seconds"), [(None, None, None)]
    )
    def test_should_parse_format_1(run_script: str, time_seconds: int) -> None:
        assert f"This means {time_seconds} seconds" in run_script

    @staticmethod
    @pytest.mark.parametrize(("days", "hours"), [(None, None)])
    def test_should_parse_format_2(run_script: str, time_seconds: int) -> None:
        assert f"This means {time_seconds} seconds" in run_script

    @staticmethod
    @pytest.mark.parametrize(("days"), [(None)])
    def test_should_parse_format_3(run_script: str, time_seconds: int) -> None:
        assert f"This means {time_seconds} seconds" in run_script

    @staticmethod
    @pytest.mark.parametrize(("minutes", "seconds"), [(None, None)])
    def test_should_parse_format_4(run_script: str, time_seconds: int) -> None:
        assert f"This means {time_seconds} seconds" in run_script

    @staticmethod
    @pytest.mark.parametrize(("seconds"), [(None)])
    def test_should_parse_format_5(run_script: str, time_seconds: int) -> None:
        assert f"This means {time_seconds} seconds" in run_script

    @staticmethod
    def test_should_parse_format_6(run_script: str, time_seconds: int) -> None:
        assert f"This means {time_seconds} seconds" in run_script
