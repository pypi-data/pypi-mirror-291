"""This module defines the ``Job`` class and the ``JobError`` enum.

.. deprecated:: Use :mod:`autojob.task`, :mod:`autojob.calculation`,
                :mod:`autojob.hpc` instead.

"""

from abc import ABC
from abc import abstractmethod
import datetime
from enum import Enum
from enum import unique
import math
import operator
import re
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from monty import json

from autojob.coordinator import classification

if TYPE_CHECKING:
    from collections.abc import Callable

COMPLEX_DICT = dict[str, str | int]

JOB_STATS_FIELDS = [
    "MaxRSS",
    "Partition",
    "Submit",
    "Start",
    "End",
    "NCPUS",
    "NNodes",
]
JOB_FILE = "job.json"


T = TypeVar("T", bound="JobStats")


# TODO: inherit from RuntimeError?
# ! This should be an error
@unique
class JobError(Enum):
    """A job error."""

    TIME_LIMIT = "time limit"
    MEMORY_LIMIT = "memory limit"

    def __str__(self) -> str:
        """A string representation of the ``JobError``."""
        return self.value


# ? Are properties necessary here?
class CalculationParameter:
    """Abstraction of an input parameter for a supported ASE calculator.

    Attributes:
        _name: The name of the InputParameter.

        _explicit: Whether the set of allowed values for the
        InputParameter is explicitly specified. True if the set of allowed
        values for the input parameter is explicitly specified; False
        otherwise.

        _allowed_types: The allowed types for the InputParameter. For
        validation and displaying (in the GUI application) purposes, if
        there exists special values for the InputParameter (e.g., string
        values that correspond to particular values), the allowed types
        should not be designated so as to include these special values.

        For example, say that a particular InputParameter accepts integer
        values, but that the string 'normal' corresponds to a particular
        value. The allowed types for the InputParameter should be specified
        as [int] and not [int, str].

        Only primitive types are allowed as entries in '_allowed_types'.
        That is, the entries must be one of str, int, bool, or float:

            _allowed_types = [int]                      <--- allowed
            _allowed_types = [int, str]                 <--- allowed
            _allowed_types = [Union[int, str]]          <--- not allowed
            _allowed_types = [list, str]                <--- not allowed
            _allowed_types = [List, str]                <--- not allowed
            _allowed_types = [List[int], str]           <--- not allowed
            _allowed_types = [Tuple[int, int, int]]     <--- not allowed
            _allowed_types = [List[List[int]]]          <--- not allowed

        _values: Indicates the allowed values of an InputParameter.

                 If the allowed values are explicitly specified, then the
                 tuple contains the only allowed values.

                 If the allowed values are specified as a range, then the
                 tuple should contain three entries.

                 The first and second items in the tuple indicate the
                 lower and upper bounds of the range, respectively, which
                 should be set to -math.inf and math.inf to specify that
                 the range is unbounded with respect to the bound.

                 The third item should be a string, indicating how to
                 treat the endpoints of the range in the same style as
                 traditional mathematical notation:

                    "[]" = both bounds included
                    "[)" = lower bound included, upper bound excluded
                    "(]" = lower bound excluded, upper bound included
                    "()" = both bounds excluded

        _specials: Indicates any special, allowed parameter values that
        may not satisfy the conditions specified in the '_values' tuple.
        Defaults to an empty list.

        _default: A default value for the InputParameter.

        _description: Returns a description of the InputParameter to be
        used for displaying tooltips.
    """

    def __init__(
        self,
        name: str,
        explicit: bool,
        allowed_types: list[type],
        values: tuple,
        default: float | int | str | None = None,
        description: str | None = None,
        specials: list | None = None,
    ):
        """Initialize a ``CalculationParameter``.

        Args:
            name: The name of the ``CalculationParameter``.
            explicit: Whether or not the parameter must be specified
                explicitly.
            allowed_types: An iterable containing the allowed parameter types.
            values: A tuple either containing the explicit values or a 3-tuple
                indicating the bounds of the parameter.
            default: The default value of the parameter. Defaults to None.
            description: A description of the parameter. Defaults to None.
            specials: Special values of the parameter that are not subject to
                validation. Defaults to None.
        """
        self._name: str = name
        self._explicit_values: bool = explicit
        self._allowed_types: list[type] = allowed_types

        # Granular typing
        if explicit:
            self._values: tuple = values
        else:
            self._values: tuple = values

        self._default: float | int | str | None = default
        self._description: str = description or ""
        self._specials: list = specials or []

    @property
    def name(self):
        """The name of the `CalculationParameter`."""
        return self._name

    @property
    def description(self) -> str:
        """A description of the parameter."""
        return self._description

    @property
    def explicit_values(self) -> bool:
        """Whether or not the parameter value is to be chosen from a list."""
        return self._explicit_values

    @property
    def values(self) -> tuple:
        """A tuple indicating the values of the parameter or its bounds."""
        return self._values

    @property
    def allowed_types(self) -> list[type]:
        """The allowed types of the parameter."""
        return self._allowed_types.copy()

    @property
    def default(self) -> Any:
        """The default value of the parameter."""
        return self._default

    @property
    def specials(self) -> list:
        """Special values of the parameter."""
        return self._specials.copy()

    def __str__(self) -> str:
        """A string representation of the parameter."""
        return self._name

    def _validate(self, val: Any, comp: Any) -> bool:
        types = []
        types.append(type(comp))

        if float in types:
            types.append(int)

        for next_type in types:
            try:
                typed_val = next_type(val)
                # Naive check to see if typing changed 'val'
                if isinstance(typed_val, int) and float(val) != typed_val:
                    continue

                # Attempt to validate after casting
                if typed_val == comp:
                    return True

            except (ValueError, TypeError):
                continue

        return False

    def validate(self, val: Any) -> bool:
        """Validates a value.

        Args:
            val (Any): The value to be validated

        Returns:
            bool: True if 'val' is valid. False otherwise.
        """
        if self._explicit_values:
            return self._validate_explicit(val)

        for value in self._specials:
            if self._validate(val, value):
                return True

        try:
            if float in self._allowed_types:
                typed_val = float(val)
            elif int in self._allowed_types and int(val) == float(val):
                typed_val = int(val)
            else:
                return str in self._allowed_types
        except ValueError:
            return False

        left_bounds = self._values[0]
        right_bounds = self._values[1]

        # Define comparison operators
        if "[" in self._values[2]:
            left_op: Callable = operator.le
        else:
            left_op: Callable = operator.lt

        if "]" in self._values[2]:
            right_op: Callable = operator.le
        else:
            right_op: Callable = operator.lt

        return left_op(left_bounds, typed_val) and right_op(
            typed_val, right_bounds
        )

    def _validate_explicit(self, val: Any) -> bool:
        return any(self._validate(val, value) for value in self._values)

    def is_finite_int_range(self) -> bool:
        """Whether the parameter is restricted to a finite range of ints."""
        return (
            int in self.allowed_types
            and self.values[0] != -math.inf
            and self.values[1] != math.inf
        )


class JobStats(json.MSONable):
    """Job statistics.

    Attributes:
        memory: The memory used for the job in kilobytes.
        start_time: The :class:`datetime.datetime` instance representing the
            time that the job started.
        end_time: The :class:`datetime.datetime` instance representing the
            time that the job ended.
        submit_time: The :class:`datetime.datetime` instance representing the
            time that the job was submitted.
        cores: The number of cores that the job ran on.
        nodes: The number of nodes that the job ran on.
        partition: A :class:`.Partition` instance representing the cluster
            partition that the job ran on.
    """

    def __init__(
        self,
        src_dict: dict[
            str,
            str,
        ],
    ) -> None:
        """Initialize a ``JobStats`` instance.

        Args:
            src_dict: A dictionary mapping ``sacct`` headers to their values
                for a SLURM job. The dictionary should have the keys listed
                in :attr:`.job.JOB_STATS_FIELDS`.
        """
        if not isinstance(src_dict, dict):
            msg = 'Supplied "src_dict" must be a dictionary.'
            raise TypeError(msg)

        for field in JOB_STATS_FIELDS:
            if field not in src_dict:
                msg = f'Missing field ({field}) in supplied "src_dict".'
                raise ValueError(msg)

        self.memory: int = JobStats.parse_max_rss(src_dict["MaxRSS"])
        self.start_time: datetime.datetime = datetime.datetime.fromisoformat(
            src_dict["Start"]
        )
        self.end_time: datetime.datetime = datetime.datetime.fromisoformat(
            src_dict["End"]
        )
        self.submit_time: datetime.datetime = datetime.datetime.fromisoformat(
            src_dict["Submit"]
        )
        self.cores: int = src_dict["NCPUS"]
        self.nodes: int = src_dict["NNodes"]
        self.partition = src_dict["Partition"]

    def as_dict(self) -> dict:
        """Return the ``JobStats`` instance as a JSON-able dictionary."""
        return {
            "MaxRSS": f"{self.memory}K",
            "Start": self.start_time.isoformat(),
            "End": self.end_time.isoformat(),
            "Submit": self.submit_time.isoformat(),
            "NCPUS": self.cores,
            "NNodes": self.nodes,
            "Partition": self.partition,
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "JobStats":
        """Create a ``JobStats`` instance from a dictionary.

        :meth:`JobStats.as_dict` and :meth:`JobStats.from_dict` are designed
        such that "round-trips" as supported. That is, given an instance
        of ``JobStats``, ``job_stats``, the following is True::

            job_stats == JobStats.from_dict(job_stats.as_dict())
        """
        return cls(d)

    @property
    def run_time(self) -> datetime.timedelta:
        """The run time for the job."""
        return self.end_time - self.start_time

    @property
    def queued_time(self) -> datetime.timedelta:
        """The time for which the job was queued."""
        return self.start_time - self.submit_time

    @property
    def wall_time(self) -> datetime.timedelta:
        """The time between job submission and completion."""
        return self.end_time - self.submit_time

    @staticmethod
    def parse_max_rss(max_rss: str) -> float:
        """Convert a memory string to memory in kilobytes."""
        if not isinstance(max_rss, str):
            msg = '"max_rss" value must be type string.'
            raise TypeError(msg)

        match = re.fullmatch(r"\d+(\.\d*)?([GKM])", max_rss)
        if not match:
            msg = f'Invalid format for "max_rss": {max_rss}'
            raise ValueError(msg)

        max_rss = float(max_rss.removesuffix(match[2]))
        match match[2]:
            case "G":
                multiplier = 1e6
            case "M":
                multiplier = 1e3
            case "K":
                multiplier = 1
            case _:
                msg = f'Invalid format for "max_rss": {max_rss}'
                raise ValueError(msg)

        return max_rss * multiplier


# TODO: adapt for non-Vasp jobs
class Job(ABC, json.MSONable):
    """A SLURM job.

    Subclasses must implement the abstract method ``input_parameters()``

    Attributes:
        _id: Job ID

        _input_structure: Input structure for job run.

        _output_structure: Output structure from job run.

        _submission_params: Parameters for the submission of the job to the
        job scheduler.

        _stats: Statistics from the job run.

        _error: Error incurred during job run.

        _note: Additional note for job.
    """

    def __init__(
        self,
        job_id: str,
        calculation_id: str,
        study_id: str,
        study_group_id: str,
        input_parameters: dict,
        results: dict,
        job_stats: COMPLEX_DICT | None,
        # TODO: replace with parameters.CalculatorType
        calculator_type: classification.CalculatorType | None = None,
        calculation_type: classification.CalculationType | None = None,
        study_type: classification.StudyType | None = None,
        error: JobError | None = None,
        name: str = "",
        notes: str = "",
    ):
        """Initialize a ``Job``.

        Args:
            job_id: The job ID.
            calculation_id: The calculation ID.
            study_id: The study ID.
            study_group_id: The study group ID.
            input_parameters: The input parameters for the job.
            results: The job results.
            job_stats: The job statistics.
            calculator_type: The calculator type. Defaults to None.
            calculation_type: The calculation type. Defaults to None.
            study_type: The study type. Defaults to None.
            error: The job error. Defaults to None.
            name: The job name. Defaults to "".
            notes: Notes on the job. Defaults to "".
        """
        self.job_id = job_id
        self.calculation_id = calculation_id
        self.study_id = study_id
        self.study_group_id = study_group_id

        self.calculator_type = calculator_type
        self.calculation_type = calculation_type
        self.study_type = study_type

        self.inputs = input_parameters
        self.outputs = results

        self.job_stats: JobStats = JobStats(job_stats)

        self.error = error

        self.name = name
        self.notes = notes

    def __eq__(self, obj: Any) -> bool:
        """Check if object is a ``Job`` with matching IDs, stats, errors."""
        return (
            isinstance(obj, Job)
            and obj.job_id == self.job_id
            and obj.calculation_id == self.calculation_id
            and obj._job_stats == self.job_stats
            and obj._error == self.error
            and obj.notes == self.notes
        )

    @abstractmethod
    def as_dict(self) -> dict:
        """Convert the ``Job`` to a JSON-able dictionary."""

    @abstractmethod
    def as_flat_dict(self) -> dict:
        """Convert the ``Job`` to a flattened dictionary."""

    @classmethod
    @abstractmethod
    def from_dict(cls, d: dict) -> "Job":
        """Create a ``Job`` instance from a dictionary.

        :meth:`Job.as_dict` and :meth:`Job.from_dict` should be designed
        such that "round-trips" as supported. That is, given an instance
        of ``Job``, ``job``, the following is True::

            job == Job.from_dict(job.as_dict())
        """

    @staticmethod
    @abstractmethod
    def input_parameters() -> list[CalculationParameter]:
        """Returns the input parameters for the type of job.

        Subclasses should implement this method.
        """

    # TODO: design method for checking compatibility and necessity of certain
    # input parameters
    # e.g., dipole-related parameters should either all be on or off
    # e.g., relation between NBANDS, NCORE, NPAR, KPAR, NELC, and NIONS
