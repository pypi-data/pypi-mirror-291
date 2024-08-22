"""Harvest metadata from directories."""

import json
import logging
from pathlib import Path
from typing import Any

from autojob import SETTINGS
from autojob.utils.files import find_calculation_dirs
from autojob.utils.files import find_study_dirs
from autojob.utils.files import find_study_group_dirs
from autojob.utils.files import get_slurm_job_id

logger = logging.getLogger(__name__)


def _load_study_group_metadata(dir_name: str | Path) -> dict[str, Any]:
    """Load study group metadata."""
    logger.info(f"Loading study group metadata from {dir_name!s}")
    study_group_dirs = find_study_group_dirs(Path(dir_name))
    metadata = {}
    for study_group_dir in study_group_dirs:
        metadata_file = study_group_dir.joinpath(SETTINGS.STUDY_GROUP_FILE)
        with metadata_file.open(mode="r", encoding="utf-8") as file:
            metadata[study_group_dir.name] = json.load(file)
    logger.info(f"Successfully loaded study metadata from {dir_name!s}")
    return metadata


def _load_study_metadata(dir_name: str | Path) -> dict[str, Any]:
    """Load study metadata."""
    logger.info(f"Loading study metadata from {dir_name!s}")
    study_dirs = find_study_dirs(dir_name)
    metadata = {}
    for study_dir in study_dirs:
        metadata_file = study_dir.joinpath(SETTINGS.STUDY_FILE)
        with metadata_file.open(mode="r", encoding="utf-8") as file:
            metadata[study_dir.name] = json.load(file)
    logger.info(f"Successfully loaded study metadata from {dir_name!s}")
    return metadata


def _load_calculation_metadata(dir_name: str | Path) -> dict[str, Any]:
    """Load calculation metadata."""
    logger.info(f"Loading calculation metadata from {dir_name!s}")
    calculation_dirs = find_calculation_dirs(dir_name)
    metadata = {}
    for calculation_dir in calculation_dirs:
        metadata_file = calculation_dir.joinpath(SETTINGS.CALCULATION_FILE)
        with metadata_file.open(mode="r", encoding="utf-8") as file:
            metadata[calculation_dir.name] = json.load(file)
    logger.info(f"Successfully loaded calculation metadata from {dir_name!s}")
    return metadata


def load_job_metadata(
    *,
    dir_name: str | Path,
    study_group_name: str,
    study_group_notes: str,
    study_name: str,
    study_notes: str,
    calculation_name: str,
    calculation_notes: str,
) -> dict[str, Any]:
    """Load job metadata from job directory.

    The job.json file must be present in `dir_name`.

    Args:
        dir_name: The directory containing the job metadata.
        study_group_name: The name of the study group.
        study_group_notes: The study group notes.
        study_name: The name of the study.
        study_notes: The study notes.
        calculation_name: The name of the calculation.
        calculation_notes: The calculation notes.

    Returns:
        A dictionary containing job metadata.
    """
    logger.debug(f"Loading job metadata from {dir_name!s}")
    job_file = Path(dir_name).joinpath(SETTINGS.JOB_FILE)
    metadata = {}
    try:
        with job_file.open(mode="r", encoding="utf-8") as file:
            metadata.update(json.load(file))

        metadata["SLURM Job ID"] = get_slurm_job_id(dir_name)
        logger.debug(f"Successfully loaded job metadata from {job_file!s}")
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning(f"Unable to job metadata from {job_file!s}")

    metadata.update(
        {
            "Study Group Name": study_group_name,
            "Study Group Notes": study_group_notes,
            "Study Name": study_name,
            "Study Notes": study_notes,
            "Calculation Name": calculation_name,
            "Calculation Notes": calculation_notes,
            # ! Related to bug with mislabeled job.json Job IDs due to
            # ! run_vibration
            "Job ID": getattr(dir_name, "name", dir_name),
        }
    )
    metadata["Job Name"] = metadata.pop("Name", "")
    metadata["Job Notes"] = metadata.pop("Notes", "")
    return metadata
