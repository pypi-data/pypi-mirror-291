"""Restart relaxation calculations.

Examples:

    .. code-block:: python

        from pathlib import Path
        from autojob.next.relaxation import restart_relaxation

        calc_mods = {
            "nsw": 250,
            "ibrion": 2,
        }
        slurm_mods = {"time-limit": "1-00:00:00", "mem": "1GB"}

        new_job = restart_relaxation(
            submit=True,
            old_job=Path.cwd(),
            bader=True,
            calc_mods=calc_mods,
            slurm_mods=slurm_mods,
        )
"""

from collections.abc import Iterable
import logging
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import Any

from autojob.advance.advance import _create_task
from autojob.advance.advance import delete_large_files
from autojob.advance.advance import submit_new_task
from autojob.advance.advance import update_metadata_file
from autojob.calculation.calculation import Calculation
from autojob.hpc import SchedulerInputs
from autojob.next import substitute_context
from autojob.task import Task

logger = logging.getLogger(__name__)

FILE_SIZE_LIMIT = 1e8


def restart_relaxation(
    submit: bool = False,
    file_size_limit: float = FILE_SIZE_LIMIT,
    old_job: pathlib.Path | None = None,
    *,
    bader: bool = False,
    chargemol: bool = False,
    auto_restart: bool = False,
    calc_mods: dict[str, Any] | None = None,
    slurm_mods: dict[str, Any] | None = None,
    files_to_carry_over: Iterable[str] | None = None,
    **_,
) -> pathlib.Path:
    """Utility function for restarting a DFT relaxation calculation.

    Args:
        submit: Whether or not to submit the new job after creation.
        file_size_limit: A float specifying the threshold above which files
            of this size will be deleted.
        old_job: The path to the old job.
        bader: Whether or not to add logic to run Bader charge analysis after
            the calculation has converged.
        chargemol: Whether or not to add logic to run DDEC6 analysis with
            chargemol after the calculation has converged.
        auto_restart: Whether or not to add logic to automatically restart the
            calculation after the calculation has converged.
        calc_mods: A dictionary mapping calculator parameters to values that
            should be used to overwrite the existing parameters.
        slurm_mods: A dictionary mapping Slurm options to values that
            should be used to overwrite the existing parameters.
        files_to_carry_over: A list of strings indicating which files to carry
            over from the old job directory to the new job directory. Defaults
            to None, in which case, the files to copy are determined from the
            previous task.

    Returns:
        The path to the newly created job.
    """
    old_job = pathlib.Path(old_job) if old_job else pathlib.Path.cwd()
    calc_mods = calc_mods or {}
    slurm_mods = slurm_mods or {}

    if bader or chargemol:
        calc_mods["laechg"] = calc_mods["lcharg"] = True

    previous = Task.from_directory(old_job, magic_mode=True, strict_mode=False)
    context = previous.task_metadata.model_dump(exclude_none=True)
    context["structure"] = previous.task_inputs.atoms.info.get(
        "structure", "{structure}"
    )
    mods = substitute_context(slurm_mods, context)

    if isinstance(previous, Calculation):
        previous.calculation_inputs.parameters.update(calc_mods)
        scheduler_inputs = previous.scheduler_inputs.model_dump(
            exclude_none=True
        )
        SchedulerInputs.update_values(scheduler_inputs, mods)
        previous.scheduler_inputs = SchedulerInputs(**scheduler_inputs)

    previous.task_inputs.auto_restart = auto_restart

    if files_to_carry_over is not None:
        previous.task_inputs.files_to_carry_over = files_to_carry_over

    with TemporaryDirectory() as tmpdir:
        spec = f"{Calculation.__module__}.{Calculation.__name__}"
        _, new_task_dir = _create_task(
            src=old_job,
            task_type_spec=spec,
            parametrization=[],
            previous_task=previous,
            root=tmpdir,
            legacy_mode=True,
            is_restart=True,
        )

        dst = old_job.parent.joinpath(new_task_dir.name)
        shutil.copytree(src=new_task_dir, dst=dst)

    update_metadata_file(
        new_task=dst,
        study_dir=old_job.parents[1],
        legacy_mode=True,
        restart=True,
    )

    delete_large_files(old_job=old_job, file_size_limit=file_size_limit)
    logger.debug(f"New job created {'/'.join(dst.parts[-4:])}")

    if submit:
        submit_new_task(new_task=dst)

    return dst
