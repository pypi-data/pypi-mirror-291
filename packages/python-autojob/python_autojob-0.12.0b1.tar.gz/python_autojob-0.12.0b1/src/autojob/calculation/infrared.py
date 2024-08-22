"""Retrieve outputs from an infrared calculation.

This module provides the :class:`InfraredOutputs`
and :class:`Infrared` classes. The results from
infrared calculations can be retrieve using the
:meth:`InfraredOutputs.from_directory` and
:meth:`Infrared.from_directory` methods.

Example:

    .. code-block::

        from pathlib import Path
        from autojob.calculation.infrared import Infrared

        task = Infrared.from_directory(Path.cwd())
"""

import logging
from pathlib import Path
from typing import Any
from typing import ClassVar
import warnings

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from autojob import SETTINGS
from autojob.calculation.calculation import Calculation
from autojob.calculation.parameters import CalculatorType
from autojob.calculation.vibration import Vibration
from autojob.task import Task

logger = logging.getLogger(__name__)


class InfraredOutputs(BaseModel):
    """The outputs of an infrared calculation."""

    ir_frequencies: list[complex] | None = Field(
        default=None, alias="IR Frequencies"
    )
    ir_intensities: list[float] | None = Field(
        default=None, alias="IR Intensities"
    )
    ir_absorbance: list[float] | None = Field(
        default=None, alias="IR Absorbance"
    )
    # TODO: add type, prefactor, width as properties

    model_config: ClassVar[ConfigDict] = ConfigDict(
        populate_by_name=True, arbitrary_types_allowed=True
    )

    @classmethod
    def from_directory(
        cls,
        dir_name: str | Path,
        *,
        out: str = "ir-spectra.dat",
        strict_mode: bool = SETTINGS.STRICT_MODE,
    ) -> "InfraredOutputs":
        """Extract infrared data from the input structure of the directory.

        Args:
            dir_name: The directory of the completed calculation.
            out: The name of the file from which to read the IR data. Defaults
                to ``"ir-spectra.dat"``.
            strict_mode: Whether or not to require all outputs. If True,
                errors will be thrown on missing outputs. Defaults to
                ``SETTINGS.STRICT_MODE``.

        Returns:
            The infrared data as ``InfraredOutputs``. If no data is found,
            and ``strict_mode = False`` every value will be None.
        """
        dir_name = Path(dir_name)
        logger.info(f"Loading infrared data for {dir_name!s}")
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")

        try:
            ir_txt = dir_name.joinpath(out)
            with ir_txt.open(mode="r", encoding="utf-8") as vib_file:
                # Discard two header lines
                _ = vib_file.readline()
                _ = vib_file.readline()

                frequencies = []
                intensities = []
                absorbance = []
                for line in vib_file:
                    f, i, a, *_ = line.split()

                    # ? Strips necessary?
                    frequencies.append(f.strip())
                    intensities.append(i.strip())
                    absorbance.append(a.strip())

                logger.info(
                    f"Successfully loaded infrared data for {dir_name!s}"
                )
        except (FileNotFoundError, RuntimeError):
            frequencies = intensities = absorbance = None
            if strict_mode:
                raise

            logger.warning(f"Unable to load infrared data for {dir_name!s}")

        return cls(
            ir_frequencies=frequencies,
            ir_intensities=intensities,
            ir_absorbance=absorbance,
        )


class Infrared(Vibration):
    """An infrared calculation."""

    infrared_outputs: InfraredOutputs | None = None

    @staticmethod
    def create_shell(context: dict[str, Any] | None = None) -> "Infrared":
        """Create a minimal ``Infrared`` shell.

        Args:
            context: A dictionary mapping attribute paths to their values.
                For example, the ``"infrared_outputs"`` key will be used to set
                the ``infrared_outputs`` attribute in the returned object.

        Returns:
            An :class:`Infrared` object initialized with the values in
            ``context``.
        """
        context = context or {}
        return Infrared(
            **Vibration.create_shell(context).model_dump(exclude_none=True)
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
    ) -> "Infrared":
        """Generate a ``Infrared`` document from a calculation directory.

        Args:
            dir_name: The directory of a infrared calculation.
            calculator_type: The type of calculation run. Must correspond to
                an ASE calculator.
            task: A :class:`~autojob.task.Task` from which to build the
                ``Infrared``.

                .. deprecated:: 0.12.0
                    This parameter is ignored since task metadata, inputs, and
                    outputs are now **always** loaded using
                    ``super().from_directory()``.

            strict_mode: Whether to raise an error if no output atoms found.
                Defaults to ``SETTINGS.STRICT_MODE``.
            magic_mode: Whether to defer the final object creation. If True,
                the final object will be an instance of the class specified
                by the ``_build_class`` attribute of the :class:`TaskMetadata`
                object created. Otherwise, a :class:`Infrared` object will
                be returned. Defaults to False.

        Returns:
            A :class:`Vibration` object.

        .. seealso:: :meth:`autojob.task.Task.from_directory`
        """
        logger.info("Loading infrared calculation from %s", dir_name)
        logger.debug(f"Strict mode {'en' if strict_mode else 'dis'}abled")

        if task:
            msg = "This parameter is now ignored. See docs."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)

        if magic_mode:
            return Calculation.load_magic(dir_name, strict_mode=strict_mode)

        calculation = Vibration.from_directory(
            dir_name=dir_name,
            calculator_type=calculator_type,
            task=task,
            strict_mode=strict_mode,
        ).model_dump()
        calculation["infrared_outputs"] = InfraredOutputs.from_directory(
            dir_name
        )
        ir_task = cls(**calculation)
        logger.info("Finished loading infrared calculation from %s", dir_name)
        return ir_task

    def write_python_script(
        self,
        dst: Path,
        *,
        template: str = "infrared.py.j2",
        structure_name: str = SETTINGS.INPUT_ATOMS,
    ) -> Path:
        """Write the Python script for the calcuation.

        Args:
            dst: A :class:`Path` indicating to where the script will be written.
            template: The template to use to write the script. Defaults to
                ``"infrared.py.j2"``.
            structure_name: The name of the input structure file. Defaults to
                ``SETTINGS.INPUT_ATOMS``.

        Returns:
            The path of the newly written file.
        """
        return super().write_python_script(
            dst, template=template, structure_name=structure_name
        )
