"""Group tasks by structure and calculation and submission parameters.

This module defines classes used to group tasks by structure, calculation
parameters, and submission parameters.

:class:`StructureGroup`s are lists of structure file names.

:class:`CalculationParameterGroup`s map :class:`.job.CalculationParameter`s
to values.

:class:`SubmissionParameterGroup`s map structure file names to dictionaries
which map :class:`.job.CalculationParameter`s to values which define
which calculations are to be included in the `SubmissionParameterGroup`.
"""

from collections.abc import Iterable
import pathlib
from typing import Any

from autojob.coordinator import job
from autojob.coordinator import validation


class StructureGroup:
    """A collection of structure filenames.

    `StructureGroup`s indicate how to group calculations involving
    particular structures.
    """

    def __init__(self) -> None:
        """Initialize a `StructureGroup`."""
        self._structures: list[pathlib.Path] = []

    @property
    def structures(self) -> list[pathlib.Path]:
        """The filenames of structures in the `StructureGroup`."""
        return self._structures.copy()

    @structures.setter
    def structures(
        self, new_structures: Iterable[pathlib.PurePath | str]
    ) -> None:
        validated_structures = StructureGroup.validate_structures(
            new_structures
        )

        self._structures = validated_structures

    # TODO: verify necessity of this function?
    # TODO: can this be replaced by Pydantic?
    @staticmethod
    def validate_structures(
        new_structures: Iterable[pathlib.Path | str],
    ) -> list[pathlib.Path]:
        """Check that each structure filename points to an existing file.

        Args:
            new_structures: An iterable of paths or filenames representing
                new structures.

        Returns:
            A list of paths corresponding to valid existing structure files.
        """
        if not isinstance(new_structures, Iterable):
            msg = "New structures must be an iterable"
            raise TypeError(msg)

        structure_paths: list[pathlib.Path] = []

        for structure in new_structures:
            try:
                if isinstance(structure, pathlib.Path):
                    path = structure
                else:
                    path = pathlib.Path(structure)

                if not path.exists():
                    msg = f"{path} does not exist"
                    raise FileNotFoundError(msg)
                if not path.is_file():
                    msg = "Structure must be a file"
                    raise ValueError(msg)

                structure_paths.append(path)

            except TypeError as error:
                msg = "Each structure in the iterable must be a Path or str"
                raise ValueError(msg) from error

        return structure_paths

    def add_structures(self, new_structures: Iterable[pathlib.Path]) -> None:
        """Add and validate new structures to `StructureGroup`.

        Args:
            new_structures: An iterable of paths to add to the
                `StructureGroup`. Duplicates are removed.
        """
        structures = self.structures
        structures.extend(StructureGroup.validate_structures(new_structures))
        structures = list(dict.fromkeys(structures))
        self.structures = structures

    def remove_structures(self, indices_to_remove: Iterable[int]) -> None:
        """Remove structures from the `StructureGroup`.

        Args:
            indices_to_remove: The indices of structures to remove.
        """
        structures_to_remove = [self.structures[i] for i in indices_to_remove]
        for structure in structures_to_remove:
            self._structures.remove(structure)

    # ? Redundant given `.validate_structures()`
    def validated_structures(
        self, new_structures: Iterable[pathlib.Path | str]
    ) -> list[pathlib.Path]:
        """Check that each structure filename points to an existing file.

        Args:
            new_structures: An iterable of paths or filenames representing
                new structures.

        Returns:
            A list of paths corresponding to valid existing structure files.
        """
        if not isinstance(new_structures, Iterable):
            msg = "New structures must be an iterable"
            raise TypeError(msg)

        structure_paths: list[pathlib.Path] = []

        for structure in new_structures:
            try:
                if isinstance(structure, pathlib.Path):
                    path = structure
                else:
                    path = pathlib.Path(structure)

                if not path.exists():
                    msg = f"{path} does not exist"
                    raise FileNotFoundError(msg)
                if not path.is_file():
                    msg = "Structure must be a file"
                    raise ValueError(msg)

                structure_paths.append(path)

            except TypeError as error:
                msg = "Each structure in the iterable must be a Path or str"
                raise ValueError(msg) from error

        return structure_paths


class CalculationParameterGroup:
    """A collection of values of :class:`.job.CalculationParameter`s.

    A :class:`CalculationParameterGroup` maps a `CalcuationParameter`
    to a list of values of that `CalculationParameter`.

    Example:
        import math

        from autojob.coordinator.gui.groups import CalculationParameterGroup
        from autojob.coordinator.job import CalculationParameter

        parameter = CalculationParameter(
            name="parameter",
            explicit=False,
            allowed_types=[int],
            values=(-math.inf, math.inf, "()")
            default=1,
        )
        group = CalculationParameterGroup([parameter])
    """

    def __init__(
        self, calculation_parameters: list[job.CalculationParameter]
    ) -> None:
        """Initialize a `CalculationParameterGroup`.

        Args:
            calculation_parameters: A list of
                :class:`.job.CalculationParameter`s used to define
                the `CalculationParameterGroup`.
        """
        # TODO: annotate keys of `_values` as a generic related to the type
        # TODO: of its values
        self._values: dict[job.CalculationParameter, list[Any]] = (
            CalculationParameterGroup.initialize_values(calculation_parameters)
        )

    @staticmethod
    def initialize_values(
        calculation_parameters: list[job.CalculationParameter],
    ) -> dict[job.CalculationParameter, list[Any]]:
        """Initialize the values of a `CalculationParameterGroup`.

        Args:
            calculation_parameters: An iterable of
                :class:`.job.CalculationParameter`s for which from
                which to initialize the `CalculationParameterGroup`.

        Returns:
            A dictionary mapping :class:`.parameters.CalculatorParameter`s to
            a list of values defining the group.
        """
        param_vals = {}
        for param in calculation_parameters:
            if param.default is not None:
                param_vals[param] = [param.default]
            else:
                param_vals[param] = []
        return param_vals

    @property
    def values(self) -> dict[job.CalculationParameter, list[Any]]:
        """A mapping from `CalculationParameter`s to its values."""
        return self._values.copy()

    @values.setter
    def values(self, new_values: dict[job.CalculationParameter, list[Any]]):
        """Set :attr:`CalculationParameterGroup._values` to a new value."""
        self._values = new_values

    @property
    def defined_values(self) -> list[list[Any]]:
        """The defined values of each `CalculationParameter`."""
        return [x for x in self.values.values() if x]

    @property
    def defined_calculation_parameters(self) -> list[job.CalculationParameter]:
        """The `CalculationParameter`s for which values are defined."""
        return [x for x, y in self.values.items() if y]

    def add_values(
        self, calculation_parameter: job.CalculationParameter, vals: Iterable
    ) -> None:
        """Add values of parameter.

        Args:
            calculation_parameter: The calculation parameter to add.
            vals: The values for the calculation parameter.
        """
        vals = validation.iter_to_native(vals)
        vals.extend(self.values[calculation_parameter])

        vals = validation.alphanum_sort(
            [str(val) for val in dict.fromkeys(vals)]
        )

        self._values[calculation_parameter] = validation.iter_to_native(vals)

    def remove_values(
        self,
        calculation_parameter: job.CalculationParameter,
        indices_to_remove: Iterable[int],
    ) -> None:
        """Remove values from a calculation parameter set.

        Args:
            calculation_parameter: The calculation parameter from which a
                value will be removed.
            indices_to_remove: The indices in the calculation parameter set to
                remove.
        """
        values_to_remove = [
            self.values[calculation_parameter][i] for i in indices_to_remove
        ]
        values_to_remove = validation.iter_to_native(values_to_remove)

        for value in values_to_remove:
            self.values[calculation_parameter].remove(value)


class SubmissionParameterGroup:
    """A collection of values of submission parameters.

    A :class:`SubmissionParameterGroup` maps structure filenames
    to a mapping relating the names of `CalculationParameter` to
    a list of values of that `CalculationParameter`.

    Example:
        from autojob.coordinator.gui.groups import SubmissionParameterGroup

        group = SubmissionParameterGroup(["memory"])
    """

    def __init__(self) -> None:
        """Initialize a `SubmissionParameterGroup`."""
        self._values: dict[str, dict[str, list]] = {}

    @property
    def values(self) -> dict[str, dict[str, list]]:
        """A mapping from structure names to a `CalculationParameter` mapping."""
        return self._values.copy()

    @values.setter
    def values(self, new_values: dict[str, dict[str, list[str]]]):
        """Set :attr:`SubmissionParameterGroup._values` to a new value."""
        self._values = new_values

    def update(self, specs_to_add: dict[str, dict[str, list[str]]]):
        """Update the values of `CalculationParameter`s in the group.

        Args:
            specs_to_add: A dictionary of the same form as
                :meth:`SubmissionParameterGroup.values` used to update
                the values in the `SubmissionParameterGroup`.
        """
        for structure, params in specs_to_add.items():
            if structure not in self._values:
                self._values[structure] = params
            else:
                for param, values in params.items():
                    old_params = self._values[structure]

                    if param not in old_params:
                        self._values[structure][param] = values
                    else:
                        for value in values:
                            old_values = self._values[structure][param]

                            if value not in old_values:
                                self._values[structure][param].append(value)
