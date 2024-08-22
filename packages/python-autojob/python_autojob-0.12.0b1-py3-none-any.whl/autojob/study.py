"""Create studies."""

from __future__ import annotations

from enum import Enum
import logging
from typing import TYPE_CHECKING

import monty

from autojob import SETTINGS

if TYPE_CHECKING:
    import datetime

TASK_FILES = {
    "scheduler_script": (SETTINGS.SLURM_SCRIPT, True),
    "job_script": (SETTINGS.PYTHON_SCRIPT, True),
}

logger = logging.getLogger(__name__)


class StudyType(Enum):
    """A tyype of study."""

    ADSORPTION = "adsorption"
    MECHANISM = "mechanism"
    SENSITIVITY = "sensitivity"

    DEFAULT = "sensitivity"  # noqa: PIE796

    def __str__(self) -> str:
        """A string representation of a ``StudyType``."""
        return self.value

    def is_implemented(self) -> bool:
        """Whether or not a ``StudyType`` is implemented."""
        implemented_study_types = [StudyType.SENSITIVITY]

        return self in implemented_study_types


class Study(monty.json.MSONable):
    """A collection of calculations."""

    def __init__(
        self,
        calculations: list[str],
        date_created: datetime.datetime,
        study_id: str,
        study_group_id: str,
        name: str = "",
        notes: str = "",
        study_type: StudyType | None = None,
    ):
        """Initialize a study.

        Args:
            calculations: A list of ``Calculation`` s.
            date_created: The date the study was created.
            study_id: The study ID.
            study_group_id: The study group ID of the study.
            name: The name of the study. Defaults to "".
            notes: Notes on the study. Defaults to "".
            study_type: The ``StudyType``. Defaults to None.
        """
        self._calculations = calculations
        self.date_created = date_created
        self.study_id = study_id
        self.study_group_id = study_group_id
        self.study_type = study_type

        self.name = name or self.create_name()
        self.notes = notes

    def create_name(self) -> str:
        """Create a study name."""
        prefix = ""

        if self.study_type:
            prefix = f"{str(self.study_type).capitalize()} Study-"

        return prefix + self.study_id
