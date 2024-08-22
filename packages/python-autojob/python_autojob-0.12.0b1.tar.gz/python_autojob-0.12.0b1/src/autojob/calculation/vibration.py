"""Retrieve the results of a vibrational calculation.

This module provides utilities from retrieving the
inputs and outputs of a vibrational (frequency) calculation
from a directory.

Example:
    from pathlib import Path

    from autojob.calculation.vibration import Vibration

    task = Vibration.from_directory(Path.cwd())
"""

import logging
from pathlib import Path
from typing import Any
from typing import ClassVar
import warnings

from ase.constraints import FixAtoms
from ccu.thermo.gibbs import calculate_free_energy
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from autojob import SETTINGS
from autojob.calculation.calculation import Calculation
from autojob.calculation.parameters import CalculatorType
from autojob.task import Task
from autojob.utils.files import extract_structure_name

logger = logging.getLogger(__name__)


FREEZE_WARNING = (
    "There are no atoms with tags in "
    "{0}. Every atom will be frozen. This is "
    "likely not what you want for a vibrational calculation. "
    "Check that your structure still possesses its original tags "
    "and that you have specified a reasonable list of tags to "
    "freeze."
)
FREE_MOLECULES = ["H2", "CO", "CO2", "HCOOH", "H2O"]


# TODO: complete
class VibrationInputs(BaseModel):
    """The inputs of a vibrational calculation."""


class VibrationOutputs(BaseModel):
    """The outputs of a vibratoinal calculation."""

    entropic_correction: float | None = Field(
        default=None, alias="TS Correction"
    )
    vibrational_frequencies: list[float] | None = Field(
        default=None, alias="Frequencies"
    )
    zero_point_energy: float | None = Field(
        default=None, alias="Zero-Point Energy"
    )

    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

    # TODO: Refactor
    @classmethod
    def from_directory(
        cls, dir_name: str | Path, *, strict_mode: bool = SETTINGS.STRICT_MODE
    ) -> "VibrationOutputs":
        """Extract thermo data from the input structure of the directory.

        Args:
            dir_name: The directory of the completed calculation.
            strict_mode: Whether or not to require all outputs. If True,
                errors will be thrown on missing outputs.

        Returns:
            The thermodynamic data as `VibrationOutputs`. If no data is found,
            and `strict_mode = False` every value will be None.
        """
        dir_name = Path(dir_name)
        logger.info(f"Loading thermodynamic data for {dir_name!s}")
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")
        python_script = dir_name.joinpath(SETTINGS.PYTHON_SCRIPT)
        geometry = "nonlinear"

        try:
            with python_script.open(mode="r", encoding="utf-8") as file:
                structure_name = extract_structure_name(file)
                structure = structure_name.removeprefix("./").removesuffix(
                    ".traj"
                )

            if structure in FREE_MOLECULES:
                approximation = "IDEAL_GAS"

                if structure in ("CO", "CO2", "H2"):
                    geometry = "linear"
            else:
                approximation = "HARMONIC"

            vib_txt = dir_name.joinpath("vib.txt")
            with vib_txt.open(mode="r", encoding="utf-8") as vib_file:
                ts, zpve, freq = calculate_free_energy(
                    log_file=None,
                    vib_file=vib_file,
                    approximation=approximation,
                    geometry=geometry,
                    atoms_file=str(dir_name.joinpath(structure_name)),
                )
                logger.info(
                    f"Successfully loaded thermodynamic data for {dir_name!s}"
                )
        except (FileNotFoundError, RuntimeError):
            ts = zpve = freq = None
            if strict_mode:
                raise

            logger.warning(
                f"Unable to load thermodynamics data for {dir_name!s}"
            )

        return cls(
            entropic_correction=ts,
            zero_point_energy=zpve,
            vibrational_frequencies=freq,
        )


class Vibration(Calculation):
    """A vibrational calculation."""

    vibration_inputs: VibrationInputs
    vibration_outputs: VibrationOutputs | None = None

    @staticmethod
    def create_shell(context: dict[str, Any] | None = None) -> "Vibration":
        """Create a minimal ``Vibration`` shell.

        Args:
            context: A dictionary mapping attribute paths to their values.
                For example, the ``"vibration_outputs"`` key will be used to set
                the ``vibration_outputs`` attribute in the returned object.

        Returns:
            An :class:`Infrared` object initialized with the values in
            ``context``.
        """
        context = context or {}
        return Vibration(
            **Calculation.create_shell(context).model_dump(exclude_none=True),
            vibration_inputs=VibrationInputs(),
        )

    @classmethod
    def from_directory(
        cls,
        dir_name: str | Path,
        *,
        calculator_type: CalculatorType | None = None,
        task: Task | None = None,
        strict_mode: bool = SETTINGS.STRICT_MODE,
        magic_mode: bool = False,
    ) -> "Vibration":
        """Generate a ``Vibration`` document from a calculation directory.

        Args:
            dir_name: The directory of a vibrational calculation.
            calculator_type: The type of calculation run. Must correspond to
                an ASE calculator.
            task: A :class:`~Task` from which to build the ``Vibration``.

                .. deprecated:: 0.12.0
                    This parameter is ignored since task metadata, inputs, and
                    outputs are now **always** loaded using
                    ``super().from_directory()``.

            strict_mode: Whether to raise an error if no output atoms found.
                Defaults to ``SETTINGS.STRICT_MODE``.
            magic_mode: Whether to defer the final object creation. If True,
                the final object will be an instance of the class specified
                by the ``_build_class`` attribute of the :class:`TaskMetadata`
                object created. Otherwise, a :class:`Vibration` object will
                be returned. Defaults to False.

        Returns:
            A :class:`Vibration` object.

        .. seealso::

            :meth:`.task.Task.from_directory`
        """
        logger.info("Loading vibrational calculation from %s", dir_name)
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")

        if task:
            msg = "This parameter is now ignored. See docs."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)

        if magic_mode:
            return Calculation.load_magic(dir_name, strict_mode=strict_mode)

        calculation = Calculation.from_directory(
            dir_name=dir_name,
            calculator_type=calculator_type,
            task=task,
            strict_mode=strict_mode,
        ).model_dump()
        calculation["vibration_outputs"] = VibrationOutputs.from_directory(
            dir_name, strict_mode=strict_mode
        )
        vib_task = cls(**calculation, vibration_inputs={})
        logger.info(
            "Finished loading vibrational calculation from %s", dir_name
        )
        return vib_task

    def write_python_script(
        self,
        dst: Path,
        *,
        template: str = "vibration.py.j2",
        structure_name: str = SETTINGS.INPUT_ATOMS,
    ) -> Path:
        """Write the Python script for the calculation."""
        return super().write_python_script(
            dst, template=template, structure_name=structure_name
        )

    def freeze_catalyst_atoms(
        self, tags_to_unfreeze: list[int] | None = None
    ) -> None:
        """Freeze the catalyst atoms of an input structure.

        Args:
            tags_to_unfreeze: A list of tags indicating which atoms to
                unfreeze. Defaults to ``[-99]``.

        Raises:
            RuntimeError: No input atoms to freeze in task.

        Warns:
            UserWarning: Every atom in the ``Atoms`` object will be frozen.
        """
        logger.debug(
            f"Freezing catalyst atoms in task: {self.task_metadata.task_id}"
        )

        if tags_to_unfreeze is None:
            tags_to_unfreeze = [-99]

        if self.task_inputs.atoms is None:
            msg = (
                "No input atoms to freeze in task: "
                f"{self.task_metadata.task_id}"
            )
            raise RuntimeError(msg)

        indices = [
            atom.index
            for atom in self.task_inputs.atoms
            if atom.tag not in tags_to_unfreeze
        ]
        if indices:
            c = FixAtoms(indices=indices)
            self.task_inputs.atoms.set_constraint(c)
            logger.debug(
                "Successfully froze catalyst atoms in task: "
                f"{self.task_metadata.task_id}"
            )
        else:
            warnings.warn(
                message=FREEZE_WARNING.format(repr(tags_to_unfreeze)),
                category=UserWarning,
                stacklevel=2,
            )
            logger.debug(f"Atom tags: {self.task_inputs.atoms.get_tags()!r}")
            logger.debug(f"Tags to unfreeze: {tags_to_unfreeze!r}")

    def prepare_input_atoms(self) -> None:
        """Prepare the input atoms for the calculation."""
        super().prepare_input_atoms()
        self.freeze_catalyst_atoms()
