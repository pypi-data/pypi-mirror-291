"""DEPRECATED: metaclasses are not needed, CalculatorType and StudyType.

are in calculation and study, respectively. CalculationTypes should be
implemented as class-level constants in calculation (or separate modules)
as subclasses of Calculation.
"""

from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from enum import EnumMeta
from enum import unique


class ABCEnumMeta(ABCMeta, EnumMeta):  # type: ignore
    """A metaclass for abstract base classes for enums."""

    def __new__(cls, *args, **kw):
        """Create enum with abstract methods.

        Raises:
            TypeError: Missing abstract methods.

        Returns:
            The created class instance.
        """
        abstract_enum_cls = super().__new__(cls, *args, **kw)
        # Only check abstractions if members were defined.
        if abstract_enum_cls._member_map_:
            try:  # Handle existence of undefined abstract methods.
                absmethods = list(abstract_enum_cls.__abstractmethods__)
                if absmethods:
                    missing = ", ".join(f"{method!r}" for method in absmethods)
                    plural = "s" if len(absmethods) > 1 else ""
                    error_string = (
                        "cannot instantiate abstract "
                        f"class {abstract_enum_cls.__name__}"
                        f" with abstract method{plural} {missing}"
                    )
                    raise TypeError(error_string)
            except AttributeError:
                pass
        return abstract_enum_cls


# TODO: replace with list of module-level variables of implemented instances
class ImplementableEnum(Enum, metaclass=ABCEnumMeta):
    """An `Enum` that can be implemented."""

    @abstractmethod
    def is_implemented(self) -> bool:
        """Indicates if particular feature is implemented or not.

        Returns:
            bool: True if feature is implemented. False otherwise.
        """

    @abstractmethod
    def is_default(self) -> bool:
        """Determine if ImplementableEnum is default value.

        Returns:
            ImplementableEnum: True if the ImplementableEnum is the default
            value.
        """


@unique
class CalculatorType(ImplementableEnum):
    """Types of calculators."""

    ABINIT = "abinit"
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

    def __str__(self) -> str:
        """A string representation of the calculator."""
        return self.value

    def is_implemented(self) -> bool:
        """Returns if the ``CalculatorType`` is implemented or not."""
        implemented_calculator_types = [
            CalculatorType.VASP,
            CalculatorType.GAUSSIAN,
        ]

        return self in implemented_calculator_types

    def is_default(self) -> bool:
        """Returns the default ``CalculatorType``."""
        return self == CalculatorType.VASP


@unique
class CalculationType(ImplementableEnum):
    """A type of calculation."""

    RELAXATION = "relaxation"
    DOS = "density of states"
    VIB = "vibrational analysis"
    EOS = "equation of state"
    MD = "molecular dynamics"

    def __str__(self) -> str:
        """A string representation of the ``CalculationType``."""
        return self.value

    def is_implemented(self) -> bool:
        """Returns if the ``CalculationType`` is implemented or not."""
        implemented_calculation_types = [CalculationType.RELAXATION]

        return self in implemented_calculation_types

    def is_default(self) -> bool:
        """Returns the default ``CalculationType``."""
        return self == CalculationType.RELAXATION


@unique
class StudyType(ImplementableEnum):
    """A type of study."""

    ADSORPTION = "adsorption"
    MECHANISM = "mechanism"
    SENSITIVITY = "sensitivity"

    def __str__(self) -> str:
        """A string representation of the ``StudyType``."""
        return self.value

    def is_implemented(self) -> bool:
        """Returns if the ``StudyType`` is implemented or not."""
        implemented_study_types = [StudyType.ADSORPTION, StudyType.SENSITIVITY]

        return self in implemented_study_types

    def is_default(self) -> bool:
        """Returns the default ``StudyType``."""
        return self == StudyType.SENSITIVITY
