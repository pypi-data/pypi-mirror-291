"""VASP calculation output utilities.

This module provides the :func:`load_calculation_outputs`
and :func:`get_output_atoms` functions for retrieving
calculation outputs and output atoms from the directory
of a VASP calculation.

Example:
    from pathlib import Path
    from autojob.calculation.vasp import vasp

    outputs = vasp.load_calculation_outputs(Path.cwd())
    atoms = vasp.get_output_atoms(Path.cwd())
"""

import logging
import pathlib
from typing import Any
from typing import TypedDict
from xml.etree import ElementTree

from ase import Atoms
import ase.io
from emmet.core.tasks import TaskDoc
from emmet.core.tasks import TaskState

from autojob import SETTINGS
from autojob.calculation import copy_atom_metadata

logger = logging.getLogger(__name__)

ALTERNATE_OUTPUT_STRUCTURES = ("relax.traj", "vasprun.xml", "CONTCAR")
FILES_TO_CARRYOVER = ("CHGCAR", "WAVECAR")
VOLUMETRIC_FILES = ("CHGCAR", "LOCPOT", "AECCAR0", "AECCAR1", "AECCAR2")


def load_calculation_outputs(
    dir_name: str | pathlib.Path,
) -> dict[str, Any]:
    """Load VASP calculation outputs from a directory.

    Args:
        dir_name: The directory from which to load VASP outputs.

    Returns:
        A dictionary with, at minimum, the required keys to initialize
        a :class:`autojob.calculation.calculation.Calculation` but
        also with same keys as an instance of
        :class:`emmet.core.tasks.OutputDoc`.
    """
    logger.info(f"Loading VASP calculation outputs from {dir_name}")
    doc = TaskDoc.from_directory(dir_name)
    outputs = doc.output.model_dump() if doc.output else {}
    _ = outputs.pop("structure", None)
    analysis = doc.analysis.model_dump()
    vasp_objects = doc.vasp_objects
    logger.debug(
        f"Successfully loaded VASP calculation outputs from {dir_name}"
    )
    return {
        **outputs,
        "analysis": analysis,
        "calculation_objects": vasp_objects,
        "converged": doc.state == TaskState.SUCCESS,
    }


# TODO: Unit test
def _reorder_atoms(output_atoms: Atoms, dir_name: str | pathlib.Path) -> Atoms:
    """Creates a new Atoms object reordered according to ase-sort.dat.

    This function assumes that the Atoms object passed is ordered in
    accordance to the POSCAR/POTCAR.
    """
    logger.debug("Reordering atoms")
    sort_file = pathlib.Path(dir_name).joinpath("ase-sort.dat")

    with pathlib.Path(sort_file).open(mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    conversion_table = [int(line.split()[0]) for line in lines]
    new_ordering = [conversion_table[atom.index] for atom in output_atoms]
    atoms = [output_atoms[i] for i in new_ordering]

    logger.debug(
        "Successfully reordered atoms: "
        f"{[atom.index for atom in output_atoms]!r} -> {new_ordering!r}"
    )
    return Atoms(
        atoms,
        cell=output_atoms.cell,
        pbc=output_atoms.pbc,
        celldisp=output_atoms.get_celldisp(),
    )


def get_output_atoms(
    dir_name: str | pathlib.Path,
    alt_filename_index: int | None = None,
    input_atoms: Atoms | None = None,
) -> Atoms:
    """Retrieve an Atoms object representing the output structure.

    This function also copies tags and constraints from the input structure
    in the case that the output structure must be read from a non-ASE file
    (e.g., vasprun.xml).

    Args:
        dir_name: The directory from which to retrieve the output structure.
        alt_filename_index: An integer pointing to which alternative structure
            file should be used. This number will be used to index
            `ALTERNATE_OUTPUT_STRUCTURES`.
        input_atoms: An Atoms object representing the corresponding input
            structure.

    Returns:
        An Atoms object representing the output structure.
    """
    if alt_filename_index is None:
        alt_filename_index = 0
        filename = SETTINGS.OUTPUT_ATOMS
    else:
        filename = ALTERNATE_OUTPUT_STRUCTURES[alt_filename_index]
        alt_filename_index += 1

    full_filename = pathlib.Path(dir_name).joinpath(filename)

    logger.debug(f"Retrieving output atoms from {full_filename}")
    atoms = None

    try:
        atoms = ase.io.read(full_filename)
    except (FileNotFoundError, AttributeError, ElementTree.ParseError):
        msg = (
            f"Unable to retrieve atoms from: {full_filename}.\n"
            "File not found."
        )
        logger.warning(msg)
        try:
            atoms = get_output_atoms(
                dir_name=dir_name,
                alt_filename_index=alt_filename_index,
                input_atoms=input_atoms,
            )
            atoms = _reorder_atoms(output_atoms=atoms, dir_name=dir_name)
            copy_atom_metadata(
                input_atoms=input_atoms,
                output_atoms=atoms,
            )
        except IndexError as err:
            msg = (
                f"No output atoms found in {SETTINGS.OUTPUT_ATOMS} or "
                f"{ALTERNATE_OUTPUT_STRUCTURES!r}"
            )
            raise FileNotFoundError(msg) from err
        except FileNotFoundError:
            if atoms is None:
                raise
            logger.warning("Unable to reorder atoms")

    logger.debug(f"Successfully retrieved output atoms from {full_filename}")
    return atoms


class VaspParameters(TypedDict):
    """VASP calculator parameters."""
