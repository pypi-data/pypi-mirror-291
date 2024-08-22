"""Create vibrational calculations.

Examples:

    .. code-block:: python

        from pathlib import Path
        from autojob.next.vibration import create_vibration

        calc_mods = {
            "nsw": 250,
            "ibrion": 2,
        }
        slurm_mods = {"time-limit": "1-00:00:00", "mem": "1GB"}

        new_job = create_vibration(
            submit=True,
            old_job=Path.cwd(),
            bader=True,
            calc_mods=calc_mods,
            slurm_mods=slurm_mods,
        )
"""

from collections.abc import Iterable
import logging
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import Any

from autojob.advance.advance import _create_task
from autojob.advance.advance import delete_large_files
from autojob.advance.advance import submit_new_task
from autojob.advance.advance import update_metadata_file
from autojob.calculation.infrared import Infrared
from autojob.calculation.parameters import CalculatorType
from autojob.calculation.vibration import Vibration
from autojob.next import create_parametrization
from autojob.parametrizations import VariableReference
from autojob.task import Task

logger = logging.getLogger(__name__)

FILE_SIZE_LIMIT = 1e8


def create_vibration(
    submit: bool = False,
    file_size_limit: float = FILE_SIZE_LIMIT,
    old_job: str | Path | None = None,
    *,
    calc_mods: dict[str, Any] | None = None,
    slurm_mods: dict[str, Any] | None = None,
    files_to_carry_over: Iterable[str] | None = None,
    infrared: bool = False,
    **_,
) -> Path:
    """Creates a vibrational calculation used to calculate :math:`TS + ZPE`.

    All atoms in the structure with the tag -99 will be frozen.

    Args:
        submit: Whether or not to submit the new job after creation.
        file_size_limit: A float specifying the threshold in bytes above which
            files of this size will be deleted.
        old_job: The path to the old job.
        calc_mods: A dictionary mapping calculator parameters to values that
            should be used to overwrite the existing parameters.
        slurm_mods: A dictionary mapping SLURM options to values that
            should be used to overwrite the existing parameters.
        files_to_carry_over: A list of strings indicating which files to copy from
            the old job directory to the new job directory. Defaults to None,
            in which case, the files to copy are determined from the previous
            task.
        infrared: Whether or not to calculate IR intensities. Requires that the
            calculator used has the method ``get_dipole_moment``.

    Returns:
        The path to the newly created job.
    """
    old_job = Path(old_job) if old_job else Path.cwd()
    calc_mods = calc_mods or {}
    slurm_mods = slurm_mods or {}

    old_task = Task.from_directory(old_job, magic_mode=True)
    if old_task.task_metadata.calculator_type == CalculatorType.VASP:
        calc_mods["nsw"] = 0

    parametrization = [
        VariableReference(
            set_path=["task_inputs", "files_to_delete"],
            get_path=["task_inputs", "files_to_delete"],
        ),
        VariableReference(
            set_path=["task_inputs", "auto_restart"],
            constant=False,
        ),
        VariableReference(
            set_path=["task_inputs", "atoms"],
            get_path=["task_outputs", "atoms"],
        ),
        VariableReference(
            set_path=["task_inputs", "files_to_copy"],
            get_path=["task_inputs", "files_to_copy"],
        ),
        VariableReference(
            set_path=["task_inputs", "files_to_carry_over"],
            constant=files_to_carry_over or [],
        ),
    ]
    parametrization += create_parametrization(
        old_task, calc_mods=calc_mods, slurm_mods=slurm_mods
    )

    with TemporaryDirectory() as tmpdir:
        task_type = Infrared if infrared else Vibration
        spec = f"{task_type.__module__}.{task_type.__name__}"
        _, new_task_dir = _create_task(
            src=old_job,
            task_type_spec=spec,
            parametrization=parametrization,
            previous_task=old_task,
            root=tmpdir,
            legacy_mode=True,
            is_restart=False,
        )
        dst = old_job.parents[1].joinpath(new_task_dir.parent.name)
        shutil.copytree(src=new_task_dir.parent, dst=dst)

    update_metadata_file(
        new_task=dst.joinpath(new_task_dir.name),
        study_dir=old_job.parents[1],
        legacy_mode=True,
        restart=False,
    )

    delete_large_files(old_job=old_job, file_size_limit=file_size_limit)

    logger.debug(f"New calculation created: {'/'.join(dst.parts[-3:])}")
    new_job = dst.joinpath(new_task_dir.name)
    logger.debug(f"New job created {'/'.join(new_job.parts[-4:])}")

    if submit:
        submit_new_task(new_task=dst)

    return new_job
