"""Harvest charge analysis results from completed task directory."""

import logging
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

import ase
from ase.geometry import geometry
from pymatgen.command_line.chargemol_caller import ChargemolAnalysis

from autojob.utils.files import extract_structure_name

if TYPE_CHECKING:
    from autojob.schemas import BondOrderDict

logger = logging.getLogger(__name__)

DDEC_NET_ATOMIC_CHARGE_FILE = "DDEC6_even_tempered_net_atomic_charges.xyz"


def get_ddec6_index_map(dir_name: str | Path) -> list[int]:
    """Return a list of integers mapping DDEC6 indices to ASE indices.

    The ASE index of the atom at index i in the DDEC6 structure can be found
    as follows:

        index_map = get_ddec6_index_map(dir_name)
        index = index_map[i]

    Args:
        dir_name: The directory containing a calculation.
    """
    with (
        Path(dir_name)
        .joinpath("run.py")
        .open(mode="r", encoding="utf-8") as python_script
    ):
        input_traj = extract_structure_name(python_script).removeprefix("./")

    ase_atoms = ase.io.read(Path(dir_name).joinpath(input_traj))
    ase_atoms.center()

    xyz_file = Path(dir_name).joinpath(DDEC_NET_ATOMIC_CHARGE_FILE)
    ddec_atoms = ase.io.read(xyz_file)
    ddec_atoms.cell = ase_atoms.cell
    ddec_atoms.center()

    ddec6_index_map = []

    for atom in ddec_atoms:
        closest_ase_atom = ase_atoms[0]
        _, min_distance = geometry.get_distances(
            [atom.position],
            [ase_atoms[0].position],
            cell=ddec_atoms.cell,
            pbc=True,
        )

        for ase_atom in ase_atoms:
            _, distance = geometry.get_distances(
                [atom.position],
                [ase_atom.position],
                cell=ddec_atoms.cell,
                pbc=True,
            )
            if distance <= min_distance:
                closest_ase_atom = ase_atom
                min_distance = distance

        ddec6_index_map.append(closest_ase_atom.index)

    if len(ddec6_index_map) != len(set(ddec6_index_map)):
        msg = (
            f"DDEC6 map is incomplete for calculation in directory: {dir_name}"
        )
        raise RuntimeError(msg)

    return ddec6_index_map


def load_ddec6_data(dir_name: str | Path) -> dict[str, Any]:
    """Extract the DDEC6 data from the job directory.

    Args:
        dir_name: The directory of the completed calculation.

    Returns:
        The DDEC6 data. The following keys are guaranteed to be present in
        the returned dictionary:
        - "Charges"
        - "Spin Densities"
        - "Bond Orders"

        If no data is found, every value will be None.
    """
    logger.info(f"Loading DDEC6 data for {dir_name!s}")
    charges = spin_densities = bond_orders = None
    try:
        analysis = ChargemolAnalysis(path=dir_name, run_chargemol=False)
        ddec6_index_map = get_ddec6_index_map(dir_name)
        charges = [0.0] * len(ddec6_index_map)
        spin_densities = [0.0] * len(ddec6_index_map)
        bond_orders: BondOrderDict = {}

        for ddec_index, ase_index in enumerate(ddec6_index_map):
            charges[ase_index] = analysis.ddec_charges[ddec_index]
            spin_densities[ase_index] = analysis.ddec_spin_moments[ddec_index]
            bond_orders[ase_index] = analysis.bond_order_dict[ddec_index]

        for bond_order in bond_orders.values():
            for bonded_to in bond_order["bonded_to"]:
                bonded_to["index"] = ddec6_index_map[bonded_to["index"]]

        logger.info(f"Successfully loaded DDEC6 data for {dir_name!s}")

    except FileNotFoundError:
        logger.warning(f"Unable to load DDEC6 data for {dir_name!s}")

    return {
        "Charges": charges,
        "Spin Densities": spin_densities,
        "Bond Orders": bond_orders,
    }
