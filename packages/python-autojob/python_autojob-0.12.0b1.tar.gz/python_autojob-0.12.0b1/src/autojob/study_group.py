"""Create study groups."""

import datetime
import pathlib
from typing import TypeVar

from monty import json
from monty import serialization
from shortuuid import uuid

from autojob import study

S = TypeVar("S", bound="StudyGroup")


class StudyGroup(json.MSONable):
    """A collection of studies."""

    def __init__(
        self,
        date_created: datetime.datetime | None = None,
        study_group_id: str = "",
        studies: list[study.Study] | None = None,
        name: str = "",
        notes: str = "",
    ):
        """Initialize a study group.

        Args:
            date_created: The date the study group was created. Defaults to
                the current time.
            study_group_id: The study group ID. A new ID is created if None.
            studies: A list of stuides belonging to the study group. Defaults
                to "".
            name: The name of the study group. Defaults to "".
            notes: The notes on the study group. Defaults to "".
        """
        self.date_created = date_created or datetime.datetime.now(
            tz=datetime.UTC
        )
        self.study_group_id = study_group_id or "g" + uuid()[-9:]
        self._studies = studies or []
        self.name = name or f"Study Group ({self.study_group_id})"
        self.notes = notes

    def as_dict(self, *, simple: bool = False) -> dict:
        """Represent the study group as a dictionary."""
        d = {
            "Name": "",
            "Notes": "",
            "Date Created": self.date_created.isoformat(),
            "Study Group ID": self.study_group_id,
        }

        if simple:
            d["Studies"] = [x.study_id for x in self._studies]
            return d

        d["Studies"] = self.studies
        d["@module"] = self.__class__.__module__
        d["@class"] = self.__class__.__name__

        return d

    @classmethod
    def from_dict(cls, d: dict) -> "StudyGroup":
        """Instantiate a study group from a dictionary."""
        if isinstance(d["Date Created"], datetime.datetime):
            date_created = d["Date Created"]
        else:
            date_created = datetime.datetime.fromisoformat(d["Date Created"])

        studies = []

        for i, study_ in enumerate(d["Studies"]):
            if isinstance(study_, study.Study):
                studies[i] = study_
            else:
                studies[i] = study.Study.from_dict(study_)

        return cls(
            date_created,
            d["Study Group ID"],
            studies,
            d["Name"],
            d["Notes"],
        )

    def __eq__(self, obj) -> bool:
        """Determine whether two study groups are equivalent."""
        if not isinstance(obj, StudyGroup):
            return False

        if obj.study_group_id != self.study_group_id:
            return False

        return obj.studies == self.studies

    @classmethod
    def from_path(cls, study_group_dir: pathlib.Path) -> S:
        """Create a study group from a directory."""
        studies = []

        details = serialization.loadfn(study_group_dir / "study.json")

        for study_ in details["Studies"]:
            studies.append(study.Study.from_path(study_group_dir / study_))

        details["Studies"] = studies
        return cls.from_dict(details)

    def create_directory(self, path: pathlib.Path) -> None:
        """Create a directory for a study group.

        Args:
            path: The directory in which to create the study group
                directory.
        """
        study_group_dir = path.joinpath(self.study_group_id)
        study_group_dir.mkdir()

        study_group_details = self.as_dict(simple=True)

        for study_ in self._studies:
            study_.create_directory(study_group_dir)

        serialization.dumpfn(
            study_group_details,
            study_group_dir / "study_group.json",
            sort_keys=False,
            indent=4,
        )

    @property
    def studies(self) -> list[study.Study]:
        """The studies in the study group."""
        return self._studies.copy()

    @studies.setter
    def studies(self, new_studies: list[study.Study] | None = None) -> None:
        """Set the studies in the study group."""
        self._studies = new_studies or []

    def addstudies(self, new_studies: list[study.Study] | None = None) -> None:
        """Add studies to the study group."""
        # Remove duplicates
        new_studies: list[study.Study] = list(set(new_studies)) or []

        for study_ in new_studies:
            if study not in self._studies:
                self._studies.append(study_)

    def removestudies(
        self, to_remove: list[int | study.Study] | None = None
    ) -> None:
        """Remove studies from the study group.

        Args:
            to_remove: A list of integers or studies to remove. Integers
                are interpreted as indices.
        """
        to_remove: list[int | study.Study] = to_remove or [-1]

        new_studies: list[study.Study] = []

        for i in len(self._studies):
            if i in to_remove:
                continue

            if self._studies[i] in to_remove:
                continue

            new_studies.append(self._studies[i])

        self._studies = new_studies
