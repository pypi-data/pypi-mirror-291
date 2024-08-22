"""Harvest data from the directories of completed calculations.

Example:
    Harvest the results in the current working directory as vibrational
    calculations

    .. code-block:: python

        from pathlib import Path

        from autojob.calculation.vibration import Vibration
        from autojob.harvest.harvest import harvest

        harvest(dir_name=Path.cwd(), strictness="relaxed", preferred=Vibration)

.. important::

    Always verify the units of harvested quantities.
"""

import logging
from pathlib import Path
from typing import Literal

from autojob import SETTINGS
from autojob.task import Task
from autojob.utils.files import find_job_dirs

logger = logging.getLogger(__name__)


def _concatenate_list_sources(sources: list[str]) -> list[str]:
    """Read the lines from a list of files and concatentate their lines.

    Args:
        sources: A list of file names.

    Returns:
        The unique, non-empty lines in the files provided.
    """
    res = []
    for source in sources:
        with Path(source).open(mode="r", encoding="utf-8") as file:
            lines = [
                line.rstrip() for line in file.readlines() if line.rstrip()
            ]
        res.extend(lines)
    return res


def harvest(
    dir_name: str | Path,
    *,
    strictness: Literal["strict", "relaxed", "atomic"] | None = None,
    whitelist: list[str] | None = None,
    blacklist: list[str] | None = None,
    preferred: type[Task] | None = None,
) -> list[Task]:
    """Collect all data in subdirectories of the given directory.

    Args:
        dir_name: The directory under which to collect data.
        strictness: How to treat tasks for which errors are thrown during their
            harvesting. If ``"strict"``, all harvesting will abort. If
            ``"atomic"``, only calculations for which errors are not thrown will
            be harvested. If ``"relaxed"``, every attempt to harvest all
            calculations. The default behaviour is controlled by the value of
            ``SETTINGS.STRICT_MODE``. If ``SETTINGS.STRICT_MODE=True``, the
            default behaviour will be that of ``strictness="strict"``.
            Otherwise, the default behaviour will be that of
            ``strictness="relaxed"``.
        whitelist: A list of strings representing whitelists, where each
            whitelist is a list of task IDs that should be harvested. When
            specified, only tasks with task IDs matching these IDs will be
            harvested. Defaults to None in which case all tasks are eligible
            for harvesting.
        blacklist: A list of strings representing task IDs, where each
            blacklist is a list of task IDs that should not be harvested.
            When specified, no tasks with task IDs in this list will be
            harvested. Defaults to None in which case all tasks will be
            harvested.
        preferred: A preferred Task type to use to harvest each calculation.
            Defaults to :class:`autojob.task.Task`.

    Returns:
        A list of :class:`~task.Task` s containing the data within ``dir_name``.
    """
    logger.debug(f"Harvesting calculations from: {dir_name}")
    strict_mode = (
        SETTINGS.STRICT_MODE
        if strictness is None
        else strictness in ("strict", "atomic")
    )
    jobs = find_job_dirs(Path(dir_name))
    builder = preferred or Task

    if whitelist is not None:
        jobs = [
            j for j in jobs if j.name in _concatenate_list_sources(whitelist)
        ]

    if blacklist is not None:
        jobs = [
            j
            for j in jobs
            if j.name not in _concatenate_list_sources(blacklist)
        ]

    harvested = []
    for job in jobs:
        try:
            harvested_task = builder.from_directory(
                job, strict_mode=strict_mode, magic_mode=True
            )
            harvested.append(harvested_task)
        except FileNotFoundError as e:
            if strict_mode and strictness != "atomic":
                raise

            logger.warning(
                f"Unable to harvest task in directory {job} due to "
                "following error"
            )
            logger.error(e)

    logger.info(f"{len(harvested)} calculations harvested")
    return harvested
