"""Represent and model the results of a task."""

from datetime import datetime
from enum import StrEnum
from enum import unique
import importlib
import json
import logging
import pathlib
from pathlib import Path
import re
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import TextIO
from uuid import UUID
from uuid import uuid4
import warnings

from ase import Atoms
from ase.calculators.calculator import PropertyNotImplementedError
import ase.io
from pydantic import UUID4
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import ImportString
from pydantic import PrivateAttr
from pydantic import SerializationInfo
from pydantic import ValidationError
from pydantic import ValidationInfo
from pydantic import ValidatorFunctionWrapHandler
from pydantic import field_serializer
from pydantic import field_validator
from pydantic import model_validator
from pymatgen.entries.computed_entries import ComputedEntry

from autojob import SETTINGS
from autojob import hpc
from autojob.calculation.parameters import CalculatorType
from autojob.coordinator.classification import CalculationType
from autojob.study import StudyType
from autojob.utils.files import extract_structure_name
from autojob.utils.files import get_uri
from autojob.utils.schemas import PydanticAtoms

if TYPE_CHECKING:
    from pydantic.main import IncEx

logger = logging.getLogger(__name__)

LEGACY_TASK_ID_LENGTH = 10


@unique
class TaskOutcome(StrEnum):
    """The state of a task."""

    SUCCESS = "successful"
    FAILED = "failed"
    ERROR = "error"
    RUNNING = "running"
    IDLE = "idle"


class TaskMetadata(BaseModel):
    """The metadata for a task."""

    model_config = ConfigDict(populate_by_name=True)

    label: str = Field(
        default="", description="A description of the job", alias="Name"
    )
    tags: list[str] = Field(
        default=[],
        title="tag",
        description="Metadata tagged to a given job",
        alias="Notes",
    )
    uri: str | None = Field(
        default=None,
        description="The uri for the directory containing this task",
    )
    study_group_id: UUID4 | str | None = Field(
        default=None,
        description="The study group uuid",
        alias="Study Group ID",
        union_mode="left_to_right",
    )
    study_id: UUID4 | str | None = Field(
        default=None,
        description="The study uuid",
        alias="Study ID",
        union_mode="left_to_right",
    )
    workflow_step_id: UUID4 | None = Field(
        default=None, description="The workflow step uuid"
    )
    task_id: UUID4 | str = Field(
        default=uuid4(),
        description="The task uuid",
        alias="Job ID",
        union_mode="left_to_right",
    )
    calculation_id: str | None = Field(
        default=None,
        description="The Calculation uuid (for backwards-compatibility)",
        alias="Calculation ID",
    )
    calculation_type: CalculationType | None = Field(
        default=None,
        description="The Calculation type (for backwards-compatibility)",
        alias="Calculation Type",
    )
    calculator_type: CalculatorType | None = Field(
        default=None,
        description="The Calculator type (for backwards-compatibility)",
        alias="Calculator Type",
    )
    study_type: StudyType | None = Field(
        default=None,
        description="The study type (for backwards-compatibility)",
        alias="Study Type",
    )
    last_updated: datetime | None = Field(
        default=None,
        description="Timestamp for the most recent calculation for this task "
        "document",
    )

    # A special key used to determine how to instantiate subclasses.
    _build_class: ImportString["Task"] | None = PrivateAttr(
        None,
    )

    @model_validator(mode="after")
    def add_build_class(self) -> "TaskMetadata":
        """Add a build class to a constructed TaskMetadata object.

        Note that this is step is for backwards-compatibility with Tasks
        created with `calculation_type` set and will be removed in future
        releases. `_build_class` can be set directly during
        instantiation.

        .. deprecated: 0.12.0
        """
        if self.calculation_type and not self._build_class:
            match self.calculation_type:
                case CalculationType.RELAXATION:
                    builder = "calculation"
                case CalculationType.VIB:
                    builder = "vibration"
                case _:
                    warnings.warn(
                        "No build class conversion defined for "
                        "calculation type {self.calculation_type!s}. The "
                        "default, Calculation, will be used.",
                        stacklevel=2,
                    )
                    builder = "calculation"

            module = importlib.import_module(f"autojob.calculation.{builder}")
            self._build_class = getattr(module, builder.capitalize())

        return self

    @field_validator("study_group_id", "study_id", "task_id", mode="wrap")
    @classmethod
    def validate_ids(
        cls,
        v: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo,  # noqa: ARG003
    ) -> str | UUID4:
        """Validate an ID."""
        value = v
        try:
            value = handler(v)
            if isinstance(value, UUID):
                return value
        except ValidationError:
            pass

        if (
            isinstance(value, str)
            and len(value) == LEGACY_TASK_ID_LENGTH
            and v.isalnum()
        ):
            return value

        msg = f"{v} is not a UUID4 or a 10-digit alphanumeric shortuuid string"
        raise ValueError(msg)

    @field_validator("tags", mode="wrap")
    @classmethod
    def validate_tags(
        cls,
        v: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo,  # noqa: ARG003
    ) -> list[str]:
        """Validate job notes/tags."""
        try:
            tags: list[str] = handler(v)
            return tags
        except ValidationError:
            return [x.strip() for x in str(v).split(";")] if v else []

    @field_serializer(
        "study_group_id",
        "study_id",
        "task_id",
        "workflow_step_id",
        mode="plain",
    )
    @staticmethod
    def serialize_ids(
        v: Any,
        info: SerializationInfo,  # noqa: ARG004
    ) -> str | None:
        """Serialize IDs."""
        return v if v is None else str(v)

    @field_serializer(
        "last_updated",
        mode="plain",
    )
    @staticmethod
    def serialize_last_updated(
        v: Any,
        info: SerializationInfo,  # noqa: ARG004
    ) -> str | None:
        """Serialize the last updated time."""
        return v if v is None else str(v)

    @field_serializer(
        "calculation_type",
        "calculator_type",
        "study_type",
        mode="plain",
    )
    @staticmethod
    def serialize_types(
        v: Any,
        info: SerializationInfo,  # noqa: ARG004
    ) -> str:
        """Serialize ``autojob`` types."""
        return str(v)

    @field_serializer(
        "tags",
        mode="plain",
        when_used="json",
    )
    @staticmethod
    def serialize_tags(v: Any, info: SerializationInfo) -> str:  # noqa: ARG004
        """Serialize tags."""
        return "; ".join(v)

    @classmethod
    def from_directory(cls, dir_name: str | pathlib.Path) -> "TaskMetadata":
        """Create a TaskMetadata document from a task directory."""
        logger.debug(f"Loading task metadata from {dir_name}")

        task_file = pathlib.Path(dir_name).joinpath(SETTINGS.JOB_FILE)
        with task_file.open(mode="r", encoding="utf-8") as file:
            raw_metadata: dict[str, Any] = json.load(file)

        raw_metadata["uri"] = get_uri(dir_name=dir_name)

        logger.debug(f"Successfully loaded task metadata from {dir_name}")
        return cls(**raw_metadata)


class _TaskIODoc(BaseModel):
    """A base class for task input/output documents."""

    atoms: PydanticAtoms | None = Field(
        default=None, description="Input or output ase.Atoms"
    )


class TaskInputs(_TaskIODoc):
    """The set of task-level inputs."""

    files_to_copy: list[str] = Field(
        default=[],
        description="The files to copy from the preceding task into the "
        "directory of this task.",
    )
    files_to_delete: list[str] = Field(
        default=[],
        description="The files to delete from the directory of the task after "
        "job completion.",
    )
    files_to_carry_over: list[str] = Field(
        default=[],
        description="The files to carry over from the completed task to the "
        "new job.",
    )
    auto_restart: bool = Field(
        default=True,
        description="Whether or not to automatically restart this calculation "
        "with the same parameters if the task finishes unsuccessfully.",
    )

    model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

    # TODO: use SETTINGS.SLURM_SCRIPT
    @classmethod
    def from_directory(cls, dir_name: str | pathlib.Path) -> "TaskInputs":
        """Generate a TaskInputs document from a completed task's directory.

        Note that this method retrieves task inputs from the first .sh file
        in the `dir_name` returned by `Path.rglob`.

        Args:
            dir_name: The directory of a completed Task.

        Returns:
            A TaskInputs object.
        """
        logger.debug(f"Loading task inputs from {dir_name}")
        logger.warning(
            "Note that it is currently not possible to retrieve the "
            "`files_to_carryover` attribute from the directory of a completed "
            "Task. Currently, `files_to_carryover` is set in "
            "`Calculation.from_directory`."
        )

        try:
            # ! IMPROVE: Beware of nested directories!
            slurm_script = next(Path(dir_name).rglob("*.sh"))
        except StopIteration as err:
            msg = (
                f"Unable to find job submission script for task in {dir_name}"
            )
            raise FileNotFoundError(msg) from err

        with slurm_script.open(mode="r", encoding="utf-8") as file:
            lines = file.readlines()

        files_to_copy = TaskInputs.extract_files_to_copy(stream=lines)
        files_to_delete = TaskInputs.extract_files_to_delete(stream=lines)
        auto_restart = TaskInputs.check_auto_restart(stream=lines)
        atoms = TaskInputs.get_input_atoms(dir_name=dir_name)

        logger.debug(f"Successfully loaded task inputs from {dir_name}")

        return cls(
            atoms=atoms,
            files_to_copy=files_to_copy,
            files_to_delete=files_to_delete,
            auto_restart=auto_restart,
        )

    @staticmethod
    def extract_files_to_copy(stream: TextIO | list[str]) -> list[str]:
        """Parse the slurm submission script for the calculation files to copy.

        This method will parse the files to copy when they are listed in
        legacy format (i.e., without assignment to a variable) or if they are
        assigned to a variable named AUTOJOB_FILES_TO_COPY.

        Args:
            stream: A TextIO or list of strings containing the text in the
                slurm submission script.

        Returns:
            A list of the strings passed as calculation files to copy.
        """
        log_addendum = ""

        if hasattr(stream, "name") and hasattr(stream, "tell"):
            offset = stream.tell()
            log_addendum = f" from {stream.name}"

        logger.debug(f"Extracting files to copy{log_addendum}")
        env_var_re = re.compile(r'AUTOJOB_FILES_TO_COPY="(?P<files>.*)"')
        legacy_delete_re = re.compile(
            r'cp -v "\$SLURM_SUBMIT_DIR"/\{(?P<files>\S+)\}'
        )
        files: list[str] = []

        for line in stream:
            match1 = env_var_re.match(line)
            match2 = legacy_delete_re.match(line)
            if match1:
                files = match1.group("files").split(",")
                break
            elif match2:
                files = match2.group("files").split(",")
                break

        if hasattr(stream, "seek"):
            stream.seek(offset)

        logger.debug(
            f"Successfully extracted files to copy{log_addendum}\n"
            f"Files: {files!r}"
        )
        return files

    @staticmethod
    def extract_files_to_delete(stream: TextIO | list[str]) -> list[str]:
        """Parse the slurm submission script for the deleted calculation files.

        This method will parse the files to delete when they are listed in
        legacy format (i.e., without assignment to a variable) or if they are
        assigned to a variable named AUTOJOB_FILES_TO_DELETE.

        Args:
            stream: A TextIO or list of strings containing the text in the
                slurm submission script.

        Returns:
            A list of the strings passed as calculation files to delete.
        """
        log_addendum = ""

        if hasattr(stream, "name") and hasattr(stream, "tell"):
            offset = stream.tell()
            log_addendum = f" from {stream.name}"

        logger.debug(f"Extracting files to delete{log_addendum}")
        env_var_re = re.compile(r'AUTOJOB_FILES_TO_DELETE="(?P<files>.*)"')
        file_delete_start_re = re.compile(r"^rm -vf (?P<files>[^\\]*)(.*)?$")
        listing_files = False

        files: list[str] = []

        for line in stream:
            match1 = env_var_re.match(line)
            match2 = file_delete_start_re.match(line)
            if match1:
                files.extend(match1.group("files").split())
                break
            elif match2:
                listing_files = True
                files.extend(match2.group("files").split())
            elif not line.startswith("sleep 10") and listing_files:
                files.extend(line.rstrip("\\ \n").split())
            elif listing_files:
                break

        if hasattr(stream, "seek"):
            stream.seek(offset)

        logger.debug(
            f"Successfully extracted files to delete{log_addendum}\n"
            f"Files: {files!r}"
        )
        return files

    @staticmethod
    def check_auto_restart(stream: TextIO | list[str]) -> bool:
        """Determines if auto-restart was enabled during job submission.

        Args:
            stream: A TextIO or list[str] containing the lines of the slurm job
                submission script.

        Returns:
            Whether or not auto-restart was enabled during job submission.
        """
        log_addendum = ""

        if hasattr(stream, "name") and hasattr(stream, "tell"):
            offset = stream.tell()
            log_addendum = f" in {stream.name}"

        logger.debug(f"Checking if auto-restart enabled{log_addendum}")

        auto_restart_enabled = False

        conditional_re = re.compile(
            r"^if \[(\[)? \$restart = true (\])?\]; then$"
        )
        advance_re = re.compile(r"^autojob advance")

        for line in stream:
            if conditional_re.match(line) or advance_re.match(line):
                auto_restart_enabled = True
                break

        if hasattr(stream, "seek"):
            stream.seek(offset)

        adverb = "" if auto_restart_enabled else " not"
        logger.debug(f"Auto-restart was{adverb} enabled{log_addendum}")
        return auto_restart_enabled

    @staticmethod
    def get_input_atoms(dir_name: str | pathlib.Path) -> Atoms:
        """Retrieve an Atoms object representing the input structure.

        Note that the filename used to identify the structure file is saved to
        :attr:`Atoms.info` under the `"structure"` key.

        Args:
            dir_name: the directory containing the completed calculation

        Returns:
            An Atoms object.
        """
        dir_name = Path(dir_name)
        logger.debug(f"Retrieving input atoms from {dir_name}")

        with dir_name.joinpath(SETTINGS.PYTHON_SCRIPT).open(
            mode="r", encoding="utf-8"
        ) as file:
            filename = extract_structure_name(file)

        atoms = ase.io.read(dir_name.joinpath(filename))
        if "structure" not in atoms.info:
            atoms.info["structure"] = Path(filename).stem.removeprefix("./")
        logger.debug(f"Successfully retrieved input atoms from {dir_name}")
        return atoms


class TaskOutputs(_TaskIODoc):
    """The set of task-level outputs."""

    entry: ComputedEntry | None = Field(
        default=None, description="The ComputedEntry from the task"
    )
    outcome: TaskOutcome = Field(
        TaskOutcome.IDLE, description="The outcome of the task"
    )

    @classmethod
    def from_directory(
        cls,
        dir_name: str | pathlib.Path,
        *,
        strict_mode: bool = SETTINGS.STRICT_MODE,
    ) -> "TaskOutputs":
        """Generate a TaskOutputs document from a completed task's directory.

        Note that the `atoms` object may not be set if the task is incomplete.
        In such a case, one may need to use a task-specific `get_output_atoms`
        function (i.e., `Calculation.get_output_atoms`)

        Args:
            dir_name: The directory of a completed Task.
            strict_mode: Whether or not to catch thrown errors. Errors will be
                thrown if ``strict_mode=True``.

        Returns:
            A TaskOutputs object.
        """
        dir_name = pathlib.Path(dir_name)
        logger.debug(f"Loading task outputs from {dir_name}")
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")
        outputs = {
            "atoms": TaskOutputs.get_output_atoms(
                dir_name=dir_name, strict_mode=strict_mode
            )
        }

        # TODO: Change this to an external call to the scheduler executable
        # TODO: e.g., sacct -j XXXXXXXX | grep ...
        if dir_name.joinpath("scratch_dir").exists():
            outputs["outcome"] = TaskOutcome.RUNNING

        logger.debug(f"Successfully loaded task outputs from {dir_name}")

        return cls(**outputs)

    @staticmethod
    def get_output_atoms(
        dir_name: str | pathlib.Path,
        *,
        strict_mode: bool = SETTINGS.STRICT_MODE,
    ) -> Atoms | None:
        """Retrieve an Atoms object representing the output structure.

        Args:
            dir_name: The directory from which to retrieve the output
                structure.
            strict_mode: Whether or not to raise an error if reading the output
                atoms file fails. Defaults to True.

        Returns:
            An Atoms object representing the output structure or None if no
            Atoms object can be retrieved.
        """
        structure = pathlib.Path(dir_name).joinpath(SETTINGS.OUTPUT_ATOMS)

        logger.debug(f"Retrieving output atoms from {structure}")
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")
        atoms: Atoms | None = None

        try:
            atoms = ase.io.read(structure, index=-1)
            logger.debug(
                f"Successfully retrieved output atoms from {structure}"
            )
        except (FileNotFoundError, AttributeError):
            if strict_mode:
                raise

            msg = (
                f"Unable to retrieve atoms from: {structure}.\n"
                "File not found."
            )
            logger.warning(msg)

        return atoms


# TODO 1: Write Task.serialize to add @class and @module keys which can be used
# TODO 1: in place of CalculationType
class Task(BaseModel):
    """Represent the result of a task."""

    task_metadata: TaskMetadata
    task_inputs: TaskInputs = Field(description="Task inputs")
    task_outputs: TaskOutputs | None = Field(
        default=None, description="Task outputs"
    )

    model_config = ConfigDict(extra="allow")

    @classmethod
    def load_magic(
        cls,
        dir_name: str | Path,
        *,
        strict_mode: bool = True,
    ) -> "Task":
        """Magically load the contents of a directory as a ``Task`` subclass.

        Args:
            dir_name: The directory from which to load the task.
            strict_mode: Whether to raise errors thrown due to missing outputs
                Defaults to True in which case errors will be thrown.

        Raises:
            RuntimeError: No build class specified in the task metadata. Only
                raised if ``strict_mode`` is True.

        Returns:
            The loaded Task.
        """
        logger.debug("Magic mode enabled")
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")
        metadata = TaskMetadata.from_directory(dir_name)

        if metadata._build_class:
            return metadata._build_class.from_directory(
                dir_name, strict_mode=strict_mode
            )
        elif strict_mode:
            msg = (
                f"No build class provided for task in {dir_name!s}. "
                "Unable to use magic mode"
            )
            raise RuntimeError(msg)
        else:
            msg = (
                "No build class provided for task in %s. Unable to "
                "use magic mode, so a %s will be created instead."
            )
            logger.warning(msg, dir_name, cls.__name__)

        return cls.from_directory(dir_name=dir_name, strict_mode=strict_mode)

    @classmethod
    def from_directory(
        cls,
        dir_name: str | pathlib.Path,
        *,
        strict_mode: bool = SETTINGS.STRICT_MODE,
        magic_mode: bool = False,
    ) -> "Task":
        """Generate a Task document from a completed task's directory.

        Args:
            dir_name: The directory of a completed Task.
            strict_mode: Whether or not to require all outputs. If True,
                errors will be thrown on missing outputs.
            magic_mode: Whether to defer the final object creation. If True,
                the final object will be an instance of the class specified
                by the `_build_class` attribute of the :class:`TaskMetadata`
                object created. Otherwise, a :class:`Task` object will be
                returned. Defaults to False.

        Returns:
            A Task object.

        Note:
            The class indicated by `_build_class` should be a subclass of the
            class from which this method is called as successive steps may
            expect attributes and methods of the calling class to be present.
        """
        logger.debug(f"Loading task from {dir_name}")
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")
        metadata = TaskMetadata.from_directory(dir_name=dir_name)

        if magic_mode:
            return cls.load_magic(dir_name=dir_name, strict_mode=strict_mode)

        inputs = TaskInputs.from_directory(dir_name=dir_name)
        outputs = TaskOutputs.from_directory(
            dir_name=dir_name, strict_mode=strict_mode
        )
        new_task = cls(
            task_metadata=metadata, task_inputs=inputs, task_outputs=outputs
        )
        logger.debug(f"Successfully loaded task from {dir_name}")

        return new_task

    @staticmethod
    def create_shell(context: dict[str, Any] | None = None) -> "Task":
        """Recursively create a minimal Task, a shell, for writing inputs.

        Args:
            context: A dictionary mapping strings to Task attributes that will
                be used to populate the shell. Defaults to an empty dictionary.

        Returns:
            The minimal Task.
        """
        context = context or {}
        return Task(
            task_metadata=context.get("task_metadata", TaskMetadata()),
            task_inputs=context.get("task_inputs", TaskInputs()),
        )

    def to_directory(
        self,
        dst: str | pathlib.Path,
        *,
        structure_name: str = SETTINGS.INPUT_ATOMS,
        legacy_mode: bool = False,
    ) -> None:
        """Dump the results of a task to a directory.

        Args:
            dst: The directory in which to save the task results.
            structure_name: The name of the structure file to save.
            legacy_mode: Whether or not to use the legacy mode.
        """
        logger.debug(f"Dumping Task to {dst}")

        if self.task_inputs.atoms:
            # TODO: Replace with a call to write_inputs(_atoms)?
            self.task_inputs.atoms.write(dst.joinpath(structure_name))

        filename = pathlib.Path(dst).joinpath(
            SETTINGS.JOB_FILE if legacy_mode else SETTINGS.TASK_FILE
        )

        if legacy_mode:
            exclude: IncEx = [
                "workflow_step_id",
                "uri",
                "last_updated",
            ]
        else:
            exclude = [
                "calculation_id",
                "calculator_type",
                "last_updated",
            ]

        model = self.task_metadata.model_dump(
            exclude=exclude,
            by_alias=True,
            exclude_none=not legacy_mode,
            mode="json",
        )

        with filename.open(mode="w", encoding="utf-8") as file:
            json.dump(model, file, indent=4)

        logger.debug(f"Successfully dumped Task to {dst}")

    def patch_task(
        self,
        *,
        output_atoms: Atoms,
        converged: bool,
        error: hpc.SchedulerError | None,
        files_to_carry_over: list[str],
        strict_mode: bool = SETTINGS.STRICT_MODE,
    ) -> None:
        """Patch Task attributes using Calculation values.

        Note that this method modifies the Task in place. The following
        attributes are patched:

        - `Task.task_outputs.atoms`: replaced with `output_atoms`
        - `Task.task_inputs.files_to_carryover`: replaced with
          `files_to_carry_over`
        - `Task.task_outputs.outcome`: set according to `converged` and `error`

        Args:
            dir_name: The directory from which to source values.
            output_atoms: An Atoms object representing the output geometry.
            converged: Whether the Calculation is converged.
            error: The hpc.SchedulerError from the calculation.
            files_to_carry_over: The files to carry over from the previous
                calculation.
            strict_mode: Whether to raise an error if no output atoms found.
                Defaults to True.
        """
        if self.task_outputs is None:
            if strict_mode:
                msg = (
                    "Patching incomplete Tasks is not supported in strict_mode"
                )
                raise RuntimeError(msg)

            logger.info(
                "No task outputs to patch in task %s",
                self.task_metadata.task_id,
            )
            return None

        if self.task_outputs.atoms is None:
            logger.debug("Patching output atoms")
            self.task_outputs.atoms = output_atoms

        if not self.task_inputs.files_to_carry_over:
            logger.debug(
                f"Patching files to carryover: {files_to_carry_over!r}"
            )
            self.task_inputs.files_to_carry_over = files_to_carry_over

        if converged:
            self.task_outputs.outcome = TaskOutcome.SUCCESS
        elif error is not None:
            self.task_outputs.outcome = TaskOutcome.ERROR

    def prepare_input_atoms(self) -> None:
        """Copy the final magnetic moments to initial magnetic moments.

        This function modifies atoms in place. Note that if atoms were obtained
        from a vasprun.xml via ase.io.read("vasprun.xml"), no magnetic moments
        will be read. In order to ensure continuity between runs, it is a good
        idea to retain the WAVECAR between runs.
        """
        logger.debug("Preparing atoms for next run.")
        try:
            self.task_inputs.atoms.set_initial_magnetic_moments(
                self.task_inputs.atoms.get_magnetic_moments()
            )
            logger.debug("Copied magnetic moments to initial magnetic moments")
        except (PropertyNotImplementedError, RuntimeError):
            logger.info(
                "No magnetic moments to copy found. Using the initial "
                "magnetic moments: "
                f"{self.task_inputs.atoms.get_initial_magnetic_moments()!r}"
            )

    # TODO: This should be called in Task.to_directory
    def write_inputs(
        self,
        dir_name: str | pathlib.Path,
        *,
        input_atoms: str | pathlib.Path | None = None,
    ) -> list[pathlib.Path]:
        """Write the required inputs for a Task to a directory.

        Args:
            dir_name: The directory in which to write the inputs.
            input_atoms: The filename to use for saving the input atoms.
                Defaults to SETTINGS.INPUT_ATOMS.

        Returns:
            A list of Path objects where each Path represents the filename of
            an input written to `dir_name`.
        """
        logger.debug(f"Writing {__class__} inputs to {dir_name}")
        inputs = []
        if self.task_inputs.atoms:
            atoms_filename = self.task_inputs.atoms.info.get("filename", None)
            input_atoms = (
                atoms_filename
                if isinstance(atoms_filename, str | pathlib.Path)
                else SETTINGS.INPUT_ATOMS
            )
            filename = pathlib.Path(dir_name).joinpath(input_atoms)
            self.task_inputs.atoms.write(filename)
            inputs = [filename]
        logger.debug(
            f"Successfully wrote {__class__} inputs to {dir_name}: {inputs!r}"
        )
        return inputs


Task.model_rebuild()
