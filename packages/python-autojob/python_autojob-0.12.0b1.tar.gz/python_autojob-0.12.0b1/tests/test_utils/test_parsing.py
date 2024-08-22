from datetime import datetime
from datetime import timedelta
from itertools import repeat
import logging
import pathlib

import pytest

from autojob.coordinator.job import JobError
from autojob.hpc import Partition
from autojob.utils.files import JOB_STATS_FILE
from autojob.utils.parsing import TimedeltaTuple
from autojob.utils.parsing import parse_job_error
from autojob.utils.parsing import parse_job_stats_file
from autojob.utils.parsing import reduce_sparse_vector
from autojob.utils.parsing import vectorize_underscored_data

logger = logging.getLogger(__name__)


def _fill(v: int) -> str:
    return f"0{v}" if v < 10 else str(v)


class TestTimedeltaTuple:
    @staticmethod
    @pytest.fixture(name="slurm_days", params=[1, 2])
    def fixture_slurm_days(request: pytest.FixtureRequest) -> int:
        slurm_day: int = request.param
        return slurm_day

    @staticmethod
    @pytest.fixture(name="slurm_hours", params=[0, 1])
    def fixture_slurm_hours(request: pytest.FixtureRequest) -> int:
        slurm_hours: int = request.param
        return slurm_hours

    @staticmethod
    @pytest.fixture(name="slurm_minutes", params=[0, 1])
    def fixture_slurm_minutes(request: pytest.FixtureRequest) -> int:
        slurm_minutes: int = request.param
        return slurm_minutes

    @staticmethod
    @pytest.fixture(name="slurm_seconds", params=[0, 1])
    def fixture_slurm_seconds(request: pytest.FixtureRequest) -> int:
        slurm_seconds: int = request.param
        return slurm_seconds

    @staticmethod
    def test_should_create_equivalent_timedelta(
        slurm_days: int,
        slurm_hours: int,
        slurm_minutes: int,
        slurm_seconds: int,
        elapsed: timedelta,
    ) -> None:
        assert (
            slurm_days,
            slurm_hours,
            slurm_minutes,
            slurm_seconds,
        ) == TimedeltaTuple.from_timedelta(delta=elapsed)

    @staticmethod
    def test_should_create_timedeltatuple_from_string1(
        slurm_days: int,
        slurm_hours: int,
        slurm_minutes: int,
        slurm_seconds: int,
    ) -> None:
        string = f"{slurm_days}-{slurm_hours}:{slurm_minutes}:{slurm_seconds}"
        assert (
            slurm_days,
            slurm_hours,
            slurm_minutes,
            slurm_seconds,
        ) == TimedeltaTuple.from_string(string=string, time_format="slurm")

    @staticmethod
    def test_should_create_timedeltatuple_from_string2(
        slurm_days: int,
        slurm_hours: int,
    ) -> None:
        string = f"{slurm_days}-{slurm_hours}"
        assert (
            slurm_days,
            slurm_hours,
        ) == TimedeltaTuple.from_string(string=string, time_format="slurm")[:2]

    @staticmethod
    @pytest.mark.parametrize("invalid_string", ["a", "1.00.00", "$1 ", "\n"])
    def test_should_raise_value_error_from_string_with_invalid_string(
        invalid_string: str,
    ) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            _ = TimedeltaTuple.from_string(invalid_string)

    @staticmethod
    @pytest.mark.parametrize("invalid_string", ["a", "1.00.00", "$1 ", "\n"])
    def test_should_raise_value_error_from_slurm_time_with_invalid_string(
        invalid_string: str,
    ) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            _ = TimedeltaTuple.from_slurm_time(invalid_string)

    @staticmethod
    def test_should_accept_slurm_format_1(slurm_minutes: int) -> None:
        string = str(slurm_minutes)
        _, _, minutes, _ = TimedeltaTuple.from_slurm_time(time=string)
        assert minutes == slurm_minutes

    @staticmethod
    def test_should_accept_slurm_format_2(
        slurm_minutes: int, slurm_seconds: int
    ) -> None:
        string = f"{slurm_minutes}:{slurm_seconds}"
        _, _, minutes, seconds = TimedeltaTuple.from_slurm_time(time=string)
        assert (minutes, seconds) == (slurm_minutes, slurm_seconds)

    @staticmethod
    def test_should_accept_slurm_format_3(
        slurm_hours: int,
        slurm_minutes: int,
        slurm_seconds: int,
    ) -> None:
        string = f"{slurm_hours}:{slurm_minutes}:{slurm_seconds}"
        _, hours, minutes, seconds = TimedeltaTuple.from_slurm_time(
            time=string
        )
        assert (hours, minutes, seconds) == (
            slurm_hours,
            slurm_minutes,
            slurm_seconds,
        )

    @staticmethod
    def test_should_accept_slurm_format_4(
        slurm_days: int, slurm_hours: int
    ) -> None:
        string = f"{slurm_days}-{slurm_hours}"
        days, hours, _, _ = TimedeltaTuple.from_slurm_time(time=string)
        assert (days, hours) == (
            slurm_days,
            slurm_hours,
        )

    @staticmethod
    def test_should_accept_slurm_format_5(
        slurm_days: int,
        slurm_hours: int,
        slurm_minutes: int,
    ) -> None:
        string = f"{slurm_days}-{slurm_hours}:{slurm_minutes}"
        days, hours, minutes, _ = TimedeltaTuple.from_slurm_time(time=string)
        assert (days, hours, minutes) == (
            slurm_days,
            slurm_hours,
            slurm_minutes,
        )

    @staticmethod
    def test_should_accept_slurm_format_6(
        slurm_days: int,
        slurm_hours: int,
        slurm_minutes: int,
        slurm_seconds: int,
    ) -> None:
        string = f"{slurm_days}-{slurm_hours}:{slurm_minutes}:{slurm_seconds}"
        days, hours, minutes, seconds = TimedeltaTuple.from_slurm_time(
            time=string
        )
        assert (days, hours, minutes, seconds) == (
            slurm_days,
            slurm_hours,
            slurm_minutes,
            slurm_seconds,
        )

    @staticmethod
    def test_should_reverse_from_timedelta(elapsed: timedelta) -> None:
        assert (
            elapsed
            == TimedeltaTuple.from_timedelta(delta=elapsed).to_timedelta()
        )

    @staticmethod
    def test_should_reverse_to_timedelta(
        slurm_days: int,
        slurm_hours: int,
        slurm_minutes: int,
        slurm_seconds: int,
    ) -> None:
        delta = TimedeltaTuple(
            days=slurm_days,
            hours=slurm_hours,
            minutes=slurm_minutes,
            seconds=slurm_seconds,
        )
        assert delta == TimedeltaTuple.from_timedelta(delta.to_timedelta())

    @staticmethod
    def test_should_reverse_from_string(
        slurm_days: int,
        slurm_hours: int,
        slurm_minutes: int,
        slurm_seconds: int,
    ) -> None:
        string = (
            f"{slurm_days}-{_fill(slurm_hours)}:{_fill(slurm_minutes)}:"
            f"{_fill(slurm_seconds)}"
        )
        assert (
            string == TimedeltaTuple.from_string(string=string).to_slurm_time()
        )

    @staticmethod
    def test_should_reverse_from_slurm_time(
        slurm_days: int,
        slurm_hours: int,
        slurm_minutes: int,
        slurm_seconds: int,
    ) -> None:
        string = (
            f"{slurm_days}-{_fill(slurm_hours)}:{_fill(slurm_minutes)}:"
            f"{_fill(slurm_seconds)}"
        )
        assert (
            string
            == TimedeltaTuple.from_slurm_time(time=string).to_slurm_time()
        )

    @staticmethod
    def test_should_reverse_to_slurm_time(
        slurm_days: int,
        slurm_hours: int,
        slurm_minutes: int,
        slurm_seconds: int,
    ) -> None:
        delta = TimedeltaTuple(
            days=slurm_days,
            hours=slurm_hours,
            minutes=slurm_minutes,
            seconds=slurm_seconds,
        )
        assert delta == TimedeltaTuple.from_slurm_time(delta.to_slurm_time())


class TestVectorizeUnderscoredData:
    @staticmethod
    @pytest.fixture(name="num_columns", params=[1, 3, 7])
    def fixture_num_columns(request: pytest.FixtureRequest) -> list[str]:
        num_columns: int = request.param
        return num_columns

    @staticmethod
    @pytest.fixture(name="headers")
    def fixture_headers(num_columns: int) -> list[str]:
        headers = [str(x) for x in range(num_columns)]
        return headers

    @staticmethod
    @pytest.fixture(name="values")
    def fixture_values(num_columns: int) -> list[str]:
        values = [f"Value {x}A" for x in range(num_columns)]
        return values

    @staticmethod
    @pytest.fixture(name="underscore_lengths")
    def fixture_underscore_lengths(
        headers: list[str], values: list[str]
    ) -> list[int]:
        underscore_lengths: list[int] = []
        for entries in zip(headers, values, strict=True):
            underscore_lengths.append(max(len(x) for x in entries))

        return underscore_lengths

    @staticmethod
    def test_should_vectorize_data(
        underscore_lengths: list[int], headers: list[str], values: list[str]
    ) -> None:
        spaced_headers = [
            x.rjust(underscore_lengths[i]) for i, x in enumerate(headers)
        ]
        underscores = [
            x * underscore_lengths[i]
            for i, x in enumerate(repeat("_", len(headers)))
        ]
        spaced_values = [
            x.rjust(underscore_lengths[i]) for i, x in enumerate(values)
        ]

        vectorized_values = [[x] for x in spaced_values]
        rows = [
            " ".join(spaced_headers),
            " ".join(underscores),
            " ".join(spaced_values),
        ]
        logger.debug(f"Expected Headers:\n{spaced_headers}")
        logger.debug(f"Expected Rows:\n{rows}")

        assert vectorize_underscored_data(rows=rows) == (
            spaced_headers,
            vectorized_values,
        )


class TestReduceSparseVector:
    @staticmethod
    @pytest.fixture(name="expected_value")
    def fixture_expected_value() -> str:
        expected_value = "111"
        return expected_value

    @staticmethod
    @pytest.fixture(name="vector")
    def fixture_vector() -> list[str]:
        vector = [
            " " * 10,
            "111",
            "a",
        ]
        return vector

    @staticmethod
    def test_should_return_first_alphanumeric_string_in_vector(
        vector: list[str],
        expected_value: str,
    ) -> None:
        assert reduce_sparse_vector(vector) == expected_value

    @staticmethod
    def test_should_raise_value_error_for_empty_vector() -> None:
        vector = [" ", ""]
        with pytest.raises(ValueError, match="No values in sparse vector"):
            _ = reduce_sparse_vector(vector)


class TestParseJobStatsFile:
    @staticmethod
    @pytest.mark.output_files("job_stats")
    def test_should_load_matching_dictionary(
        populate_outputs: pathlib.Path,
        job_stats: dict[str, int | Partition | datetime],
    ) -> None:
        stats_file = populate_outputs.joinpath(JOB_STATS_FILE)
        parsed_job_stats = parse_job_stats_file(stats_file=stats_file)
        assert parsed_job_stats["NCPUS"] == str(job_stats["NCPUS"])
        assert parsed_job_stats["Submit"] == job_stats["Submit"].isoformat()
        assert parsed_job_stats["MaxRSS"] == f"{int(job_stats['MaxRSS'])}K"
        assert parsed_job_stats["Start"] == job_stats["Start"].isoformat()
        assert parsed_job_stats["End"] == job_stats["End"].isoformat()
        assert parsed_job_stats["NNodes"] == str(job_stats["NNodes"])
        assert (
            parsed_job_stats["Partition"]
            == job_stats["Partition"].cluster_name
        )


class TestParseJobError:
    # ! Add memory limit test
    @staticmethod
    @pytest.mark.output_files("slurm_output_file")
    @pytest.mark.parametrize("job_error", [JobError.TIME_LIMIT])
    def test_should_identify_time_limit(
        populate_outputs: pathlib.Path,
        slurm_output_filename: str,
        job_error: JobError | None,
    ) -> None:
        slurm_file: str = populate_outputs.joinpath(slurm_output_filename)
        assert parse_job_error(slurm_file=slurm_file) == job_error

    @staticmethod
    @pytest.mark.output_files("slurm_output_file")
    @pytest.mark.parametrize("job_error", [None])
    def test_should_identify_non_time_limit(
        populate_outputs: pathlib.Path,
        slurm_output_filename: str,
    ) -> None:
        slurm_file: str = populate_outputs.joinpath(slurm_output_filename)
        assert parse_job_error(slurm_file=slurm_file) is None
