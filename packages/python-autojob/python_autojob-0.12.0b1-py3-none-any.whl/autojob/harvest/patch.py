"""Supplement harvested data with data patches.

Oftentimes, you may have additional data that you either

a. can't determine a priori (and thus mark the task with it prior to
   submission), or

b. extract programatically (these may be analyses that require fuzzy
   intuition).

but nonetheless want to store with your data. This module defines some
simple routines and classes to facilitate this use-case.

A :class:`Patch` is just that, a "patch" - it fills in the gap in data
that may exist. To define one, you specify to a feature of the data
to which it should be applied and what data should be added when it is
applied.

.. code-block:: python

    from ase import Atoms
    from autojob.harvest.patch import Patch

    pch = Patch(match_path=["study_id"],
        match_value="123456789",
        patch_path=["atoms", "positions"]
        patch_value=[0.0, 0.0, 0.0]
    )

    datapoint1 = {
        "study_id": None,
        "atoms": None
    }

    atoms = Atoms("C", positions=[[0.0, 1.0, 2.0]])
    datapoint2 = {
        "study_id": None,
        "atoms": atoms
    }

    pch.apply(datapoint1)
    print(datapoint1["atoms"])
    None

    pch.apply(datapoint2)
    print(datapoint2["atoms"].positions)
    [0.0, 0.0, 0.0]

To what data the :class:`Patch` will apply is specified by ``match_path`` and
``match_value``. While, what will be applied is specified by ``patch_path`` and
``patch_value``.

Note:
    Patch applies to both dictionaries and objects alike!

Example:
    Apply a set of patches in batch

    .. code-block:: python

        from autojob.task import Task

        tasks = [Task(...), Task(...), ...]
        patches = [Patch(..., Patch(...), ...]

        for task in tasks:
            for patch in patches:
                patch.apply(task)

"""

from collections.abc import Mapping
from functools import reduce
import json
import logging
from pathlib import Path
from typing import Any
from typing import NamedTuple

from autojob import SETTINGS
from autojob.parametrizations import VariableReference
from autojob.task import Task
from autojob.utils.files import find_calculation_dirs
from autojob.utils.files import find_study_dirs
from autojob.utils.files import find_study_group_dirs

logger = logging.getLogger(__name__)


class Patch(NamedTuple):
    """A data patch.

    Attributes:
        match_path: A list of attribute/key names used to identify which
            attributes are to be patched by the path.
        match_value: The value of the attribute/key that must match.
        patch_path: The value of the attribute/key to be patched.
        patch_value: The value of the attribute/key to be set.

    """

    match_path: list[str]
    match_value: Any
    patch_path: list[str]
    patch_value: Any

    def apply(self, data: object) -> None:
        """Apply a patch to an object.

        Args:
            data: the data to which the patch will be applied. Note that this
                method may or may not end up modifying ``data``, but if it
                does, it will do in place.
        """

        def _get(x, y):
            if isinstance(x, Mapping):
                return x.get(y)
            return getattr(x, y)

        condition = reduce(
            lambda x, y: _get(x, y),
            self.match_path,
            data,
        )
        if condition == self.match_value:
            reference = VariableReference(
                set_path=self.patch_path,
                get_path=self.match_path,
                constant=self.patch_value,
            )
            # reference.set_input_value(task, task)
            to_get = data
            to_set = self.patch_path[-1]

            for node in self.patch_path[:-1]:
                if not hasattr(to_get, node):
                    logger.warn(
                        "Unable to set attribute %s on task %s",
                        node,
                        data,
                    )
                    break

                to_get = getattr(to_get, node)

            value = reference.evaluate(data)
            logger.info(f"Setting value: {to_set} to: {value}")
            setattr(to_get, to_set, self.patch_value)


def patch_tasks(patches: list[Patch], tasks: list[Task]) -> None:
    """Patch a list of tasks.

    This method modifies ``tasks`` in place.

    Args:
        patches: The patches to apply.
        tasks: The tasks to which the patches will be applied.
    """
    for task in tasks:
        for patch in patches:
            patch.apply(task)


# TODO: must implement calculation/study/study_group_metadata as Task
# TODO: attributes to prevent AttributeError and simplifying dumping
def build_calculation_patches(
    dir_name: Path, *, strict_mode: bool = SETTINGS.STRICT_MODE
) -> list[Patch]:
    """Creates patches from calculation metadata.

    Args:
        dir_name: The name of the directory under which to search for
            metadata. Defaults to the current working directory.
        strict_mode: Whether or not to abort metadata collection if
            metadata cannot be found. Defaults to ``SETTINGS.STRICT_MODE``.
    """
    calculations = find_calculation_dirs(dir_name)
    patches: list[Patch] = []

    for calculation in calculations:
        try:
            with calculation.joinpath(SETTINGS.CALCULATION_FILE).open(
                mode="r", encoding="utf-8"
            ) as file:
                metadata = {
                    f"Calculation {k}" for k, v in json.load(file).items()
                }
                patch_path = ["calculation_metadata"]
                patches.append(
                    Patch(
                        match_path=patch_path,
                        match_value=calculation.name,
                        patch_path=patch_path,
                        patch_value=metadata,
                    )
                )
        except FileNotFoundError:
            if strict_mode:
                raise

            logger.warning(
                "Unable to build metadata patches for calculation %s",
                calculation,
            )

    return patches


def build_study_patches(
    dir_name: Path | None = None,
    *,
    strict_mode: bool = SETTINGS.STRICT_MODE,
    legacy_mode: bool,
) -> list[Patch]:
    """Creates patches from study and calculation metadata.

    Args:
        dir_name: The name of the directory under which to search for
            metadata. Defaults to the current working directory.
        strict_mode: Whether or not to abort metadata collection if
            metadata cannot be found. Defaults to ``SETTINGS.STRICT_MODE``.
        legacy_mode: Whether or not to assume the legacy format for the
            directory.
    """
    studies = find_study_dirs(dir_name)
    patches: list[Patch] = []

    for study in studies:
        try:
            with study.joinpath(SETTINGS.STUDY_FILE).open(
                mode="r", encoding="utf-8"
            ) as file:
                metadata = json.load(file)
                patch_path = ["study_metadata"]

                patches.append(
                    Patch(
                        match_path=patch_path,
                        match_value=study.name,
                        patch_path=patch_path,
                        patch_value=metadata,
                    )
                )

                if legacy_mode:
                    patches.extend(
                        build_calculation_patches(
                            study, strict_mode=strict_mode
                        )
                    )
        except FileNotFoundError:
            if strict_mode:
                raise

            logger.warning(
                "Unable to build metadata patches for study %s",
                study,
            )

    return patches


def build_metadata_patches(
    dir_name: Path | None,
    *,
    strict_mode: bool = SETTINGS.STRICT_MODE,
    legacy_mode: bool = False,
) -> list[Patch]:
    """Creates patches from study group, study, and calculation metadata.

    Args:
        dir_name: The name of the directory under which to search for
            metadata. Defaults to the current working directory.
        strict_mode: Whether or not to abort metadata collection if
            metadata cannot be found. Defaults to ``SETTINGS.STRICT_MODE``.
        legacy_mode: Whether or not to assume the legacy format for the
            directory.

    Returns:
        A list of :class:`Patch` instances that when applied, will set the
        study group, study, and calculation metadata for a mapping or
        object.

    Example:
        Patch study group and study metadata for all tasks in a subdirectory.

        .. code-block:: python

            from pathlib import Path

            from autojob.harvest.harvest import harvest
            from autojob.harvest.patch import build_metadata_patches
            from autojob.harvest.patch import patch_tasks

            dir_name = Path().cwd()
            tasks = harvest(dir_name)
            patches = build_metadata_patches(dir_name)
            patch_tasks(patches, tasks)
    """
    study_groups = find_study_group_dirs(dir_name or Path().cwd())
    patches: list[Patch] = []

    for study_group in study_groups:
        try:
            with study_group.joinpath(SETTINGS.STUDY_GROUP_FILE).open(
                mode="r", encoding="utf-8"
            ) as file:
                metadata = json.load(file)
                patch_path = ["study_group_metadata"]
                patches.append(
                    Patch(
                        match_path=patch_path,
                        match_value=study_group.name,
                        patch_path=patch_path,
                        patch_value=metadata,
                    )
                )

            patches.extend(
                build_study_patches(
                    study_group,
                    strict_mode=strict_mode,
                    legacy_mode=legacy_mode,
                )
            )
        except FileNotFoundError:
            if strict_mode:
                raise

            logger.warning(
                "Unable to build metadata patches for study group %s",
                study_group,
            )

    return patches
