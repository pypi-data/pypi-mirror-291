"""Specify the configurable parameters for a calculator."""

from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import MutableMapping
from importlib import import_module
from typing import TYPE_CHECKING
from typing import Any

from monty.json import MSONable

if TYPE_CHECKING:
    from autojob.calculation import parameters


class CalculatorConfiguration(MutableMapping, MSONable):
    """A set of calculator parameters."""

    def __init__(
        self,
        calculator_parameters: Iterable[parameters.CalculatorParameter],
        values: Iterable | None = None,
    ) -> None:
        """Create a ``CalculatorConfiguration`` from parameters and values.

        Args:
            calculator_parameters: An iterable of
                :class:`.parameters.CalculatorParameter` s from which to create
                the configuration.
            values: The values with which to initialize the configuration.
                Defaults to None, in which case, the defaults of the
                :class:`.parameters.CalculatorParameter` s are used.
        """
        if values is None:
            self._dict = CalculatorConfiguration.initialize_values(
                calculator_parameters
            )
        else:
            self._dict = dict(zip(calculator_parameters, values, strict=False))

    @staticmethod
    def initialize_values(
        calculator_parameters: Iterable[parameters.CalculatorParameter],
    ) -> dict[parameters.CalculatorParameter, Any]:
        """Initialize the values of a ``CalculatorConfiguration``.

        Args:
            calculator_parameters: An iterable of
                :class:`.parameters.CalculatorParameter` s for which from
                which to initialize the ``CalculatorConfiguration``.

        Returns:
            A dictionary mapping :class:`.parameters.CalculatorParameter` s to
            their value in the configuration.
        """
        param_vals = {}
        for calculator_parameter in calculator_parameters:
            if calculator_parameter.default is not None:
                param_vals[calculator_parameter] = calculator_parameter.default
            else:
                param_vals[calculator_parameter] = None
        return param_vals

    def __getitem__(self, __k: parameters.CalculatorParameter) -> Any:
        """Get the value of ``CalculatorParameter``."""
        return self._dict[__k]

    def __setitem__(self, __k: parameters.CalculatorParameter, __v: Any):
        """Set the value of ``CalculatorParameter``."""
        self._dict[__k] = __v

    def __delitem__(self, __v: parameters.CalculatorParameter):
        """Delete the value of ``CalculatorParameter``."""
        del self._dict[__v]

    def __iter__(self) -> Iterator[parameters.CalculatorParameter]:
        """Iterate over the ``CalculatorParameter`` s in the configuration."""
        return iter(self._dict)

    def __len__(self) -> int:
        """Get the number of ``CalculatorParameter`` s in the configuration."""
        return len(self._dict)

    def __eq__(self, __o: object) -> bool:
        """Returns True if underlying mappings are equal. False otherwise."""
        if not isinstance(__o, CalculatorConfiguration):
            return False

        return __o._dict == self._dict

    def as_dict(self) -> dict[str, Any]:
        """Convert the ``CalculatorConfiguration`` to a dictionary.

        The :class:`.parameters.CalculatorParameter` s are stored
        as dictionaries, and the underlying dictionary is stored
        as a list of 2-tuples where the first element corresponds
        to the ``CalculatorParameter`` and the second element
        corresponds to the value.
        """
        parameters_and_values = [
            (p.as_dict(), value) for p, value in self._dict.items()
        ]
        return {
            "parameters_and_values": parameters_and_values,
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, d) -> CalculatorConfiguration:
        """Return a ``CalculatorConfiguration`` from a dictionary.

        This method is implemented to enable round-trips from
        :meth:`.calculators.CalculatorConfiguration.as_dict` and
        :meth:`.calculators.CalculatorConfiguration.from_dict`.
        """
        # Extract parameter dicts
        parameter_dicts = [x for x, _ in d["parameters_and_values"]]

        # Extract parameter type
        params = []
        for parameter_dict in parameter_dicts:
            module = import_module(parameter_dict["@module"])
            parameter_type = getattr(module, parameter_dict["@class"])
            constructor = parameter_type.from_dict
            params.append(constructor(parameter_dict))

        # Extract parameter value
        values = [y for _, y in d["parameters_and_values"]]
        return cls(params, values)
