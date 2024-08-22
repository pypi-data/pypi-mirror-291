"""Utilities for parsing data."""

import ast
from collections.abc import Iterable
from datetime import datetime
from datetime import timedelta
import importlib
import logging
import pathlib
import re
from typing import Any
from typing import Literal
from typing import NamedTuple
from typing import TypeVar

from pydantic import ImportString

from autojob.coordinator import job

logger = logging.getLogger(__name__)


class TimedeltaTuple(NamedTuple):
    """Convenience wrapper around a timedelta object."""

    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0

    def __str__(self) -> str:
        """Return the result of `.to_slurm_time()`."""
        return self.to_slurm_time()

    @classmethod
    def from_timedelta(cls, delta: timedelta) -> "TimedeltaTuple":
        """Break a timedelta instance into days, hours, minutes, and seconds.

        Args:
            delta: a timedelta instance.

        Returns:
            A 4-tuple of ints: days, hours, minutes, seconds
        """
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds - (hours * 3600)) // 60
        seconds = delta.seconds - (hours * 3600) - (minutes * 60)
        return cls(days, hours, minutes, seconds)

    @classmethod
    def from_string(
        cls,
        string: str,
        time_format: Literal["iso", "slurm"] = "slurm",
    ) -> "TimedeltaTuple":
        """Return a TimedeltaTuple from a string.

        Args:
            string: the time string to parse.
            time_format: One of "iso" or "slurm". Determines how the time
                string is parsed.

        Returns:
            A TimedeltaTuple.
        """
        match time_format:
            case "slurm":
                return TimedeltaTuple.from_slurm_time(string)
            case "iso":
                dt = datetime.fromisoformat(string)
                midnight = datetime(
                    year=dt.year,
                    month=dt.month,
                    day=dt.day,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                    tzinfo=dt.tzinfo,
                )
                return cls.from_timedelta(dt - midnight)
            case _:
                raise NotImplementedError

    @classmethod
    def from_slurm_time(cls, time: str) -> "TimedeltaTuple":
        """Parses a valid slurm time value into a TimedeltaTuple.

        The six formats accepted by Slurm are:

            1:            minutes

            2:            minutes:seconds

            3:      hours:minutes:seconds

            4: days-hours

            5: days-hours:minutes

            6: days-hours:minutes:seconds

        Args:
            time: the string containing the value of the --time slurm option

        Raises:
            ValueError: The string is not a valid value of the slurm --time
                option. See https://slurm.schedmd.com/sbatch.html for details.

        Returns:
            A TimedeltaTuple.
        """
        logger.debug(f"Parsing slurm time from {time=!r}")
        pattern1 = (
            r"^(?:(?=\d+:\d+:\d+$)(?P<hours>\d+):)?(?P<minutes>\d+)"
            r"(:(?P<seconds>\d+))?$"
        )
        match1 = re.match(pattern1, time.strip())
        pattern2 = (
            r"^(?P<days>\d+)-(?P<hours>\d+)(:(?P<minutes>\d+)(:"
            r"(?P<seconds>\d+))?)?$"
        )
        match2 = re.match(pattern2, time.strip())
        if match1:
            match = match1
        elif match2:
            match = match2
        else:
            msg = f"{time} is not a valid value of the slurm --time option"
            raise ValueError(msg)

        parsed_time_denominations = {
            k: int(v)
            for k, v in match.groupdict().items()
            if k and v is not None
        }
        logger.debug(
            f"Successfully parsed slurm time from {time=!r}. "
            f"Values: {parsed_time_denominations=!r}"
        )
        return cls(**parsed_time_denominations)

    def to_timedelta(self) -> timedelta:
        """Convert a `TimedeltaTuple` to a `timedelta` instance."""
        return timedelta(
            days=self.days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds,
        )

    @staticmethod
    def format_time(time_denomination: int) -> str:
        """Format time into a 0-padded integer."""
        if 0 <= time_denomination < 10:  # noqa: PLR2004
            return f"0{time_denomination}"

        return str(time_denomination)

    # TODO: Use format spec
    def to_slurm_time(self) -> str:
        """Convert `TimedeltaTuple` into a SLURM-compatible time format."""
        days = f"{self.days}-" if self.days else ""
        hours = TimedeltaTuple.format_time(self.hours)
        minutes = TimedeltaTuple.format_time(self.minutes)
        seconds = TimedeltaTuple.format_time(self.seconds)
        return f"{days}{hours}:{minutes}:{seconds}"


_T = TypeVar("_T")


def vectorize_underscored_data(rows: list[str]) -> tuple[list[str], list[str]]:
    """Turns rows of underscored data into columns.

    An example of supported data is that which is returned by the SLURM command
    `sacct`::

       Partition     MaxRSS   NNodes               Start
       --------- ---------- -------- -------------------
            razi                   1 2022-07-29T09:48:15
                  18049744K        1 2022-07-29T09:48:15
                          0        1 2022-07-29T09:48:15

    Args:
        rows: A list of strings read from a file containing the output from
            a Slurm job stats file or sacct.

    Returns:
        Vectorized job stats are returned as a tuple (headers, columns) where
        headers is a list of strings representing the headers used in the job
        stats file and columns is a list of lists of strings representing the
        remaining entries in the column. The header delimiters are excluded.
    """
    logger.debug(f"Vectorizing data:\n\n{rows}\n")

    delimiters = rows[1]
    headers: list[str] = []
    column_widths = [len(x) for x in delimiters.split()]
    columns: list[list[str]] = []
    boundary = 0

    for width in column_widths:
        headers.append(rows[0][boundary : boundary + width])
        columns.append([row[boundary : boundary + width] for row in rows[2:]])
        boundary += width + 1

    logger.debug(f"Successfully vectorized data:\n{headers!r}\n{columns!r}\n")
    return headers, columns


def reduce_sparse_vector(vector: Iterable[_T]) -> _T:
    """Returns the first value in the sparse vector.

    Args:
        vector: An iterable.

    Raises:
        ValueError: The vector is empty.
    """
    try:
        return next(x for x in vector if x.replace(" ", ""))
    except StopIteration as err:
        msg = "No values in sparse vector"
        raise ValueError(msg) from err


def parse_job_stats_file(
    stats_file: pathlib.Path,
) -> dict[str, float | int | str]:
    """Parse information from a job stats file into a dictionary.

    Args:
        stats_file: Path to jobstats.txt file.

    Raises:
        ValueError: Missing headers in job stats file or extra headers found.

    Returns:
        The parsed job stats dictionary.

        Note that no validation/conversion is done to the field values.
        Conversion to valid (more useful) Python values can be performed
        using `SchedulerOutputs.model_validate`.
    """
    logger.debug(f"Parsing job stats from: {stats_file}")

    with stats_file.open(encoding="utf-8") as file:
        rows = file.readlines()

    headers, columns = vectorize_underscored_data(rows=rows)
    headers = [h.replace(" ", "") for h in headers]
    values = []

    for i, column in enumerate(columns):
        try:
            value = reduce_sparse_vector(vector=column).replace(" ", "")
        except ValueError:
            logger.info(f"No value found for {headers[i]}")
            value = None
        values.append(value)

    # Create job stats dictionary
    try:
        job_stats = dict(zip(headers, values, strict=True))
    except ValueError as error:
        msg = "Unable to parse job stats file."
        raise ValueError(msg) from error

    missing_headers = [
        header for header in job.JOB_STATS_FIELDS if header not in job_stats
    ]

    if missing_headers:
        missing = ", ".join(missing_headers)
        msg = f"Missing headers in job stats file: {missing}."
        raise ValueError(msg)

    logger.debug(f"Successfully parsed job stats from: {stats_file}")
    return job_stats


def parse_job_error(slurm_file: pathlib.Path) -> job.JobError | None:
    """Parse the reason for job termination from the slurm script.

    Args:
        slurm_file: A Path pointing to the slurm script.

    Returns:
        A `JobError` corresponding to the reason for job termination,
        otherwise None.
    """
    logger.info(f"Parsing job error in {slurm_file}")
    error_checker = re.compile(r"Cancelled due to (time|memory) limit")
    with slurm_file.open(encoding="utf-8") as file:
        for line in file:
            match = error_checker.search(line)
            if match:
                reason = match.group(1)
                error = job.JobError(f"{reason} limit")
                logger.info(f"Job error found: {error}")
                return error
    logger.info("No job error found")
    return None


def extract_keyword_arguments(
    keywords: list[ast.keyword], code: ast.Module
) -> dict[str, Any]:
    """Extract the runtime values of the keyword arguments to a function.

    Args:
        keywords: A list of keyword objects.
        code: The module object of which the keywords are descendents.

    Returns:
        A dictionary mapping the keywords to the runtime values.
    """
    assignments = [
        node
        for node in ast.walk(code)
        if isinstance(node, ast.AnnAssign | ast.Assign)
    ]

    kwargs: dict[str, Any] = {}

    for keyword in keywords:
        try:
            kwargs[keyword.arg] = eval(  # noqa: S307
                ast.unparse(keyword.value)
            )
        except NameError as err:
            match = re.match(r"name '(.*)' is not defined", err.args[0])
            missing_name = match.group(1)
            # The value is a variable, so we try to determine its runtime value
            for assignment in assignments:
                names = [
                    x.id for x in assignment.targets if isinstance(x, ast.Name)
                ]
                if missing_name in names:
                    _locals = {
                        missing_name: eval(  # noqa: S307
                            ast.unparse(assignment.value)
                        )
                    }
                    value = eval(  # noqa: S307
                        ast.unparse(keyword.value),
                        None,
                        _locals,
                    )
                    kwargs[keyword.arg] = value
                    break

            if keyword.arg not in kwargs:
                raise

    return kwargs


def import_class(class_string: ImportString[_T]) -> _T:
    """Import a class using its fully qualified name.

    Args:
        class_string: The fully qualified name of the class. For example,
            autojob.hpc.SchedulerInputs.

    Returns:
        The class.
    """
    if isinstance(class_string, str):
        parts = class_string.split(".")
        name = ".".join(parts[:-1])
        class_name = parts[-1]
        mod = importlib.import_module(name)
        return getattr(mod, class_name)

    raise TypeError
