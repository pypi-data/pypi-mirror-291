"""Read and standardize Gaussian outputs."""

import logging
import pathlib
from typing import Any
from typing import TypedDict

from ase import Atoms
import ase.io
from ase.io.formats import UnknownFileTypeError
import cclib
from cclib.parser.data import ccData

from autojob import SETTINGS
from autojob.calculation import copy_atom_metadata

logger = logging.getLogger(__name__)

ALTERNATE_OUTPUT_STRUCTURES = ("relax.traj", "Gaussian.log")
FILES_TO_CARRYOVER = ["Gaussian.chk"]
GAUSSIAN_LOG = "Gaussian.log"


def load_calculation_outputs(
    dir_name: str | pathlib.Path,
) -> dict[str, Any]:
    """Load calculation outputs for a Gaussian calculation.

    Note that all quantities other than the final energy are reported in atomic
    units (Hartree/Bohr).

    Args:
        dir_name: The directory containing the Gaussian output files.

    Returns:
        A dictionary containing Gaussian calculation outputs.
    """
    logger.debug(
        f"Loading calculation outputs for Gaussian calculation in: {dir_name}"
    )
    log_file = pathlib.Path(dir_name).joinpath(GAUSSIAN_LOG)
    outputs = {"forces": None, "energy": None}

    if not log_file.exists():
        logger.warning(
            f"Gaussian output file {GAUSSIAN_LOG} does not exist in {dir_name}"
        )
    elif data := cclib.io.ccread(log_file):
        data.listify()
        outputs.update(data.getattributes())
        outputs["converged"] = bool(
            # optimization statuses are defined in bit value notation
            getattr(data, "optstatus", False)
            and (data.optstatus[-1] & ccData.OPT_DONE)
        )

        if forces := outputs.get("grads"):
            outputs["forces"] = forces[-1] if forces else None

        if energies := outputs.get("scfenergies"):
            outputs["energy"] = energies[-1] if energies else None

        logger.debug(
            "Successfully loaded calculation outputs for Gaussian calculation "
            f"in: {dir_name}"
        )
    else:
        logger.warning(f"Unable to parse Gaussian outputs from {dir_name}")

    return outputs


def get_output_atoms(
    dir_name: str | pathlib.Path,
    alt_filename_index: int | None = None,
    input_atoms: Atoms | None = None,
) -> Atoms:
    """Retrieve an ``Atoms`` object representing the output structure.

    This function also copies tags and constraints from the input structure
    in the case that the output structure must be read from a non-ASE file
    (e.g., ``Gaussian.log``).

    Args:
        dir_name: The directory from which to retrieve the output structure.
        alt_filename_index: An integer pointing to which alternative structure
            file should be used. This number will be used to index
            ``ALTERNATE_OUTPUT_STRUCTURES``.
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

    try:
        atoms = ase.io.read(full_filename)
        logger.debug(
            f"Successfully retrieved output atoms from {full_filename}"
        )
    except (FileNotFoundError, AttributeError, UnknownFileTypeError):
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

    return atoms


class GaussianParameters(TypedDict):
    """WIP."""
