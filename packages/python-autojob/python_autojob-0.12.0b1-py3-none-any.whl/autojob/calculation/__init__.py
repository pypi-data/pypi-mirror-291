"""Store the results of a :class:`~.task.Task` representing a calculation."""

import logging

from ase import Atoms

logger = logging.getLogger(__name__)


def copy_atom_metadata(input_atoms: Atoms | None, output_atoms: Atoms) -> None:
    """Copy tags, constraints, and info from the input to output atoms.

    This function modifies `output_atoms` in place.

    Args:
        input_atoms: An :class:`ase.atoms.Atoms` object.
        output_atoms: An :class:`ase.atoms.Atoms` object.
    """
    if input_atoms is None:
        logger.warning("Unable to copy atom metadata")
    else:
        logger.info("Copying atom metadata")
        output_atoms.set_constraint(constraint=input_atoms.constraints)
        output_atoms.set_tags(tags=input_atoms.get_tags())
        output_atoms.info = input_atoms.info
        logger.info("Successfully copied atom metadata")
