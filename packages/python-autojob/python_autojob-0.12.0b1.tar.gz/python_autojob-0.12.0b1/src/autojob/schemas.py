"""Custom schemas."""

import logging
from typing import Annotated
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import PlainSerializer
from pydantic import computed_field
from pydantic import field_validator
from pymatgen.core.periodic_table import Element
from pymatgen.io.vasp import Chgcar
from typing_extensions import TypedDict

from autojob.calculation.parameters import CalculatorType
from autojob.coordinator.classification import CalculationType
from autojob.coordinator.classification import StudyType
from autojob.utils.schemas import PydanticAtoms

logger = logging.getLogger(__name__)


_T = TypeVar("_T")

StringSerialized = Annotated[
    _T, PlainSerializer(lambda x: str(x), return_type=str)
]


class _BondedToDict(TypedDict):
    index: int
    element: StringSerialized[Element]
    bond_order: float
    direction: tuple[float, float, float]
    spin_polarization: float


class _BondOrders(TypedDict):
    element: StringSerialized[Element]
    bonded_to: list[_BondedToDict]
    bond_order_sum: float


BondOrderDict = dict[int, _BondOrders]


class BaderData(TypedDict):
    """Bader change analysis data."""

    atomic_vol: float
    min_dist: float
    charge: float
    x: float
    y: float
    z: float


class BaderDensity(TypedDict):
    """Bader density data."""

    data: list[list[float]]
    shift: list[float]
    dim: list[float]


class BaderAnalysis(TypedDict):
    """Bader change analysis data."""

    data: BaderData
    vacuum_volume: float
    vacuum_charge: float
    nelectrons: int
    chgcar: Chgcar
    atomic_densities: list[BaderDensity]


class DDEC6Analysis(TypedDict):
    """DDEC6 analysis data."""

    partial_charges: list[float]
    spin_moments: list[float]
    dipoles: list[float]
    rsquared_moments: list[float]
    rcubed_moments: list[float]
    rfourth_moments: list[float]
    bond_order_dict: BondOrderDict


class CalculationModel(BaseModel):
    """An alternative representation of a calculation."""

    # Metadata
    study_group_id: str = Field(alias="Study Group ID")
    study_id: str = Field(alias="Study ID")
    calculation_id: str = Field(alias="Calculation ID")
    job_id: str = Field(alias="Job ID")
    slurm_job_id: int | None = Field(default=None, alias="SLURM Job ID")
    sources: list[str]

    study_group_name: str = Field(alias="Study Group Name")
    study_name: str = Field(alias="Study Name")
    calculation_name: str = Field(alias="Calculation Name")
    job_name: str = Field(alias="Job Name")

    study_group_notes: str = Field(alias="Study Group Notes")
    study_notes: str = Field(alias="Study Notes")
    calculation_notes: str = Field(alias="Calculation Notes")
    job_notes: str = Field(alias="Job Notes")

    calculation_type: StringSerialized[CalculationType] = Field(
        alias="Calculation Type",
    )
    calculator_type: StringSerialized[CalculatorType] = Field(
        alias="Calculator Type"
    )
    study_type: StringSerialized[StudyType] = Field(alias="Study Type")

    # Structural Metadata
    structure: str = Field(alias="Structure")
    base_structure: str | None = Field(default=None, alias="Base Structure")
    final_atoms: PydanticAtoms | None = Field(
        default=None, alias="Final Atoms"
    )
    energy: float | None = None
    max_force: float | None = Field(default=None, alias="max force")

    # Mechanistic Metadata
    adsorbate: str | None = Field(default=None, alias="Adsorbate")
    adsorbed: bool = False
    initial_site: str | None = Field(default=None, alias="Site")
    adsorbate_migration: str | None = Field(
        default=None, alias="Adsorbate Migration"
    )
    orientation: str | None = Field(default=None, alias="Orientation")
    integrity: bool = Field(default=True, alias="Adsorbate Integrity")

    # Thermodynamic Analysis
    entropic_correction: float | None = Field(
        default=None, alias="TS Correction"
    )
    zero_point_energy: float | None = Field(
        default=None, alias="Zero-Point Energy"
    )
    vibrational_frequencies: list[float] | None = Field(
        default=None, alias="Frequencies"
    )

    # Charge Analysis
    charges: list[float] | None = Field(default=None, alias="Charges")
    bond_orders: BondOrderDict | None = Field(
        default=None, alias="Bond Orders"
    )
    spin_densities: list[float] | None = Field(
        default=None, alias="Spin Densities"
    )

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    @field_validator("structure")
    @classmethod
    def remove_unit_cell_suffix(cls, v: str) -> str:
        """Remove the unit cell suffix from structure names."""
        return v.removesuffix("_unit_cell")

    @field_validator("adsorbate_migration")
    @classmethod
    def validate_initial_site(cls, v: str) -> str | None:
        """Validate the initial site."""
        return v if v else None

    @field_validator("adsorbed", mode="before")
    @classmethod
    def validate_adsorbed(cls, v: str) -> bool:
        """Validate `adsorbed`."""
        return v == "Y"

    @field_validator("integrity", mode="before")
    @classmethod
    def validate_integrity(cls, v: str) -> bool:
        """Validate `integrity`."""
        return not bool(v)

    @computed_field  # type: ignore[misc]
    @property
    def final_site(self) -> str | None:
        """Determine the final site of the calculation."""
        return self.adsorbate_migration or self.initial_site

    @computed_field  # type: ignore[misc]
    @property
    def free_energy(self) -> float | None:
        """Calculate the free energy of the calculation."""
        if None in (
            self.energy,
            self.entropic_correction,
            self.zero_point_energy,
        ):
            logger.warning(
                "Either the energy, the entropic correction, or the "
                "zero-point energy is not defined. Returning the DFT energy"
            )
            return self.energy
        return self.energy + self.entropic_correction + self.zero_point_energy  # type: ignore[operator]
