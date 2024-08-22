"""Interface with high performance computing resources."""

from __future__ import annotations

import datetime
from enum import Enum
from enum import unique
import logging
import pathlib
import re
from typing import TYPE_CHECKING
from typing import Annotated
from typing import Any
from typing import ClassVar
from typing import NamedTuple
from typing import Self
from typing import TextIO
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import FieldSerializationInfo
from pydantic import SerializerFunctionWrapHandler
from pydantic import ValidationInfo
from pydantic import ValidatorFunctionWrapHandler
from pydantic import WrapSerializer
from pydantic import WrapValidator
from pydantic import field_serializer
from pydantic import field_validator
from pydantic import model_validator

from autojob.utils import parsing
from autojob.utils.files import create_job_stats_file
from autojob.utils.files import find_slurm_file
from autojob.utils.files import get_slurm_job_id
from autojob.utils.schemas import hyphenate

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="Partition")

MEMORY_RE = r"^(?P<memory>[0-9.]+)(?P<units>[A-Za-z]*)$"
_memory_keys = ["mem", "mem_per_cpu"]


def convert(memory: float, from_units: str, to_units: str) -> float:
    """Convert memory denominations in binary.

    Units can be specified using uppercase, lowercase, one-, or two-letter
    abbreviations.
    E.g., 'K', 'k', 'KB', 'kb' are all interpreted as kilobytes.

    Args:
        memory (float): memory to be converted.
        from_units (str): The units from which memory is to be converted.
        to_units (str): The units to which memory is to be converted.

    Returns:
        float: The memory in the desired units.
    """
    factor = _determine_conversion_factor(units=from_units)
    divisor = _determine_conversion_factor(units=to_units)

    return (factor / divisor) * memory


def _determine_conversion_factor(units: str) -> float:
    prefixes = ["", "k", "m", "g", "t"]
    units = units.lower().rstrip("b")
    try:
        exponent = prefixes.index(units)
        return 1e3**exponent
    except ValueError as err:
        msg = f"Unknown units specified: {units}"
        raise ValueError(msg) from err


def validate_memory(
    v: Any,
    handler: ValidatorFunctionWrapHandler,
    _: ValidationInfo,
) -> int | None:
    """Validate the memory request."""
    logger.debug(f"Validating memory: {v}")
    if isinstance(v, str):
        match = re.match(pattern=MEMORY_RE, string=v)
        memory = float(match.group("memory"))
        units = match.group("units") or "MB"
        logger.debug(f"Validating memory: {memory} in units: {units}")
        value = convert(memory=memory, from_units=units, to_units="MB")
        return int(value)

    return handler(v)


def validate_time(
    v: Any,
    handler: ValidatorFunctionWrapHandler,
    _: ValidationInfo,
) -> datetime.timedelta | None:
    """Validate the time request."""
    if isinstance(v, str):
        return parsing.TimedeltaTuple.from_slurm_time(time=v).to_timedelta()

    return handler(v)


def serialize_memory(
    v: Any,
    _: FieldSerializationInfo,
) -> str | None:
    """Serialize the memory request into a SLURM-compatible format."""
    return v if v is None else f"{v!s}MB"


def serialize_time(
    v: Any,
    _: FieldSerializationInfo,
) -> str | None:
    """Serialize the time request into a SLURM-compatible format."""
    if isinstance(v, datetime.timedelta):
        return parsing.TimedeltaTuple.from_timedelta(v).to_slurm_time()

    return None


Memory = Annotated[
    int,
    WrapValidator(validate_memory),
    WrapSerializer(serialize_memory, when_used="json"),
]
Time = Annotated[
    datetime.timedelta,
    WrapValidator(validate_time),
    WrapSerializer(serialize_time, when_used="json"),
]


class Cluster(NamedTuple):
    """A computing cluster."""

    name: str
    affiliation: str = ""
    alliance: str | None = None
    partitions: Iterable[Partition] | None = None


@unique
class Partition(Enum):
    """A partition on a computing cluster."""

    BIGMEM = ("bigmem", 4, 80, True, 8256000000, 1 * 24 * 60)
    CPU2013 = ("cpu2013", 14, 16, False, 120000000, 7 * 24 * 60)
    CPU2017_BF05 = ("cpu2017-bf05", 36, 28, False, 245000000, 5 * 60)
    CPU2019 = (
        "cpu2019",
        40,
        40,
        False,
        185000000,
        7 * 24 * 60,
    )
    CPU2019_BF05 = (
        "cpu2019-bf05",
        87,
        40,
        False,
        185000000,
        5 * 60,
    )
    CPU2021 = (
        "cpu2021",
        34,
        48,
        False,
        185000000,
        7 * 24 * 60,
    )
    CPU2021_BF24 = (
        "cpu2021-bf24",
        7,
        48,
        False,
        381000000,
        24 * 60,
    )
    CPU2022 = (
        "cpu2022",
        52,
        52,
        False,
        256000000,
        7 * 24 * 60,
    )
    CPU2022_BF24 = (
        "cpu2022-bf24",
        16,
        52,
        False,
        256000000,
        24 * 60,
    )
    CPU2023 = (
        "cpu2023",
        52,
        53,  # this is actually 52, but changed so that differs from CPU2022
        False,
        256000000,
        7 * 24 * 60,
    )
    GPU_V100 = (
        "gpu-v100",
        13,
        40,
        True,
        753000000,
        1 * 24 * 60,
    )
    LATTICE = (
        "lattice",
        196,
        8,
        False,
        11800000,
        7 * 24 * 60,
    )
    PARALLEL = (
        "parallel",
        576,
        12,
        False,
        23000000,
        7 * 24 * 60,
    )
    RAZI = (
        "razi",
        54,
        40,
        False,
        185000000,
        7 * 24 * 60,
    )
    SINGLE = (
        "single",
        168,
        8,
        False,
        11800000,
        7 * 24 * 60,
    )

    def __new__(
        cls: type[Self],
        name: str,
        nodes: int,
        cpus_per_node: int,
        gpu: bool,
        max_mem_per_node: int,
        time_limit: float,
    ) -> Self:
        """Initialize the ``Partition`` object."""
        entry = object.__new__(cls)
        entry._name_ = entry._value_ = (
            name  # set the value, and the extra attribute
        )
        entry._nodes = nodes  # type: ignore[attr-defined]
        entry._cpus_per_node = cpus_per_node  # type: ignore[attr-defined]
        entry._gpu = gpu  # type: ignore[attr-defined]
        entry._max_mem_per_node = max_mem_per_node  # type: ignore[attr-defined]
        entry._time_limit = time_limit  # type: ignore[attr-defined]
        return entry

    def __repr__(self):
        """A string representation of the ``Partition``."""
        return (
            f"<{type(self).__name__}.{self.name}: ({self._name_!r}, "
            f"{self._nodes!r}, {self._cpus_per_node!r}, {self._gpu!r}, "
            f"{self._max_mem_per_node!r}, {self._time_limit!r})>"
        )

    def __str__(self) -> str:
        """A string representation of the ``Partition``."""
        return self.cluster_name

    @property
    def cluster_name(self):
        """The name of the cluster with underscores replaced with hyphens."""
        return self.name.lower().replace("_", "-")

    @property
    def nodes(self):
        """The number of nodes in the partition."""
        return self._nodes

    @property
    def cpus_per_node(self):
        """The number of cores per node in the partition."""
        return self._cpus_per_node

    @property
    def gpu(self):
        """Whether the partition is GPU-enabled."""
        return self._gpu

    @property
    def max_mem_per_node(self):
        """The maximum memory per node on the partition."""
        return self._max_mem_per_node

    @property
    def time_limit(self):
        """The maximum time limit for the partition."""
        return self._time_limit


class SchedulerInputs(BaseModel):
    """The inputs for the scheduler.

    Attributes are named for convenience/intuitiveness. Aliases
    are provided for consistency with SLURM. Special validation
    for parsing values as provided to SLURM options is performed
    by default.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=hyphenate)

    job_name: str | None = None
    account: str | None = None
    partitions: list[Partition] | None = Field(
        default=None,
        description="The partitions specified for the job",
        alias="partition",
    )
    mem: Memory | None = Field(
        default=None,
        description="The memory requested per node in MB.",
    )
    mem_per_cpu: Memory | None = Field(
        default=None,
        description="The memory requested per cpu in MB.",
    )
    nodes: int | None = None
    cores_per_node: int | None = Field(
        default=None,
        description="The number of cores per node",
        alias="ntasks-per-node",
    )
    time: Time | None = Field(
        default=None,
        description="The time requested for a job.",
    )
    mail_user: str | None = None
    mail_type: list[str] | None = Field(
        default=None,
        description=(
            "The list of conditions for which email notifications will "
            "be sent"
        ),
    )

    @field_validator("partitions", mode="wrap")
    @classmethod
    def validate_partitions(
        cls,
        v: Any,
        handler: ValidatorFunctionWrapHandler,
        _: ValidationInfo,
    ) -> float | None:
        """Validate the partitions in the scheduler request."""
        if isinstance(v, str):
            return [Partition(x) for x in v.split(",")]

        return handler(v)

    @field_validator("mail_type", mode="wrap")
    @classmethod
    def validate_mail_type(
        cls,
        v: Any,
        handler: ValidatorFunctionWrapHandler,
        _: ValidationInfo,
    ) -> list[str] | None:
        """Validate the ``mail_type`` option value."""
        if isinstance(v, str):
            return v.split(",")

        return handler(v)

    # Pydantic issue: why do I have to specify return_type
    @field_serializer("partitions", mode="wrap", return_type=list)
    def serialize_partitions(
        self,
        v: Any,
        _: SerializerFunctionWrapHandler,
        info: FieldSerializationInfo,
    ) -> list[str] | str | None:
        """Serialize the partitions in the scheduler request."""
        if self.partitions is None:
            return None

        if info.mode == "json":
            return ",".join(str(x) for x in self.partitions)

        return v

    # Pydantic issue: why do I have to specify return_type
    @field_serializer("mail_type", mode="wrap", return_type=list)
    def serialize_mail_type(
        self,
        v: Any,
        _: SerializerFunctionWrapHandler,
        info: FieldSerializationInfo,
    ) -> list[str] | str | None:
        """Serialize the ``mail_type`` option value."""
        if self.mail_type is None:
            return None

        if info.mode == "json":
            return ",".join(str(x) for x in self.mail_type)

        return v

    @classmethod
    def from_directory(cls, dir_name: str | pathlib.Path) -> SchedulerInputs:
        """Load scheduler inputs from Slurm file.

        Args:
            dir_name: The directory to load inputs from.

        Returns:
            A SchedulerInputs dictionary.
        """
        logger.debug(f"Loading scheduler inputs from {dir_name}")
        from autojob import SETTINGS

        slurm_script = pathlib.Path(dir_name).joinpath(SETTINGS.SLURM_SCRIPT)

        with slurm_script.open(mode="r", encoding="utf-8") as file:
            inputs = cls.extract_scheduler_inputs(file)

        scheduler_inputs = cls(**inputs)

        logger.debug(f"Successfully loaded scheduler inputs from {dir_name}")
        return scheduler_inputs

    @staticmethod
    def extract_scheduler_inputs(stream: TextIO | list[str]) -> dict[str, str]:
        """Parse a slurm submission file to determine the slurm options.

        Args:
            stream: A TextIO containing the contents of the slurm submission
                file.

        Returns:
            A dictionary mapping slurm parameter names to parameter values.

            Note that no validation/conversion is done to the field values.
            Conversion to valid (more useful) Python values can be performed
            using `SchedulerInputs.model_validate`.
        """
        log_addendum = ""

        if hasattr(stream, "name"):
            offset = stream.tell()
            log_addendum = f" from {stream.name}"

        logger.debug(f"Extracting scheduler inputs{log_addendum}")

        slurm_param_re = re.compile(
            r"^#SBATCH\s*-(?:-)?(?P<parameter>[a-zA-Z\-]*)=(?P<value>.*)$"
        )
        parameters: dict[str, Any] = {}
        reading_code = reading_slurm_params = False

        for line in stream:
            match = slurm_param_re.match(line)
            if match and not reading_code:
                reading_slurm_params = True
                parameter, value = match.groups()
                parameters[parameter] = value
            elif (
                reading_slurm_params
                and not line.lstrip().startswith("#")  # not a comment
                and line.strip()  # non-whitespace character
            ):
                reading_code = True

        if hasattr(stream, "name"):
            stream.seek(offset)

        logger.debug(
            f"Successfully extracted scheduler inputs{log_addendum}: "
            f"{parameters}"
        )
        return parameters

    @staticmethod
    def _update_memory(inputs: dict[str, Any], mods: dict[str, Any]) -> None:
        """Update the memory request.

        This method modifies `inputs` in place.

        Args:
            inputs: A dictionary containing SchedulerInputs fields.
            mods: A dictionary containing new values with which to update
                `inputs`. Note that only one of `mem` and `mem_per_cpu` can be
                set.
        """
        set_memory_keys = [k for k in mods if k in _memory_keys]

        if not set_memory_keys:
            return None

        set_memory_key = set_memory_keys[0]
        new_memory_value = mods[set_memory_key]

        for key in _memory_keys:
            if key in inputs:
                old_value = inputs.pop(key)

                if key == set_memory_key:
                    suffix = f" with {key}: {new_memory_value}"
                else:
                    suffix = ""
                logger.info(f"Unsetting {key}: {old_value}{suffix}")

        logger.info(f"Setting {set_memory_key}: {new_memory_value}")
        inputs[set_memory_key] = new_memory_value

    @staticmethod
    def update_values(inputs: dict[str, Any], mods: dict[str, Any]) -> None:
        """Safely updates scheduler parameters subject to SLURM conditions.

        This method modifies `inputs` in place.

        Args:
            inputs: A dictionary containing SchedulerInputs fields.
            mods: A dictionary containing new values with which to update
                `inputs`. Note that only one of `mem` and `mem_per_cpu` can be
                set.
        """
        logger.debug("Safely updating scheduler parameters")
        SchedulerInputs._update_memory(inputs, mods)

        for k, v in mods.items():
            if k not in _memory_keys:
                inputs[k] = v
                logger.info(f"Setting parameter '{k}' to: {v}")

        logger.debug("Safely updated scheduler parameters")

    def check_inputs(self) -> list[str]:
        """Check that the scheduler request is valid."""
        msgs = []
        if None not in (self.mem, self.mem_per_cpu):
            msgs.append(
                "SLURM does not permit setting both `mem` and `mem_per_cpu`"
            )

        return msgs


@unique
class SchedulerError(Enum):
    """A scheduler error."""

    TIME_LIMIT = "time limit"
    MEMORY_LIMIT = "memory limit"

    def __str__(self) -> str:
        """A string representation of the error."""
        return self.value


class SchedulerOutputs(BaseModel):
    """The outputs from a scheduler task."""

    model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

    elapsed: Time | None = Field(
        default=None,
        description="The job wall time.",
    )
    error: SchedulerError | None = None
    idle_time: Time | None = Field(
        default=None,
        description="The time required for the job to start after submission.",
    )
    job_id: int | None = None
    max_rss: Memory | None = Field(
        default=None,
        description="Maximum memory used by job",
        alias="MaxRSS",
    )
    partition: Partition | None = None

    @model_validator(mode="after")
    def time_validator(self) -> SchedulerOutputs:
        """Calculate and set the time-related attributes."""
        try:
            submit = datetime.datetime.fromisoformat(self.Submit)
        except (AttributeError, ValueError):
            return self

        try:
            start = datetime.datetime.fromisoformat(self.Start)
        except (AttributeError, ValueError):
            return self

        self.idle_time = start - submit

        try:
            end = datetime.datetime.fromisoformat(self.End)
        except (AttributeError, ValueError):
            return self

        self.elapsed = end - start

        return self

    # TODO: implement strict_mode
    # TODO: use sacct -j JOB_ID --json or -p
    @classmethod
    def from_directory(cls, dir_name: str | pathlib.Path) -> SchedulerOutputs:
        """Load scheduler outputs from Slurm file.

        Args:
            dir_name: The directory to load outputs from.

        Returns:
            A SchedulerOutputs dictionary.
        """
        logger.debug(f"Loading scheduler outputs from {dir_name}")
        from autojob import SETTINGS

        job_stats = {"job_id": None}
        stats_file = pathlib.Path(dir_name).joinpath(SETTINGS.JOB_STATS_FILE)

        try:
            job_stats["job_id"] = job_id = get_slurm_job_id(job_dir=dir_name)
        except FileNotFoundError as err:
            job_stats["job_id"] = job_id = None
            msg = f"Unable to get SLURM job ID: {err.args[0]}"
            logger.warning(msg)

        if not stats_file.exists() and job_id is not None:
            try:
                stats_file = create_job_stats_file(
                    slurm_job_id=job_id, job_dir=dir_name
                )
            except RuntimeError as err:
                msg = f"Unable to create job stats file: {err.args[0]}"
                logger.warning(msg)

        try:
            job_stats.update(parsing.parse_job_stats_file(stats_file))
        except (FileNotFoundError, IndexError, ValueError) as err:
            msg = f"Unable to parse job stats file: {err.args[0]}"
            logger.warning(msg)

        try:
            slurm_file = find_slurm_file(dir_name=dir_name)
            error = parsing.parse_job_error(slurm_file=slurm_file)
            job_stats["error"] = str(error) if error else None
        except FileNotFoundError as err:
            msg = f"Unable to parse job error: {err.args[0]}"
            logger.warning(msg)

        scheduler_outputs = SchedulerOutputs(**job_stats)

        logger.debug(f"Successfully loaded scheduler outputs from {dir_name}")
        return scheduler_outputs


ARC_PARTITIONS = (
    Partition.BIGMEM,
    Partition.CPU2017_BF05,
    Partition.CPU2019,
    Partition.CPU2019_BF05,
    Partition.CPU2021,
    Partition.CPU2021_BF24,
    Partition.CPU2022,
    Partition.CPU2022_BF24,
    Partition.GPU_V100,
    Partition.LATTICE,
    Partition.PARALLEL,
    Partition.RAZI,
    Partition.SINGLE,
)

ARBUTUS = Cluster(
    "arbutus", "University of Victoria", "Digital Research Alliance"
)
ARC = Cluster("arc", "University of Calgary", partitions=ARC_PARTITIONS)
BELUGA = Cluster("beluga", "McGill University", "Digital Research Alliance")
CEDAR = Cluster(
    "cedar", "Simon Fraser University", "Digital Research Alliance"
)
GRAHAM = Cluster(
    "graham", "University of Waterloo", "Digital Research Alliance"
)
NARVAL = Cluster("narval", "McGill University", "Digital Research Alliance")
NIAGARA = Cluster(
    "arbutus", "University of Toronto", "Digital Research Alliance"
)

DRA = (ARBUTUS, BELUGA, CEDAR, GRAHAM, NARVAL, NIAGARA)
