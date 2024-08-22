"""Store the results of a calculation.

This module defines the :class:`.autojob.calculation.calculation.Calculation`,
:class:`.autojob.calculation.calculation.CalculationInputs`, and
:class:`.autojob.calculation.calculation.CalculationOutputs` classes. Instances
of these classes represent the results of a calculation, its inputs, and its
outputs, respectively.

For building the respective documents from a folder, each class exposes a
``from_directory()`` method.

Example:
    .. code-block:: python

        from autojob.calculation.calculation import Calculation

        dir_name = "path/to/calculation/directory"
        results = Calculation.from_directory(dir_name)
"""

from __future__ import annotations

import ast
from collections.abc import Sequence
from contextlib import suppress
import importlib
import logging
import pathlib
from typing import Any
from typing import ClassVar
from typing import Literal
from typing import TextIO
from typing import overload
import warnings
from xml.etree import ElementTree

from ase import Atoms
from ase.calculators.calculator import PropertyNotImplementedError
import ase.io
import jinja2
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import ImportString
from pydantic import TypeAdapter
from pydantic import field_validator
from pymatgen.command_line.bader_caller import bader_analysis_from_path
from pymatgen.command_line.chargemol_caller import ChargemolAnalysis
from pymatgen.io.vasp import Kpoints

from autojob import SETTINGS
from autojob import hpc
from autojob.calculation import gaussian
from autojob.calculation.parameters import CalculatorType
from autojob.calculation.vasp import vasp
from autojob.coordinator.scripter import Scripter
from autojob.schemas import BaderAnalysis
from autojob.schemas import DDEC6Analysis
from autojob.task import Task
from autojob.utils.files import extract_structure_name
from autojob.utils.parsing import extract_keyword_arguments

logger = logging.getLogger(__name__)

FILES_TO_COPY = [
    "CHGCAR",
    "*py",
    "*cif",
    "POSCAR",
    "coord",
    "*xyz",
    "*.traj",
    "CONTCAR",
    "*.pkl",
    "*xml",
    "WAVECAR",
    "*.com",
    "*.chk",
]
FILES_TO_DELETE = [
    "*.d2e",
    "*.int",
    "*.rwf",
    "*.skr",
    "*.inp",
    "EIGENVAL",
    "IBZKPT",
    "PCDAT",
    "PROCAR",
    "ELFCAR",
    "LOCPOT",
    "PROOUT",
    "TMPCAR",
    "vasp.dipcor",
]


class Pseudopotential(BaseModel):
    """A pseudopotential."""

    pot_type: str | None = Field(
        default=None,
        description="Pseudo-potential type, e.g. PAW",
    )
    functional: str | None = Field(
        default=None,
        description="Functional type use in the calculation.",
    )
    symbols: list[str] | None = Field(
        default=None,
        description="List of VASP potcar symbols used in the calculation.",
    )


class Analysis(BaseModel):
    """Analysis from a calculation."""

    delta_volume: float | None = Field(
        default=None,
        title="Volume Change",
        description="Volume change for the calculation.",
    )
    delta_volume_percent: float | None = Field(
        default=None,
        title="Volume Change Percent",
        description="Percent volume change for the calculation.",
    )
    max_force: float | None = Field(
        default=None,
        title="Max Force",
        description="Maximum force on any atom at the end of the calculation.",
    )
    warnings: list[str] | None = Field(
        default=None,
        title="Calculation Warnings",
        description="Warnings issued after analysis.",
    )
    errors: list[str] | None = Field(
        default=None,
        title="Calculation Errors",
        description="Errors issued after analysis.",
    )


class CalculationInputs(BaseModel):
    """The inputs for the calculation."""

    ase_calculator: ImportString = Field(
        default="ase.calculators.vasp.Vasp",
        description="The ASE Calculator used to perform this calculation",
    )
    # TODO: implement & add to validator
    # ase_optimizer: ImportString | None = Field(
    #     default="ase.optimize.bfgs.BFGS",  # or None
    #     description="The ASE optimizer used to perform this calculation"
    #         "None defaults to the internal calculator.",
    # )
    parameters: dict[str, Any] = Field(
        default={},
        description="The parameters used to configure the ASE calculator",
    )
    kpoints: Kpoints | Sequence[int] | None = Field(
        default=None,
        description="Pymatgen object representing the KPOINTS file",
    )
    xc_override: str | None = Field(
        default=None,
        description="Exchange-correlation functional used if not the default",
    )
    is_lasph: bool | None = Field(
        default=None,
        description="Whether the calculation was run with aspherical "
        "corrections",
    )
    is_hubbard: bool = Field(
        default=False,
        description="Is this a Hubbard+U calculation",
    )
    hubbards: dict[str, Any] | None = Field(
        default=None,
        description="The hubbard parameters used",
    )
    pseudopotentials: Pseudopotential | None = Field(
        default=None,
        description="Summary of the pseudopotentials used in this calculation",
    )
    calculation_objects: dict[str, Any] | None = Field(
        default=None,
        description="Calculation objects provided as inputs to this "
        "calculation",
    )
    # ! Add check for `laechg` in write_python_script
    run_bader: bool = Field(
        default=False,
        description="Whether or not to run Bader charge analysis",
    )
    run_chargemol: bool = Field(
        default=False,
        description="Whether or not to run Chargemol charge analysis",
    )

    model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

    # TODO: bolster validator
    @field_validator("ase_calculator", mode="before")
    @classmethod
    def validate_ase_class(cls, v: Any) -> Any:
        """Validate an instance of :class:`.calculator.Calculator`.

        Args:
            v: A value to be validated.

        Raises:
            ValueError: Unable to validate the value.

        Returns:
            _description_
        """
        logger.debug(f"Validating {v}")
        if isinstance(v, str):
            try:
                fully_qual_class = v.split(".")
                module_name = ".".join(fully_qual_class[:-1])
                calc_cls = fully_qual_class[-1]
                mod = importlib.import_module(name=module_name)
                calc = getattr(mod, calc_cls)
                logger.debug(f"Successfully validated {v} as {calc!s}")
                return calc
            except (AttributeError, ImportError, IndexError) as err:
                logger.warning(f"Unable to validate {v} due to {err!r}")
                raise ValueError(err.args[0]) from err
        logger.debug(f"Successfully validated {v}")
        return v

    @staticmethod
    def extract_imported_ase_calculators(
        stream: TextIO,
    ) -> list[tuple[str, str | None]]:
        """Determine which ASE calculators a script imports.

        Args:
            stream: A TextIO containing the script.

        Returns:
            A list of strings tuples (``calculator``, ``alias``) where
            ``calculator`` and ``alias`` are the class and alias ("as name")
            of an imported ASE calculator, respectively.

        Warning:
            This is only tests for imports of the sort:

            .. code-block:: python

                from ase.calculator.module import Calculator

            or

            .. code-block:: python

                import ase.calculator.module.Calculator as Calculator

            It has not expected to behave well when the calculator is imported
            like:

            .. code-block:: python

                import ase.calculator.module.Calculator
        """
        logger.debug(f"Extracting imported ASE calculators from {stream.name}")
        offset = stream.tell()

        # parse with ast
        code = ast.parse(stream.read(), filename=stream.name)

        imported_ase_calculators: list[tuple[str, str | None]] = []

        for node in ast.walk(code):
            if isinstance(node, ast.Import):
                for name in node.names:
                    if name.name.startswith("ase.calculators"):
                        imported_ase_calculators.append(
                            ((name.asname or name.name), None)
                        )
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module is not None
                and node.module.startswith("ase.calculators")
            ):
                imported_ase_calculators.extend(
                    (x.name, x.asname) for x in node.names
                )

        _ = stream.seek(offset)
        logger.debug(
            "Successfully extracted imported ASE calculators from "
            f"{stream.name}"
        )
        return imported_ase_calculators

    @staticmethod
    def extract_calculation_parameters(
        stream: TextIO,
    ) -> tuple[list[Any], dict[str, Any]]:
        """Extract parameters used to configure ASE calculator.

        All imports with ASE calculators must use fully qualified module
        names. All calculator configuration arguments must be passed by keyword
        in order to be recognized.

        Args:
            stream: a TextIO containing the lines of code.

        Raises:
            RuntimeError: Unable to extract calculation parameters.

        Returns:
            A list and dictionary. This list contains positional arguments
            used to configure the calculator while the dictionary maps
            calculator parameters to their values.
        """
        logger.debug(f"Extracting calculation parameters from {stream.name}")
        offset = stream.tell()

        imported_ase_calculators = (
            CalculationInputs.extract_imported_ase_calculators(stream=stream)
        )
        calculator_in_use, calculator_alias = imported_ase_calculators[0]
        calculator_alias = calculator_alias or calculator_in_use

        # Find assign statement where value is Call matching first element
        # of above
        args = keywords = None

        # parse with ast
        code = ast.parse(stream.read(), filename=stream.name)

        for node in ast.walk(code):
            # Find a function call matching the calculator name
            if (
                (value := getattr(node, "value", False))
                # Only ast.Call nodes have func attributes
                and (func := getattr(value, "func", False))
                and (getattr(func, "id", None) == calculator_alias)
            ):
                args = [ast.unparse(x) for x in value.args]  # type: ignore[union-attr]
                keywords = extract_keyword_arguments(
                    keywords=value.keywords,  # type: ignore[union-attr]
                    code=code,
                )

        if args is None or keywords is None:
            msg = (
                f"Unable to extract calculation parameters from {stream.name}"
            )
            raise RuntimeError(msg)

        keywords["calculator"] = CalculatorType(calculator_in_use.lower())

        _ = stream.seek(offset)
        logger.debug(
            f"Successfully extracted calculation parameters from "
            f"{stream.name}: args: {args}, kwargs: {keywords}"
        )
        return args, keywords

    @classmethod
    def from_directory(
        cls,
        *,
        dir_name: str | pathlib.Path,
        calculator_type: CalculatorType | None = None,
    ) -> CalculationInputs:
        """Generate a CalculationInputs document from a calculation's directory.

        Args:
            dir_name: The directory of a calculation.
            calculator_type: The calculator type. Must correspond to an ASE
                calculator

        Returns:
            A CalculationInputs object with the calculator parameters and ASE
            calculator used to perform the calculation.
        """
        logger.debug(f"Loading calculation inputs from {dir_name}")
        python_script = pathlib.Path(dir_name).joinpath(SETTINGS.PYTHON_SCRIPT)

        with python_script.open(mode="r", encoding="utf-8") as file:
            # map _ to posargs using inspect
            _, parameters = CalculationInputs.extract_calculation_parameters(
                file
            )

        calculator = str(parameters.pop("calculator"))
        if calculator_type:
            ase_calculator = (
                f"ase.calculators.{str(calculator_type).lower()}."
                f"{str(calculator_type).capitalize()}"
            )
        else:
            ase_calculator = (
                f"ase.calculators.{calculator.lower()}."
                f"{calculator.capitalize()}"
            )

        calculation_inputs = cls(
            ase_calculator=ase_calculator, parameters=parameters
        )

        logger.debug(f"Successfully loaded calculation inputs from {dir_name}")
        return calculation_inputs

    def check_inputs(self) -> list[str]:
        """Verify the input parameters."""
        msgs = []
        if self.run_bader:
            msgs + check_bader(self.parameters)
        return msgs


def check_bader(parameters: dict[str, Any]) -> list[str]:
    """Peform parameter checks for Bader analysis."""
    msgs = []

    for kw in ["laechg", "lcharg"]:
        if not parameters.get(kw, False):
            msgs.append(
                f"{kw.upper()} is not to True but `run_bader` is True. "
                f"Bader analysis requires {kw.upper()} to be True"
            )

    if parameters.get("nsw", 0):
        msgs.append(
            "NSW is non-zero but `run_bader` is True. "
            "Bader analysis requires NSW to be zero."
        )
    return msgs


class CalculationOutputs(BaseModel):
    """The outputs of a calculation."""

    density: float | None = Field(
        default=None, description="Density of in units of g/cc."
    )
    energy: float | None = Field(
        default=None,
        description="Total Energy in units of eV.",
    )
    forces: list[list[float]] | None = Field(
        default=None,
        description="The force on each atom in units of eV/Å.",
    )
    stress: list[list[float]] | None = Field(
        default=None,
        description="The stress on the cell in units of kB.",
    )
    energy_per_atom: float | None = Field(
        default=None,
        description="The final DFT energy per atom for the last calculation",
    )
    bandgap: float | None = Field(
        default=None,
        description="The DFT bandgap for the last calculation",
    )
    converged: bool = Field(
        default=False,
        description="Whether or not the calculaton has converged",
    )
    analysis: Analysis | None = Field(
        default=None,
        title="Calculation Analysis",
        description="Some analysis of calculation data after collection.",
    )
    calculation_objects: dict[str, Any] | None = Field(
        default=None,
        description="Calculation objects returned as outputs of this "
        "calculation",
    )
    bader_analysis: BaderAnalysis | None = Field(
        default=None, description="A Bader charge analysis document"
    )
    ddec6_analysis: DDEC6Analysis | None = Field(
        default=None, description="A DDEC6 charge analysis document"
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

    # ? How to record Bader charges?
    #   - attach in Python script: add to Atoms object as charges after running
    #   - ensure Atoms are serialized with `charges`
    @classmethod
    def from_directory(
        cls,
        *,
        dir_name: str | pathlib.Path,
        calculator_type: CalculatorType | None = None,
        strict_mode: bool = SETTINGS.STRICT_MODE,
    ) -> CalculationOutputs:
        """Generate a CalculationOutputs document from a calculation directory.

        Args:
            dir_name: The directory of a calculation.
            calculator_type: The type of calculation run. Must correspond to
                an ASE calculator.
            strict_mode: Whether or not to require all outputs. If True,
                errors will be thrown on missing outputs.

        Returns:
            A CalculationOutputs object.
        """
        logger.debug(f"Loading calculation outputs from {dir_name}")
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")

        # TODO: eliminate try/except by passing down strict_mode
        try:
            match calculator_type:
                case CalculatorType.VASP:
                    outputs = vasp.load_calculation_outputs(dir_name=dir_name)
                case CalculatorType.GAUSSIAN:
                    outputs = gaussian.load_calculation_outputs(
                        dir_name=dir_name
                    )
                case None:
                    outputs = {
                        "energy": read_energy(dir_name),
                        "forces": read_forces(dir_name),
                    }
                case _:
                    msg = (
                        f"Loading {calculator_type!s} calculation outputs "
                        "not supported!"
                    )
                    raise NotImplementedError(msg)
        except (
            FileNotFoundError,
            NotImplementedError,
            ElementTree.ParseError,
        ):
            logger.warning(
                f"Unable to read {calculator_type!s} calculation outputs"
            )

            if strict_mode:
                raise

            logger.info("Attempting to read generic calculation outputs")
            outputs = {
                "energy": read_energy(dir_name, strict_mode=strict_mode),
                "forces": read_forces(dir_name, strict_mode=strict_mode),
            }

        outputs["bader_analysis"] = outputs["chargemol_analysis"] = None

        with suppress(Exception):
            outputs["bader_analysis"] = bader_analysis_from_path(dir_name)

        with suppress(Exception):
            outputs["chargemol_analysis"] = ChargemolAnalysis(
                dir_name
            ).summary["ddec"]

        calculation_outputs = cls(**outputs)

        logger.debug(
            f"Successfully loaded calculation outputs from {dir_name}"
        )
        return calculation_outputs


class Calculation(Task):
    """A record representing a calculation."""

    calculation_inputs: CalculationInputs
    calculation_outputs: CalculationOutputs | None = None
    scheduler_inputs: hpc.SchedulerInputs
    scheduler_outputs: hpc.SchedulerOutputs | None = None

    @overload
    @staticmethod
    def get_output_atoms(
        dir_name: str | pathlib.Path,
        input_atoms: Atoms,
        calculator_type: CalculatorType,
        *,
        strict_mode: Literal[True],
    ) -> Atoms: ...

    @overload
    @staticmethod
    def get_output_atoms(
        dir_name: str | pathlib.Path,
        input_atoms: Atoms,
        calculator_type: CalculatorType,
        *,
        strict_mode: Literal[False],
    ) -> Atoms | None: ...

    @staticmethod
    def get_output_atoms(
        dir_name,
        input_atoms,
        calculator_type,
        *,
        strict_mode=SETTINGS.STRICT_MODE,
    ):
        """Retrieve output Atoms from a Calculation.

        Args:
            dir_name: The directory of a calculation.
            calculator_type: The type of calculation run. Must correspond to
                an ASE calculator.
            input_atoms: An Atoms object representing the corresponding input
                structure.
            strict_mode: Whether to raise an error if no output atoms found.
                Defaults to ``SETTINGS.STRICT_MODE``.

        Raises:
            FileNotFoundError: Unable to find output atoms file.

        Returns:
            An Atoms object representing the output structure.
        """
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")
        try:
            match calculator_type:
                case CalculatorType.VASP:
                    atoms = vasp.get_output_atoms(
                        dir_name=dir_name, input_atoms=input_atoms
                    )
                case CalculatorType.GAUSSIAN:
                    atoms = gaussian.get_output_atoms(
                        dir_name=dir_name, input_atoms=input_atoms
                    )
                case _:
                    msg = (
                        f"Retrieving output atoms from {calculator_type!s} "
                        "calculations is not yet supported"
                    )
                    raise NotImplementedError(msg)
        except (FileNotFoundError, NotImplementedError, StopIteration):
            if strict_mode:
                raise

            logger.warning("Unable to retrieve output atoms")
            return None

        return atoms

    @staticmethod
    def get_files_to_carryover(calculator_type: CalculatorType) -> list[str]:
        """Returns a list of strings representing the files to be carried over.

        Args:
            calculator_type: The type of calculator used in the calculation.
        """
        mod = importlib.import_module(f"{__package__}.{calculator_type!s}")
        files_to_carryover: list[str] = TypeAdapter(list[str]).validate_python(
            mod.FILES_TO_CARRYOVER
        )
        logger.debug(
            "Successfully retrieved files to carry over: "
            f"{files_to_carryover!r}"
        )
        return files_to_carryover

    @staticmethod
    def create_shell(context: dict[str, Any] | None = None) -> Calculation:
        """Creates a minimal :class:`Calculation` with defaults set.

        Args:
            context: A dictionary to be used to seed values in the shell.
                Defaults to None.

        Returns:
            A new :class:`Calculation` with no outputs.
        """
        context = context or {}
        return Calculation(
            **Task.create_shell(context).model_dump(exclude_none=True),
            calculation_inputs=context.get(
                "calculation_inputs", CalculationInputs()
            ),
            scheduler_inputs=context.get(
                "scheduler_inputs", hpc.SchedulerInputs()
            ),
        )

    @classmethod
    def from_directory(
        cls,
        dir_name: str | pathlib.Path,
        *,
        calculator_type: CalculatorType | None = None,
        task: Task | None = None,
        strict_mode: bool = SETTINGS.STRICT_MODE,
        magic_mode: bool = False,
    ) -> Calculation:
        """Generate a ``Calculation`` document from a calculation directory.

        Args:
            dir_name: The directory of a calculation.
            calculator_type: The type of calculation run. Must correspond to
                an ASE calculator.
            task: A Task from which to build the Calculation.

                .. deprecated:: 0.12.0
                   This parameter is ignored since task metadata, inputs, and
                   outputs are now **always** loaded using
                   ``super().from_directory()``.

            strict_mode: Whether to raise an error if no output atoms found.
                Defaults to True.
            magic_mode: Whether to defer the final object creation. If True,
                the final object will be an instance of the class specified
                by the ``_build_class`` attribute of the :class:`TaskMetadata`
                object created. Otherwise, a :class:`Calculation` object will
                be returned. Defaults to False.

        Returns:
            A :class:`Calculation` object.

        .. seealso::

            :meth:`.task.Task.from_directory`
        """
        logger.debug("Loading calculation from %s", dir_name)
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")

        if task:
            msg = "This parameter is now ignored. See docs."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)

        if magic_mode:
            return cls.load_magic(dir_name, strict_mode=strict_mode)

        task = Task.from_directory(dir_name=dir_name, strict_mode=strict_mode)
        calculation_inputs = CalculationInputs.from_directory(
            dir_name=dir_name,
            calculator_type=calculator_type,
        )
        calculator_type = CalculatorType(
            calculation_inputs.ase_calculator.__name__.lower()
        )
        # TODO: Consider reading subset of outputs from Atoms object
        # TODO: (e.g.,: forces, energy) and deferring calculation-specific
        # TODO: properties to other schemes
        calculation_outputs = CalculationOutputs.from_directory(
            dir_name=dir_name,
            calculator_type=calculator_type,
            strict_mode=strict_mode,
        )
        scheduler_inputs = hpc.SchedulerInputs.from_directory(
            dir_name=dir_name
        )
        scheduler_outputs = hpc.SchedulerOutputs.from_directory(
            dir_name=dir_name
        )

        if task.task_outputs is None or task.task_outputs.atoms is None:
            output_atoms = Calculation.get_output_atoms(
                dir_name=dir_name,
                input_atoms=task.task_inputs.atoms,
                calculator_type=calculator_type,
                strict_mode=strict_mode,
            )
        else:
            output_atoms = task.task_outputs.atoms

        task.patch_task(
            converged=calculation_outputs.converged,
            error=scheduler_outputs.error,
            output_atoms=output_atoms,
            files_to_carry_over=Calculation.get_files_to_carryover(
                calculator_type
            ),
        )

        logger.debug("Successfully loaded calculation from %s", dir_name)
        return cls(
            **task.model_dump(exclude_none=True),
            calculation_inputs=calculation_inputs,
            calculation_outputs=calculation_outputs,
            scheduler_inputs=scheduler_inputs,
            scheduler_outputs=scheduler_outputs,
        )

    # ? Is this necessary in addition to Task.write_inputs()
    # ? Is this for delegation scheme
    def write_input_atoms(
        self,
        new_job: pathlib.Path,
    ) -> None:
        """Writes a structure file to the new job directory.

        Args:
            new_job: A pathlib.Path object representing the path to the new job
                directory.
        """
        # ! This call should be removed since it should be called upon new task
        # ! creation
        self.prepare_input_atoms()
        with new_job.joinpath(SETTINGS.PYTHON_SCRIPT).open(
            mode="r", encoding="utf-8"
        ) as file:
            structure_name = extract_structure_name(python_script=file)

        self.task_inputs.atoms.write(new_job.joinpath(structure_name))

    def write_python_script(
        self,
        dst: pathlib.Path,
        *,
        template: str = SETTINGS.PYTHON_TEMPLATE,
        structure_name: str = SETTINGS.INPUT_ATOMS,
    ) -> pathlib.Path:
        """Write the Python script used to run the Calculation.

        Args:
            dst: The directory in which to write the Python script.
            template: The name of the template to use to write the Python
                script.
            structure_name: The name of the input structure to be used to
                load the :class:`~ase.atoms.Atoms` object for the calculation.

        Returns:
            A Path object representing the filename of the written Python
            script.
        """
        msgs = self.calculation_inputs.check_inputs()
        for msg in msgs:
            logger.warning(msg)

        calculator = self.calculation_inputs.ase_calculator.__name__
        parameters = self.calculation_inputs.parameters

        for k, v in parameters.items():
            parameters[k] = repr(v)

        env = jinja2.Environment(
            loader=Scripter.get_loader(),
            autoescape=False,  # noqa: S701
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        to_render = env.get_template(template)
        filename = dst.joinpath(SETTINGS.PYTHON_SCRIPT)

        with filename.open(mode="x", encoding="utf-8") as file:
            file.write(
                to_render.render(
                    calculator=calculator,
                    structure=structure_name,
                    parameters=parameters,
                    run_bader=self.calculation_inputs.run_bader,
                    run_chargemol=self.calculation_inputs.run_chargemol,
                )
            )

        return filename

    def write_slurm_script(
        self,
        dst: pathlib.Path,
        *,
        template_file: str = SETTINGS.SLURM_TEMPLATE,
        compute_canada_format: bool = False,
        slurm_script: str | None = None,
    ) -> pathlib.Path:
        """Write the SLURM input script using the template given.

        Args:
            dst: The directory in which to write the SLURM file.
            template_file: The template file to use. Defaults to
                ``SETTINGS.SLURM_TEMPLATE``.
            compute_canada_format: Whether or not to write the SLURM script
                in ComputeCanada format.
            slurm_script: The name with which the SLURM script will be
                written.

        Returns:
            A Path representing the filename of the written SLURM script.
        """
        msgs = self.scheduler_inputs.check_inputs()
        for msg in msgs:
            logger.warning(msg)

        parameters = self.scheduler_inputs.model_dump(
            mode="json", exclude_none=True, by_alias=True
        )
        slurm_parameters = {}

        for key, value in parameters.items():
            # ? Is this necessary given that we're dumping by alias above
            new_key = key.replace("_", "-")
            new_key = f"-{new_key}" if len(new_key) == 1 else f"--{new_key}"
            slurm_parameters[new_key] = value

        env = jinja2.Environment(
            loader=Scripter.get_loader(),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        template = env.get_template(template_file)
        slurm_script = slurm_script or SETTINGS.SLURM_SCRIPT
        filename = dst.joinpath(slurm_script)
        calculator = self.calculation_inputs.ase_calculator.__name__

        # TODO: add CLI logic to using `construct_cli_call`
        with filename.open(mode="x", encoding="utf-8") as file:
            file.write(
                template.render(
                    parameters=slurm_parameters,
                    **self.task_inputs.model_dump(),
                    compute_canada_format=compute_canada_format,
                    calculator=calculator,
                    python_script=SETTINGS.PYTHON_SCRIPT,
                    slurm_script=slurm_script,
                )
            )

        return filename

    def to_directory(
        self,
        dst: str | pathlib.Path,
        *,
        structure_name: str = SETTINGS.INPUT_ATOMS,
        legacy_mode: bool = False,
    ) -> None:
        """Write a Calculation to a directory.

        Args:
            dst: The directory to which to write the Calculation.
            structure_name: The name to be used to save the input
                struture for the calculation.
            legacy_mode: Whether or not to use the legacy directory
                structure.

        .. seealso::

            :ref:`legacy-vs-normal`
        """
        dst = pathlib.Path(dst)
        _ = self.write_python_script(dst, structure_name=structure_name)
        _ = self.write_slurm_script(dst)
        super().to_directory(
            dst,
            structure_name=structure_name,
            legacy_mode=legacy_mode,
        )


@overload
def read_energy(
    dir_name: pathlib.Path, *, strict_mode: Literal[False]
) -> float | None: ...


@overload
def read_energy(
    dir_name: pathlib.Path, *, strict_mode: Literal[True]
) -> float: ...


def read_energy(dir_name, *, strict_mode=SETTINGS.STRICT_MODE):
    """Read the final energy from the output atoms.

    Args:
        dir_name: The path to the calculation directory.
        strict_mode: Whether or not to raise an error if unable to retrieve
            the energy. If True, one of FileNotFound, PropertyNotImplemented,
            or RuntimeError will be raised if unable to retrieve the energy.

    Returns:
        A float representing the energy. If unable to read the energy
        and strict_mode is disable, this function will return None.
    """
    logger.info(f"Reading generic energy from {dir_name}")
    try:
        atoms = ase.io.read(dir_name.joinpath("final.traj"), index=-1)
        e = atoms.get_potential_energy()
        logger.info(f"Successfully read generic energy from {dir_name}")
        return e
    except (FileNotFoundError, PropertyNotImplementedError, RuntimeError):
        logger.warning(f"Failed to read generic energy from {dir_name}")
        if strict_mode:
            raise

        return None


@overload
def read_forces(
    dir_name: pathlib.Path, *, strict_mode: Literal[False]
) -> list[list[float]] | None: ...


@overload
def read_forces(
    dir_name: pathlib.Path, *, strict_mode: Literal[True]
) -> list[list[float]]: ...


def read_forces(
    dir_name: pathlib.Path, *, strict_mode: bool = SETTINGS.STRICT_MODE
) -> list[list[float]]:
    """Read the final forces from the output atoms.

    Args:
        dir_name: The path to the calculation directory.
        strict_mode: Whether or not to raise an error if unable to retrieve
            the forces. If True, one of FileNotFound, PropertyNotImplemented,
            or RuntimeError will be raised if unable to retrieve the forces.
            Defaults to :attr:`SETTINGS.STRICT_MODE`.

    Returns:
        A list of lists of floats representing the forces. If unable to read
        the energy and ``strict_mode`` is disable, this function will return
        None.
    """
    logger.info(f"Reading generic forces from {dir_name}")
    try:
        atoms = ase.io.read(dir_name.joinpath("final.traj"), index=-1)
        f = atoms.get_forces()
        logger.info(f"Successfully read generic forces from {dir_name}")
        return f
    except (FileNotFoundError, PropertyNotImplementedError, RuntimeError):
        logger.warning(f"Failed to read generic forces from {dir_name}")
        if strict_mode:
            raise

        return None
