"""Extract structural metadata."""

from contextlib import suppress
import logging
from pathlib import Path
import re
from typing import Any

import ase.io
from ase.io.formats import UnknownFileTypeError

from autojob import SETTINGS
from autojob.utils.files import extract_structure_name

logger = logging.getLogger(__name__)

_re_adsorbate_complex = re.compile(
    r"(?P<structure>.+)_((?P<adsorbate>[A-Za-z]+)_)?(?P<site>((on_[A-Za-z]{1,2}(_linker)?)|between_linkers))(_(?P<orientation>perpendicular|parallel|co(l){1,2}inear_with_[A-Za-z]{1,2}|vertical)?(_\w+))?"
)
ADSORBATE_TAG = -99


def load_structural_data(dir_name: str | Path) -> dict[str, Any]:
    """Extract the structural data from the input structure of the directory.

    Args:
        dir_name: The directory of the completed calculation.

    Returns:
        The structural data. The following keys are guaranteed to be present in
        the returned dictionary:

        - ``"Structure"``
        - ``"Base Structure"``: only assigned if extracted from adsorbate complex name
        - ``"Adsorbate"``
        - ``"Site"``
        - ``"Orientation"``

        If no data is found, every value will be None.
    """
    logger.info(f"Loading structural data for {dir_name!s}")
    python_script = Path(dir_name).joinpath(SETTINGS.PYTHON_SCRIPT)
    structure = base_structure = adsorbate = site = orientation = None

    if python_script.exists():
        with python_script.open(mode="r", encoding="utf-8") as file:
            structure_name = extract_structure_name(file)
            structure = structure_name.removeprefix("./").removesuffix(".traj")

        if match := _re_adsorbate_complex.match(structure):
            base_structure, adsorbate, site, orientation = match.group(
                "structure", "adsorbate", "site", "orientation"
            )

    if None in (structure, adsorbate):
        with suppress(FileNotFoundError, UnknownFileTypeError):
            atoms = ase.io.read(
                Path(dir_name).joinpath(f"{structure or 'in'}.traj")
            )
            structure = structure or str(atoms.symbols)
            adsorbate = adsorbate or "".join(
                x.symbol for x in atoms if x.tag == ADSORBATE_TAG
            )

    # ! Patch for misnamed structures
    if structure:
        structure = structure.replace("HAB", "HIB")
    if base_structure:
        base_structure = base_structure.replace("HAB", "HIB")

    # TODO: Adsorbed?

    # Nearest catalyst atom (and distance)
    final_structure = dir_name.joinpath("final.traj")
    final_atoms = (
        ase.io.read(final_structure) if final_structure.exists() else None
    )

    data = {
        "Structure": structure,
        "Base Structure": base_structure,
        "Adsorbate": adsorbate,
        "Site": site if site is None else site.strip("_"),
        "Orientation": orientation,
        "Final Atoms": final_atoms,
    }

    if None in list(data.values()):
        none = ", ".join(k for k, v in data.items() if v is None)
        logger.warning(
            f"Unable to load structural data for {dir_name!s}. "
            f"The following values are None: {none}"
        )
    else:
        logger.info(f"Successfully loaded structural data for {dir_name!s}")
    return data
