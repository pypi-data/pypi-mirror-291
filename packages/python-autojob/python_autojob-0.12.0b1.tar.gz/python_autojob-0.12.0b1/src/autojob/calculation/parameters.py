"""Define calculator parameters."""

from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Mapping
from collections.abc import Sequence
from copy import copy
from copy import deepcopy
from enum import Enum
import math
from typing import Any

from monty.json import MSONable


class CalculatorType(Enum):
    """A type of ASE calculator."""

    ABINIT = "abinit"
    ACE = "ace"
    AIMS = "aims"
    AMBER = "amber"
    ASAP = "asap"
    CASTEP = "castep"
    CP2K = "cp2k"
    CRYSTAL = "crystal"
    DEMON = "demon"
    DEMON_NANO = "demonnano"
    DFTB = "dftb"
    DFTD3 = "dftd3"
    DMOL3 = "dmol"
    EAM = "eam"
    ELK = "elk"
    EMT = "emt"
    ESPRESSO = "espresso"
    EXCITING = "exciting"
    FORCE_FIELD = "ff"
    FLEUR = "fleur"
    GAMESS_US = "gamess_us"
    GAUSSIAN = "gaussian"
    GPAW = "gpaw"
    GROMACS = "gromacs"
    GULP = "gulp"
    HOTBIT = "hotbit"
    KIM = "kim"
    LAMMPS = "lammpsrun"
    LAMMPS_LIB = "lammpslib"
    LENNARD_JONES = "lj"
    MOPAC = "mopac"
    MORSE_POTENTIAL = "morse"
    NWCHEM = "nwchem"
    OCTOPUS = "octopus"
    ONETEP = "onetep"
    OPENMX = "openmx"
    ORCA = "orca"
    PSI4 = "psi4"
    QCHEM = "qchem"
    SIESTA = "siesta"
    TIP3P = "tip3p"
    TIP4P = "tip4p"
    TURBOMOLE = "turbomole"
    VASP = "vasp"

    DEFAULT = "vasp"  # noqa: PIE796

    def __str__(self) -> str:
        """Get a string representation of a `CalculatorType`."""
        return self.value

    def is_implemented(self) -> bool:
        """Return whether the `CalculatorType` is implemented or not."""
        implemented_calculator_types = [
            CalculatorType.VASP,
            CalculatorType.GAUSSIAN,
        ]

        return self in implemented_calculator_types


# ! Remove all NumberRange etc.
class NumberRange(MSONable):
    """A range of numbers."""

    def __init__(
        self,
        *,
        lower_bound: int | float = -math.inf,
        lower_bound_exclusive: bool = True,
        upper_bound: int | float = math.inf,
        upper_bound_exclusive: bool = True,
    ) -> None:
        """Initialize a `NumberRange`.

        Args:
            lower_bound: The lower bound for the range.
            lower_bound_exclusive: Whether the lower bound is excluded from
                the range.
            upper_bound: The upper bound for the range.
            upper_bound_exclusive: Whether the upper bound is excluded from
                the range.
        """
        if math.nan in (lower_bound, upper_bound):
            msg = "Neither bound can be NaN"
            raise ValueError(msg)
        if lower_bound == math.inf:
            msg = "Lower bound must be less than positive infinity"
            raise ValueError(msg)
        if upper_bound == -math.inf:
            msg = "Upper bound must be greater than negative infinity"
            raise ValueError(msg)
        if lower_bound > upper_bound:
            msg = "Lower bound must be less than upper bound"
            raise ValueError(msg)

        self.lower_bound = lower_bound
        self.lower_bound_exclusive = lower_bound_exclusive
        self.upper_bound = upper_bound
        self.upper_bound_exclusive = upper_bound_exclusive

    def __repr__(self) -> str:
        """A string representation of the number range."""
        return (
            f"NumberRange(lower_bound={self.lower_bound}, "
            f"lower_bound_exclusive={self.lower_bound_exclusive}, "
            f"upper_bound={self.upper_bound}, "
            f"upper_bound_exclusive={self.upper_bound_exclusive})"
        )

    def __eq__(self, __o: object) -> bool:
        """Determine if both bounds and their exclusivity are equal."""
        if not isinstance(__o, NumberRange):
            return False

        return False not in (
            __o.lower_bound == self.lower_bound,
            __o.lower_bound_exclusive == self.lower_bound_exclusive,
            __o.upper_bound == self.upper_bound,
            __o.upper_bound_exclusive == self.upper_bound_exclusive,
        )

    def validate_number(self, number: int | float) -> bool:
        """Returns True if a number is within the range. False, otherwise.

        Args:
            number: A number to check.
        """
        if number < self.lower_bound or number > self.upper_bound:
            return False

        if number == self.lower_bound and self.lower_bound_exclusive:
            return False

        return number != self.upper_bound or self.upper_bound_exclusive


# TODO: design method for checking compatibility and necessity of certain
# input parameters
# e.g., dipole-related parameters should either all be on or off
# e.g., relation between NBANDS, NCORE, NPAR, KPAR, NELC, and NIONS


class CalculatorParameter(MSONable):
    """Abstraction of an calculator parameter for a supported ASE calculator.

    Attributes:
        name (str; defaults to ''): The name of the CalculatorParameter.

        allowed_types (Iterable[Type]; defaults to (Any,)): The allowed types
            for the CalculatorParameter. For validation and displaying (in the
            GUI application) purposes, if there exists special values for the
            CalculatorParameter (e.g., string values that correspond to
            particular values), the allowed types should not be designated so
            as to include these special values.

        For example, say that a particular CalculatorParameter accepts integer
        values, but that the string 'normal' corresponds to a particular
        value. The allowed types for the CalculatorParameter should be
        specified as (int,) and not (int, str).

        special_values (Iterable; defaults to tuple()): A tuple indicating the
        special values of a CalculatorParameter. These may be values whose
        types do not conform to the types specified in the attribute
        'allowed_types'.

        _default (Any; defaults to None): A default value for the
        CalculatorParameter.

        description (str; defaults to ''): Returns a description of the
        CalculatorParameter to be used for displaying tooltips.
    """

    def __init__(
        self,
        name: str = "",
        allowed_types: Iterable[type] = (Any,),
        special_values: Iterable | None = None,
        default: Any = None,
        description: str = "",
    ):
        """Initialize a `CalculatorParameter`.

        Args:
            name: The name of the `CalculatorParameter`. Defaults to "".
            allowed_types: An iterable of the allowed types for the parameter.
                Defaults to (Any,).
            special_values: An iterable of the special values for the parameter.
                Defaults to None.
            default: The default value for the parameter. Defaults to None.
            description: A description of the parameter. Defaults to "".
        """
        self.name = name
        self._allowed_types: tuple[type] = tuple(allowed_types)
        self._allowed_types: tuple[type] = tuple(allowed_types)

        self._special_values = tuple(special_values) if special_values else ()
        self._special_values = tuple(special_values) if special_values else ()

        self._default = default
        self.description = description

    def __eq__(self, __o: object) -> bool:
        """Determine if two parameters are equal."""
        if not isinstance(__o, CalculatorParameter):
            return False

        return False not in (
            __o.name == self.name,
            __o._allowed_types == self._allowed_types,
            __o._special_values == self._special_values,
            __o._default == self._default,
            __o.description == self.description,
        )

    def __repr__(self) -> str:
        """Get a string representation of the parameter."""
        return (
            f"CalculatorParameter(name={self.name}, "
            f"allowed_types={self._allowed_types!r}, "
            f"special_values={self._special_values!r}, "
            f"default={self._default!r}, description={self.description})"
        )

    def __hash__(self) -> int:
        """Return a hash of the string representation."""
        return hash(repr(self))

    @property
    def allowed_types(self) -> tuple:
        """The allowed types for the parameter."""
        return copy(self._allowed_types)

    @property
    def special_values(self) -> tuple:
        """The special values of the parameter."""
        return deepcopy(self._special_values)

    @property
    def default(self) -> Any:
        """The default value of the parameter."""
        return deepcopy(self._default)

    def __str__(self) -> str:
        """The parameter name."""
        return self.name

    def validate(self, val: Any) -> bool:
        """Validate a parameter value."""
        if val in self._special_values:
            return True

        return self._allowed_types is not None and isinstance(
            val, self._allowed_types
        )


class NumberParameter(CalculatorParameter):
    """A parameter that can be a number."""

    __hash__ = CalculatorParameter.__hash__

    def __init__(
        self,
        *,
        name: str = "",
        allow_floats: bool = False,
        special_values: Iterable[type] | None = None,
        default: Any = None,
        description: str = "",
        number_range: NumberRange = None,
    ) -> None:
        """Initialize a `NumberParameter`.

        Args:
            name: The name of the `NumberParameter`. Defaults to "".
            allow_floats: Whether to allow floats. Defaults to False.
            special_values: An iterable of the special values for the parameter.
                Defaults to None.
            default: The default value for the parameter. Defaults to None.
            description: A description of the parameter. Defaults to "".
            number_range: A `NumberRange` to use to limit the parameter.
                Defaults to None.
        """
        self._number_range = number_range or NumberRange()
        allowed_types = (float, int) if allow_floats else (int,)
        super().__init__(
            name=name,
            allowed_types=allowed_types,
            special_values=special_values,
            default=default,
            description=description,
        )

    def __eq__(self, __o: object) -> bool:
        """Determine if two parameters are equal."""
        if not super().__eq__(__o):
            return False

        return __o._number_range == self._number_range

    def __repr__(self) -> str:
        """Get a string representation of the parameter."""
        return (
            f"NumberParameter(name={self.name}, "
            f"allowed_floats={float in self._allowed_types}, "
            f"special_values={self._special_values!r}, "
            f"default={self._default!r}, "
            f"description={self.description}, "
            f"number_range={self._number_range!r})"
        )

    def as_dict(self) -> dict:
        """Return the `NumberParameter` as a dictionary."""
        return {
            "name": self.name,
            "special_values": self._special_values,
            "default": self.default,
            "description": self.description,
            "_number_range": self._number_range.as_dict(),
            "allowed_types": self._allowed_types,
            "@class": self.__class__.__name__,
            "@module": self.__class__.__module__,
        }

    @classmethod
    def from_dict(cls, d) -> NumberParameter:
        """Initiate a `NumberParameter` from a dictionary."""
        return cls(
            name=d["name"],
            allow_floats=float in d["allowed_types"],
            special_values=d["special_values"],
            default=d["default"],
            description=d["description"],
            number_range=NumberRange.from_dict(d["_number_range"]),
        )

    @property
    def number_range(self) -> NumberRange:
        """The number range of the parameter."""
        return copy(self._number_range)

    def validate(self, val: Any) -> bool:
        """Validate a value."""
        if val in self._special_values:
            return True

        if not isinstance(val, self._allowed_types):
            return False

        if self._number_range is None:
            return True

        return self._number_range.validate_number(val)


class SequenceParameter(CalculatorParameter):
    """A parameter that can be a sequence."""

    __hash__ = CalculatorParameter.__hash__

    def __init__(
        self,
        member_types: Iterable[type],
        name: str = "",
        special_values: Iterable | None = None,
        default: Any = None,
        description: str = "",
    ):
        """Initialize a `SequenceParameter`.

        Args:
            name: The name of the `SequenceParameter`. Defaults to "".
            member_types: The allowed types of the items in the sequence.
            special_values: An iterable of the special values for the parameter.
                Defaults to None.
            default: The default value for the parameter. Defaults to None.
            description: A description of the parameter. Defaults to "".
        """
        self._member_types = tuple(member_types)
        super().__init__(
            name=name,
            allowed_types=(Sequence,),
            special_values=special_values,
            default=default,
            description=description,
        )

    def __eq__(self, __o: object) -> bool:
        """Determine if two parameters are equal."""
        if not super().__eq__(__o):
            return False

        return __o._member_types == self._member_types

    def __repr__(self) -> str:
        """Get a string representation of the parameter."""
        return (
            f"SequenceParameter(member_types={self.member_types!r}, "
            f"name={self.name}, allowed_types={self._allowed_types!r}, "
            f"special_values={self._special_values!r}, "
            f"default={self._default!r}, description={self.description})"
        )

    @property
    def member_types(self) -> Iterable:
        """The allowed member types of the parameter."""
        return copy(self._member_types)

    def as_dict(self) -> dict:
        """Return the `SequenceParameter` as a dictionary."""
        return {
            "name": self.name,
            "special_values": self._special_values,
            "member_types": self.member_types,
            "default": self.default,
            "description": self.description,
            "allowed_types": self._allowed_types,
            "@class": self.__class__.__name__,
            "@module": self.__class__.__module__,
        }

    @classmethod
    def from_dict(cls, d) -> SequenceParameter:
        """Initiate a `SequenceParameter` from a dictionary."""
        return cls(
            member_types=d["member_types"],
            name=d["name"],
            special_values=d["special_values"],
            default=d["default"],
            description=d["description"],
        )

    def validate(self, val: Any) -> bool:
        """Validate a value."""
        if val in self._special_values:
            return True

        if not isinstance(val, self._allowed_types) or isinstance(val, str):
            return False

        return all(isinstance(x, self.member_types) for x in val)


class NumberSequenceParameter(SequenceParameter):
    """A parameter that can be a sequence of numbers."""

    __hash__ = SequenceParameter.__hash__

    def __init__(
        self,
        *,
        name: str = "",
        allow_floats: bool = False,
        special_values: Iterable | None = None,
        default: Any = None,
        description: str = "",
        number_range: NumberRange = None,
    ):
        """Initialize a `NumberSequenceParameter`.

        Args:
            name: The name of the `NumberSequenceParameter`. Defaults to "".
            allow_floats: Whether to allow floats. Defaults to False.
            special_values: An iterable of the special values for the parameter.
                Defaults to None.
            default: The default value for the parameter. Defaults to None.
            description: A description of the parameter. Defaults to "".
            number_range: A `NumberRange` to use to limit the parameter.
                Defaults to None.
        """
        self._number_range = number_range or NumberRange()
        member_types = (float, int) if allow_floats else (int,)
        super().__init__(
            name=name,
            member_types=member_types,
            special_values=special_values,
            default=default,
            description=description,
        )

    def __eq__(self, __o: object) -> bool:
        """Determine if two parameters are equal."""
        if not super().__eq__(__o):
            return False

        return __o._number_range == self._number_range

    def __repr__(self) -> str:
        """Get a string representation of the parameter."""
        return (
            f"NumberSequenceParameter(name={self.name}, "
            f"allow_floats={float in self.member_types}, "
            f"special_values={self._special_values}, "
            f"default={self._default!r}, description={self.description}, "
            f"number_range={self._number_range!r})"
        )

    def as_dict(self) -> dict:
        """Return the `NumberSequenceParameter` as a dictionary."""
        d = super().as_dict()
        del d["member_types"]
        d["allow_floats"] = float in self.member_types
        d["_number_range"] = self._number_range.as_dict()
        return d

    @classmethod
    def from_dict(cls, d) -> NumberSequenceParameter:
        """Initiate a `SequenceParameter` from a dictionary."""
        return cls(
            name=d["name"],
            allow_floats=d["allow_floats"],
            special_values=d["special_values"],
            default=d["default"],
            description=d["description"],
            number_range=NumberRange.from_dict(d["_number_range"]),
        )

    def validate(self, val: Any) -> bool:
        """Validate a value."""
        if val in self._special_values:
            return True

        if not isinstance(val, self._allowed_types) or isinstance(val, str):
            return False

        for x in val:
            if not isinstance(x, self.member_types):
                return False

            if not self._number_range.validate_number(x):
                return False

        return True


class MappingParameter(CalculatorParameter):
    """A parameter that can be a mapping."""

    __hash__ = CalculatorParameter.__hash__

    def __init__(
        self,
        *,
        member_types: Iterable[type],
        name: str = "",
        special_values: Iterable | None = None,
        default: Any = None,
        description: str = "",
    ):
        """Initialize a `MappingParameter`.

        Args:
            name: The name of the `MappingParameter`. Defaults to "".
            member_types: The allowed types of the items in the sequence.
            special_values: An iterable of the special values for the parameter.
                Defaults to None.
            default: The default value for the parameter. Defaults to None.
            description: A description of the parameter. Defaults to "".
        """
        self._member_types = tuple(member_types)
        super().__init__(
            name=name,
            allowed_types=(Mapping,),
            special_values=special_values,
            default=default,
            description=description,
        )

    def __eq__(self, __o: object) -> bool:
        """Determine if two parameters are equal."""
        if not super().__eq__(__o):
            return False

        return __o._member_types == self._member_types

    def __repr__(self) -> str:
        """Get a string representation of the parameter."""
        return (
            f"MappingParameter(name={self.name}, "
            f"member_types={self.member_types!r}, "
            f"special_values={self._special_values!r}, "
            f"default={self._default!r}, "
            f"description={self.description})"
        )

    @property
    def member_types(self) -> Iterable:
        """The allowed member types of the parameter."""
        return copy(self._member_types)

    def as_dict(self) -> dict:
        """Return the `MappingParameter` as a dictionary."""
        return {
            "member_types": self.member_types,
            "name": self.name,
            "special_values": self._special_values,
            "default": self.default,
            "description": self.description,
            "@class": self.__class__.__name__,
            "@module": self.__class__.__module__,
        }

    @classmethod
    def from_dict(cls, d) -> MappingParameter:
        """Initiate a `MappingParameter` from a dictionary."""
        return cls(
            member_types=d["member_types"],
            name=d["name"],
            special_values=d["special_values"],
            default=d["default"],
            description=d["description"],
        )

    def validate(self, val: Any) -> bool:
        """Validate a value."""
        if val in self._special_values:
            return True

        if not isinstance(val, self._allowed_types):
            return False

        return all(isinstance(x, self.member_types) for x in val.values())


class NumberMappingParameter(MappingParameter):
    """A parameter that can be a mapping to numbers."""

    __hash__ = MappingParameter.__hash__

    def __init__(
        self,
        *,
        name: str = "",
        allow_floats: bool = False,
        special_values: Iterable | None = None,
        default: Any = None,
        description: str = "",
        number_range: NumberRange = None,
    ):
        """Initialize a `NumberMappingParameter`.

        Args:
            name: The name of the `NumberMappingParameter`. Defaults to "".
            allow_floats: Whether to allow floats. Defaults to False.
            special_values: An iterable of the special values for the parameter.
                Defaults to None.
            default: The default value for the parameter. Defaults to None.
            description: A description of the parameter. Defaults to "".
            number_range: A `NumberRange` to use to limit the parameter.
                Defaults to None.
        """
        self._number_range = number_range
        member_types = (float, int) if allow_floats else (int,)
        super().__init__(
            name=name,
            member_types=member_types,
            special_values=special_values,
            default=default,
            description=description,
        )

    def __eq__(self, __o: object) -> bool:
        """Determine if two parameters are equal."""
        if not super().__eq__(__o):
            return False

        return __o._number_range == self._number_range

    def __repr__(self) -> str:
        """Get a string representation of the parameter."""
        return (
            f"NumberMappingParameter(name={self.name}, "
            f"allow_floats=({float in self.member_types}, "
            f"special_values={self._special_values!r}, "
            f"default={self._default!r}, "
            f"description={self.description}, "
            f"number_range={self._number_range!r}))"
        )

    def as_dict(self) -> dict:
        """Return the `NumberMappingParameter` as a dictionary."""
        d = super().as_dict()
        del d["member_types"]
        d["allow_floats"] = float in self.member_types
        d["_number_range"] = self._number_range.as_dict()
        return d

    @classmethod
    def from_dict(cls, d) -> NumberMappingParameter:
        """Initiate a `NumberMappingParameter` from a dictionary."""
        return cls(
            name=d["name"],
            allow_floats=d["allow_floats"],
            special_values=d["special_values"],
            default=d["default"],
            description=d["description"],
            number_range=NumberRange.from_dict(d["_number_range"]),
        )

    def validate(self, val: Any) -> bool:
        """Validate a value."""
        if val in self._special_values:
            return True

        if not isinstance(val, self._allowed_types):
            return False

        if self._number_range is None:
            return True

        for x in val.values():
            if not isinstance(x, self.member_types):
                return False

            if not self._number_range.validate_number(x):
                return False

        return True
