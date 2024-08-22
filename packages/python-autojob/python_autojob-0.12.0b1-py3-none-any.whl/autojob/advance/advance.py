"""Semi-automatically advance workflows.

Examples:
    Programmatically,

    .. code-block:: python

        from pathlib import Path

        from autojob.advance.advance import advance

        advance(dir_name=Path.cwd())

    From the command-line,

    .. code-block:: console

        autojob advance
"""

import datetime
import json
import logging
import pathlib
import shutil
import subprocess
from tempfile import TemporaryDirectory
from typing import Any
from typing import Literal
from typing import overload
from uuid import uuid4

import click
from pydantic import ImportString
from pydantic import TypeAdapter
from shortuuid import uuid

from autojob import SETTINGS
from autojob.coordinator.classification import CalculationType
from autojob.parametrizations import VariableReference
from autojob.task import Task
from autojob.utils.files import extract_structure_name
from autojob.utils.parsing import import_class
from autojob.workflow import Step
from autojob.workflow import Workflow

logger = logging.getLogger(__name__)

_SUBTASK_TO_NAME = {
    "Calculation": CalculationType.RELAXATION,
    "Vibration": CalculationType.VIB,
}
FILE_SIZE_LIMIT = 1e8


@overload
def archive_task(
    dst: pathlib.Path,
    task: Task,
    archive_mode: Literal["json"],
    study_dir: pathlib.Path | None,
) -> pathlib.Path: ...


@overload
def archive_task(
    dst: pathlib.Path,
    task: Task,
    archive_mode: Literal["None"],
    study_dir: pathlib.Path | None,
) -> None: ...


def archive_task(
    dst,
    task,
    archive_mode,
    *,
    study_dir=None,
):
    """Archive a completed Task and note its completion in the study record.

    Args:
        dst: A Path object indicating in which directory to archive the Task
        task: The Task to archive
        archive_mode: The mode to archive the Task. "json" archives the Task
            as a .json file. "None" does not archive the Task.
        study_dir: The root directory of the study to which `task` belongs. If
            None, then the task won't be recorded in the study record.

    Returns:
        A Path representing the filename in which the completed task is
        dumped, if ``archive_mode = "json"``. Otherwise, None.
    """
    if study_dir:
        with study_dir.joinpath(SETTINGS.RECORD_FILE).open(
            mode="a", encoding="utf-8"
        ) as file:
            file.write(f"{task.task_metadata.task_id}\n")

    if archive_mode == "json":
        task_json = dst.joinpath(SETTINGS.TASK_FILE)
        with task_json.open(mode="w", encoding="utf-8") as file:
            json.dump(task.model_dump(), file, indent=4)
            return task_json
    return None


def get_next_steps(
    task: Task, study_dir: pathlib.Path, *, restart: bool = False
) -> list[str]:
    """Get the UUIDs of the next steps in the workflow.

    Args:
        task: The previous task.
        study_dir: The root directory of the study containing the completed
            task.
        restart: Whether the task must be restarted. Defaults to False.

    Returns:
        A list of strings representing the steps that should be started since
        `task` has completed. If the task is to be restarted, the list will
        only contain a single string: the workflow step ID of the previous
        task.
    """
    logger.debug(f"Determining next steps for {task.task_metadata.task_id}")
    wfw = Workflow.from_directory(study_dir)
    nodes = iter(wfw.static_order())
    try:
        # ! For backwards-compatibility, assume only the first Task (a
        # ! relaxation Calculation) can fail; if it does, restart
        # TODO: implement restart for normal mode
        next_steps = [next(nodes)]
        if restart:
            step_id = task.task_metadata.workflow_step_id
            if step_id is None:
                # This block is for backwards-compatibility with 2-step,
                # linear workflows in which tasks do not have workflow step IDs
                # This can be removed when autojob assigns workflow step IDs
                # to jobs
                next_steps = [next(nodes)]
            else:
                # ! Must determine how to record completed tasks/steps to
                # ! facilitate the use of the `record` parameter in
                # ! Workflow.get_next_steps; note that the current
                # ! implementation will create a task for every
                # ! parametrization in a step (new and old); for new steps,
                # ! this is fine, but for repeating steps this is not the
                # ! desired behaviour
                next_steps = wfw.get_next_steps(str(step_id))
    except StopIteration:
        next_steps = []

    num_next_steps = len(next_steps)
    logger.debug(
        f"{num_next_steps} next step{'' if num_next_steps == 1 else 's'}"
    )

    return next_steps


def write_calculation_metadata(
    new_task: Task,
    new_job: pathlib.Path,
    old_calculation: pathlib.Path,
) -> None:
    """Write a new calculation metadata file.

    Args:
        new_task: The new Task.
        new_job: The path to the new job which must be in a subdirectory of
            the new calculation.
        old_calculation: The path to the calculation from which to create the
            new calculation metadata file.
    """
    logger.debug(f"Writing calculation file for {new_job.parent.name}")
    with old_calculation.joinpath(SETTINGS.CALCULATION_FILE).open(
        mode="r", encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    metadata["Date Created"] = str(datetime.datetime.now(tz=datetime.UTC))
    metadata["Calculation Type"] = str(
        new_task.task_metadata.calculation_type or CalculationType.RELAXATION
    )
    metadata["Calculation ID"] = new_job.parent.name
    metadata["Jobs"] = [new_job.name]
    metadata["Notes"] = f"based on {old_calculation.name}"

    with new_job.parent.joinpath(SETTINGS.CALCULATION_FILE).open(
        mode="w", encoding="utf-8"
    ) as file:
        json.dump(metadata, file, indent=4)

    logger.debug(
        f"Successfully wrote calculation file for {new_job.parent.name}"
    )


def create_new_task_tree(
    *,
    root: pathlib.Path,
    new_task: Task,
    legacy_step: bool = False,
) -> pathlib.Path:
    """Create the directory and parent directories of a new task.

    Args:
        root: A Path representing the root directory from which to create the
            directory of the new task.
        new_task: The newly created Task.
        legacy_step: Whether or not we are stepping forward in a legacy
            workflow.

    Returns:
        A Path object representing the directory of the newly created task.
    """
    if legacy_step:
        new_calc_id = new_task.task_metadata.calculation_id
        new_calc = pathlib.Path(root).joinpath(new_calc_id)
        new_job_parent = new_calc
    else:
        new_job_parent = root

    new_job_id = str(new_task.task_metadata.task_id)
    new_job = new_job_parent.joinpath(new_job_id)
    new_job.mkdir(parents=True)
    return new_job


def add_item_to_parent(
    item_id: str, metadata_file: pathlib.Path, key: str
) -> None:
    """Add the given ID to the details.json of its parent.

    Args:
        item_id: The ID to add.
        metadata_file: The path to the metadata file of the parent to which to
            add the item ID.
        key: The key to which to add. The key must point to a list[str] value.
    """
    logger.debug(f"Adding {item_id} to {metadata_file}")
    with metadata_file.open(mode="r", encoding="utf-8") as file:
        metadata = json.load(file)

    metadata[key].append(item_id)

    with metadata_file.open(mode="w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)
    logger.debug(f"Successfully added {item_id} to {metadata_file}")


def populate_new_task_tree(
    *,
    previous_task_src: pathlib.Path,
    new_task_dest: pathlib.Path,
    new_task: Task,
    files_to_carry_over: list[str],
    legacy_mode: bool = False,
    is_restart: bool = False,
) -> None:
    """Populate the directory tree of a new task.

    This function will copy over files to carry over, write task metadata files
    (e.g., job.json and calculation.json) as well as copy the directories
    that are staged in a temporary directory.

    Args:
        previous_task_src: A Path object representing the directory of the
            completed Task.
        new_task_dest: A Path object representing the destination directory of
            the new Task.
        new_task: The new Task.
        files_to_carry_over: A list of strings indicating the files to
            carry over from the previous Task.
        legacy_mode: Whether or not to use the legacy directory structure.
            Additional features of legacy mode include: 1) tasks have a non
            None calculation ID, 2) task_id has the form r"j[A-Za-z0-9]{9}"
        is_restart: Whether or not the new task is a restart.
    """
    # TODO: Check that files_to_carry_over are int files_to_copy
    for file in files_to_carry_over:
        try:
            _ = shutil.copy(
                src=previous_task_src.joinpath(file), dst=new_task_dest
            )
            logger.info(
                f"Successfully copied {file} to new task directory for task: "
                f"{new_task.task_metadata.task_id!s}"
            )
        except FileNotFoundError:
            logger.warning(
                f"Unable to copy {file} to new task directory for task: "
                f"{new_task.task_metadata.task_id!s}"
            )

    with previous_task_src.joinpath(SETTINGS.PYTHON_SCRIPT).open(
        mode="r", encoding="utf-8"
    ) as file:
        structure_name = extract_structure_name(file)

    new_task.to_directory(
        dst=new_task_dest,
        structure_name=structure_name,
        legacy_mode=legacy_mode,
    )

    if legacy_mode and not is_restart:
        write_calculation_metadata(
            new_task=new_task,
            new_job=new_task_dest,
            old_calculation=previous_task_src.parent,
        )


def update_metadata_file(
    new_task: pathlib.Path,
    study_dir: pathlib.Path,
    *,
    legacy_mode: bool = False,
    restart: bool = False,
):
    """Update the metadata files for a newly created Task.

    Args:
        new_task: A Path representing the directory of the newly created Task
            in its final destination.
        study_dir: The root directory of the study to which `task` belongs.
        legacy_mode: Whether or not to use the legacy directory structure.
            Additional features of legacy mode include: 1) tasks have a non
            None calculation ID, 2) task_id has the form r"j[A-Za-z0-9]{9}"
        restart: Whether the metadata is for a completed task. Defaults to
            True.
    """
    item_id = (
        new_task.parent.name if legacy_mode and not restart else new_task.name
    )

    if legacy_mode and restart:
        metadata_file = new_task.parent.joinpath(SETTINGS.CALCULATION_FILE)
        key = "Jobs"
    else:
        metadata_file = study_dir.joinpath(SETTINGS.STUDY_FILE)
        key = "Calculations" if legacy_mode else "Tasks"

    add_item_to_parent(
        item_id=item_id,
        metadata_file=metadata_file,
        key=key,
    )


def update_task_metadata(
    task_shell: dict[str, Any],
    task_type: str,
    *,
    context: dict[str, Any],
    legacy_mode: bool = False,
) -> None:
    """Update the task metadata for a Task shell.

    This method modifies `task_shell` in-place. Specifically, this function
    sets the keys "study_group_id" and "study_id" to be the same as in
    `context` and creates a new "task_id". The "tags" and "calculation_id"
    keys may also be set.

    Args:
        task_shell: A Task shell containing the key, `task_metadata`, which
            maps to a dictionary equivalent to what would be obtained with
            Task.create_shell().model_dump(exclude_none=True).
        task_type: The class name of the type of Task to be created.
        context: A dictionary containing a dumped model of the completed Task.
            The dictionary must have the key, "task_metadata", which maps to a
            dictionary containing the keys "study_group_id" and "study_id".
        legacy_mode: Whether or not to use the legacy directory structure.
            Additional features of legacy mode include: 1) tasks have a non
            None calculation ID, 2) task_id has the form r"j[A-Za-z0-9]{9}"
    """
    metadata = task_shell["task_metadata"]
    metadata["study_group_id"] = context["task_metadata"]["study_group_id"]
    metadata["study_id"] = context["task_metadata"]["study_id"]
    metadata["study_type"] = context["task_metadata"]["study_type"]
    metadata["calculator_type"] = task_shell["calculation_inputs"][
        "ase_calculator"
    ].__name__.lower()
    metadata["calculation_type"] = _SUBTASK_TO_NAME[task_type]
    metadata["task_id"] = f"j{uuid()[:9]}" if legacy_mode else uuid4()

    source_comment = context["task_metadata"]["task_id"]
    tags = context["task_metadata"].get("tags", [])
    metadata["tags"] = [*tags, source_comment]

    if legacy_mode:
        metadata["calculation_id"] = "c" + uuid()[:9]


# TODO: Support calc_mods/slurm_mods
def setup_task(
    *,
    task_type_spec: ImportString[Task],
    parametrization: list[VariableReference[Any]],
    previous_task: Task,
    legacy_mode: bool = False,
    is_restart: bool = True,
) -> Task:
    """Setup a new Task according to a parametrization.

    Args:
        src: The source directory for the new Task.
        task_type_spec: A string representing the fully qualified class name
            of the type of Task to be created.
        parametrization: The Parametrization for the new Task. Note that the
            metadata of the new Task will also be newly set regardless of the
            parametrization.
        previous_task: The previous Task.
        legacy_mode: Whether or not to use the legacy directory structure.
            Additional features of legacy mode include: 1) tasks have a non
            None calculation ID, 2) task_id has the form r"j[A-Za-z0-9]{9}"
        is_restart: Whether the task must be restarted. Defaults to False.

    Returns:
        The new Task instance.
    """
    task_type: type[Task] = import_class(task_type_spec)
    context = previous_task.model_dump(exclude_none=True)

    # Inherit all inputs if restarting
    if is_restart:
        context["task_inputs"]["atoms"] = context["task_outputs"]["atoms"]
        task_shell = task_type.create_shell(context).model_dump(
            exclude_none=True
        )
    else:
        task_shell = task_type.create_shell().model_dump(exclude_none=True)

        for ref in parametrization:
            ref.set_input_value(context, task_shell)

    update_task_metadata(
        task_shell=task_shell,
        task_type=task_type.__name__,
        context=context,
        legacy_mode=legacy_mode,
    )

    new_task = task_type(**task_shell)
    new_task.prepare_input_atoms()
    return new_task


def _create_task(
    *,
    src: pathlib.Path,
    task_type_spec: ImportString[Task],
    parametrization: list[VariableReference[Any]],
    previous_task: Task,
    root: str | pathlib.Path,
    legacy_mode: bool = False,
    is_restart: bool = True,
) -> tuple[Task, pathlib.Path]:
    """Create a new task, its directory, and its parent directories.

    Args:
        src: The source directory for the new Task.
        task_type_spec: A string representing the fully qualified class name
            of the type of Task to be created.
        parametrization: The Parametrization for the new Task. Note that the
            IDs within metadata cannot be set using parametrizations. See
            `update_task_metadata` for details.
        previous_task: The previous Task.
        root: The temporary root directory for the new directories.
        legacy_mode: Whether or not to use the legacy directory structure.
            Additional features of legacy mode include: 1) tasks have a non
            None calculation ID, 2) task_id has the form r"j[A-Za-z0-9]{9}"
        is_restart: Whether the metadata is for a completed task. Defaults to
            True.

    Returns:
        A 2-tuple (task, path) where task is the new Task instance and path
        is the directory in which it was dumped.
    """
    new_task = setup_task(
        task_type_spec=task_type_spec,
        parametrization=parametrization,
        previous_task=previous_task,
        legacy_mode=legacy_mode,
        is_restart=is_restart,
    )

    new_task_dir = create_new_task_tree(
        root=pathlib.Path(root),
        new_task=new_task,
        legacy_step=legacy_mode and not is_restart,
    )

    populate_new_task_tree(
        previous_task_src=src,
        new_task_dest=new_task_dir,
        new_task=new_task,
        files_to_carry_over=previous_task.task_inputs.files_to_carry_over,
        legacy_mode=legacy_mode,
        is_restart=is_restart,
    )
    return new_task, new_task_dir


def delete_large_files(
    old_job: pathlib.Path,
    *,
    file_size_limit: float = FILE_SIZE_LIMIT,
    files_to_delete: list[str] | None = None,
) -> None:
    """Deletes large files from copied job.

    Args:
        old_job: A pathlib.Path object representing the directory holding the
            large files to be deleted.
        file_size_limit: A float specifying the file size in bytes over which
            files will be deleted. Defaults to FILE_SIZE_LIMIT.
        files_to_delete: A list of strings specifying files to delete.
            Defaults to an empty list.
    """
    files_to_delete = files_to_delete or []

    for path in old_job.iterdir():
        if (
            path.stat().st_size >= file_size_limit
            or path.name in files_to_delete
        ):
            file = old_job.joinpath(path)
            file.unlink()
            logger.info(f'{"/".join(file.parts[-5:])} deleted')


def submit_new_task(new_task: pathlib.Path) -> None:
    """Submit the newly created job to the Slurm scheduler.

    Args:
        new_task: A Path to the new task's directory.
    """
    logger.info(f"Submitting task in {new_task}")
    output = subprocess.check_output(  # noqa: S603
        ["/usr/bin/env", "sbatch", SETTINGS.SLURM_SCRIPT],
        cwd=new_task,
        encoding="utf-8",
    )
    output = output.strip("\n")
    job_name = "/".join(new_task.parts[-4:])
    click.echo(f"{output} ({job_name})")
    logger.info(f"Successfully submitted task in {new_task}")


def _initiate_step(
    *,
    src: pathlib.Path,
    step: Step,
    previous_task: Task,
    file_size_limit: float = FILE_SIZE_LIMIT,
    submit: bool = True,
    legacy_mode: bool = False,
    restart: bool = True,
) -> list[tuple[Task, pathlib.Path]]:
    """Initiate a step by creating all tasks that are ready to start.

    Args:
        src: The source directory for the new tasks. That is, the directory
            containing the recently completed task.
        step: The Step to initiate.
        previous_task: The previous Task.
        file_size_limit: A float specifying the threshold above which files
            of this size will be deleted from the source directory. Defaults to
            FILE_SIZE_LIMIT.
        submit: Whether or not to submit the new Tasks after creation. Defaults
            to True.
        legacy_mode: Whether or not to use the legacy directory structure.
            Additional features of legacy mode include: 1) tasks have a non
            None calculation ID, 2) task_id has the form r"j[A-Za-z0-9]{9}"
        restart: Whether the metadata is for a completed task. Defaults to
            True.

    Returns:
        A list of 2-tuples (task, path) where task is the new Task instance
        and path is the path in which it was dumped.
    """
    tasks_and_dirs: list[tuple[Task, pathlib.Path]] = []
    for parametrization in step.parametrizations:
        with TemporaryDirectory() as tmpdir:
            new_task, new_task_dir = _create_task(
                src=src,
                task_type_spec=step.task_type,
                parametrization=None if restart else parametrization,
                previous_task=previous_task,
                root=tmpdir,
                legacy_mode=legacy_mode,
                is_restart=restart,
            )

            anchor_level = 1 if legacy_mode and not restart else 0
            new_task_tree = (
                new_task_dir.parent if anchor_level else new_task_dir
            )
            dst = src.parents[anchor_level].joinpath(new_task_tree.name)
            shutil.copytree(src=new_task_tree, dst=dst)

        study_dir = dst.parent
        update_metadata_file(
            new_task=new_task,
            study_dir=study_dir,
            legacy_mode=legacy_mode,
            restart=restart,
        )
        delete_large_files(
            old_job=src,
            file_size_limit=file_size_limit,
            files_to_delete=previous_task.task_inputs.files_to_delete,
        )
        tasks_and_dirs.append((new_task, new_task_dir))

        logger.debug(f"New task created {'/'.join(new_task_dir.parts[-4:])}")

        if submit:
            submit_new_task(new_task=new_task)

    return tasks_and_dirs


# TODO: Set legacy mode from command-line
# ! Note that all parametrizations of a given step are currently
def advance(
    *,
    dir_name: pathlib.Path,
    file_size_limit: float = FILE_SIZE_LIMIT,
    submit: bool = True,
    archive_mode: Literal["json", "None"],
    legacy_mode: bool = False,
) -> list[tuple[Task, pathlib.Path]]:
    """Advance to the next task in the workflow.

    Args:
        dir_name: The directory of the completed calculation.
        file_size_limit: A float specifying the threshold above which files
            of this size will be deleted. Defaults to FILE_SIZE_LIMIT.
        submit: Whether or not to submit the new job after creation. Defaults
            to True.
        archive_mode: How to store the results.
        legacy_mode: Whether or not to use the legacy directory structure.
            Additional features of legacy mode include: 1) tasks have a non
            None calculation ID, 2) task_id has the form r"j[A-Za-z0-9]{9}"

    Returns:
        A list of tuples (task_i, path_i) where task_i is the ith created Task
        and path_i is the Path representing the directory containing the ith
        created Task.
    """
    logger.debug(f"Advancing job in {dir_name}")
    study_dir = dir_name.parent.parent if legacy_mode else dir_name.parent
    completed_task = Task.from_directory(dir_name, magic_mode=True)
    restart = (
        completed_task.task_outputs is None
        or completed_task.task_outputs.outcome != "success"
    )
    _ = archive_task(
        dst=dir_name,
        task=completed_task,
        archive_mode=archive_mode,
        study_dir=study_dir,
    )
    next_steps = get_next_steps(completed_task, study_dir)

    with pathlib.Path(SETTINGS.PARAMETRIZATION_FILE).open(
        mode="r", encoding="utf-8"
    ) as file:
        steps = TypeAdapter(dict[str, Step]).validate_json(file.read())

    tasks_and_dirs: list[tuple[Task, pathlib.Path]] = []

    for step in next_steps:
        new_tasks_and_dirs = _initiate_step(
            src=dir_name,
            step=steps[step],
            previous_task=completed_task,
            file_size_limit=file_size_limit,
            submit=submit,
            legacy_mode=legacy_mode,
            restart=restart,
            study_dir=study_dir,
        )
        tasks_and_dirs.extend(new_tasks_and_dirs)

    return tasks_and_dirs
