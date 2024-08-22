from collections.abc import Generator
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from io import TextIOWrapper
import json
import logging
import pathlib
import shutil
import textwrap
from typing import Any
from typing import Literal
from uuid import uuid4

from ase import Atoms
from ase.calculators.emt import EMT
from numpy.linalg import norm
from pydantic import UUID4
from pymatgen.io.vasp import Vasprun
import pytest

from autojob import SETTINGS
from autojob import MyEncoder
from autojob import hpc
from autojob.calculation.calculation import CalculationInputs
from autojob.calculation.calculation import CalculationOutputs
from autojob.calculation.vasp.vasp import FILES_TO_CARRYOVER
from autojob.calculation.vasp.vasp import VOLUMETRIC_FILES

# TODO: replace with parameters.CalculatorType
from autojob.coordinator.classification import CalculationType
from autojob.coordinator.classification import CalculatorType
from autojob.coordinator.classification import StudyType
from autojob.coordinator.job import JobError
from autojob.coordinator.vasp import VaspJob
from autojob.hpc import Partition
from autojob.hpc import SchedulerInputs
from autojob.hpc import SchedulerOutputs
from autojob.task import Task
from autojob.task import TaskInputs
from autojob.task import TaskMetadata
from autojob.task import TaskOutcome
from autojob.task import TaskOutputs
from autojob.utils.files import get_uri
from autojob.utils.parsing import TimedeltaTuple

logger = logging.getLogger(__name__)

VASP_OUTPUT_FILES = [
    "BSETFATBAND",
    "CHG",
    "CHGCAR",
    "DOSCAR",
    "EIGENVAL",
    "ELFCAR",
    "IBZKPT",
    "LOCPOT",
    "OSZICAR",
    "PARCHG",
    "PCDAT",
    "PROCAR",
    "PROOUT",
    "REPORT",
    "TMPCAR",
    "WAVECAR",
    "WAVEDER",
    "XDATCAR",
    "vasp.dipcor",
    "vasprun.xml",
]

SLURM_OUTPUT_FILES = {
    None: "no-job-error-slurm-file.txt",
    JobError.TIME_LIMIT: "time-limit-error-slurm-file.txt",
    # ! uncomment when memory limit output file comment decided on
    # JobError.MEMORY_LIMIT: "memory-limit-error-slurm-file.txt",
}

BUILDING_TASK_METADATA = """
############################
## Building Task Metadata ##
############################
"""


@pytest.fixture(name="label")
def fixture_label() -> str:
    label = "label"
    return label


@pytest.fixture(name="tags")
def fixture_tags() -> list[str]:
    tags = ["tag1"]

    return tags


@pytest.fixture(
    name="id_stem",
    params=[
        "111111111",
    ],
)
def fixture_id_stem() -> str:
    return "111111111"


@pytest.fixture(name="study_group_id")
def fixture_study_group_id(id_stem: str) -> str:
    return f"g{id_stem}"


@pytest.fixture(name="study_id")
def fixture_study_id(id_stem: str) -> str:
    return f"s{id_stem}"


@pytest.fixture(name="workflow_step_id")
def fixture_workflow_step_id() -> UUID4:
    return uuid4()


@pytest.fixture(name="calculation_id")
def fixture_calculation_id(id_stem: str) -> str:
    return f"c{id_stem}"


@pytest.fixture(name="task_id")
def fixture_task_id() -> UUID4:
    return uuid4()


@pytest.fixture(name="job_id")
def fixture_job_id(id_stem: str) -> str:
    return f"j{id_stem}"


@pytest.fixture(name="date_created")
def fixture_date_created() -> datetime:
    return datetime.datetime(2022, 1, 1)


@pytest.fixture(name="last_updated")
def fixture_last_updated() -> datetime:
    last_updated = datetime.now(tz=UTC)

    return last_updated


@pytest.fixture(name="uri")
def fixture_uri(tmp_path: pathlib.Path) -> str:
    return get_uri(tmp_path)


@pytest.fixture(name="use_task_aliases")
def fixture_use_task_aliases() -> bool:
    use_task_aliases = False
    return use_task_aliases


@pytest.fixture(name="task_metadata")
def fixture_task_metadata(
    *,
    label: str,
    tags: list[str],
    uri: str,
    study_group_id: str | UUID4 | None,
    study_id: str | UUID4 | None,
    workflow_step_id: UUID4 | None,
    task_id: str | UUID4,
    calculation_id: str | UUID4,
    last_updated: datetime | None,
    calculation_type: CalculationType,
    calculator: CalculatorType,
    study_type: StudyType,
    use_task_aliases: bool,
) -> TaskMetadata:
    data = {
        "label": label,
        "tags": tags,
        "uri": uri,
        "study_group_id": study_group_id,
        "study_id": study_id,
        "workflow_step_id": workflow_step_id,
        "task_id": task_id,
        "calculation_id": calculation_id,
        "last_updated": last_updated,
        "calculation_type": calculation_type,
        "calculator_type": calculator,
        "study_type": study_type,
    }
    if use_task_aliases:
        data["Name"] = data.pop("label")
        data["Notes"] = "; ".join(data.pop("tags"))
        data["Study Group ID"] = str(data.pop("study_group_id"))
        data["Study ID"] = str(data.pop("study_id"))
        data["Calculation ID"] = str(data.pop("calculation_id"))
        data["Job ID"] = str(data.pop("task_id"))
        data["Calculation Type"] = str(data.pop("calculation_type"))
        data["Calculator Type"] = str(data.pop("calculator_type"))
        data["Study Type"] = str(data.pop("study_type"))
    return TaskMetadata(**data)


@pytest.fixture(name="valid_job")
def fixture_valid_job(
    job_id: str,
    calculation_id: str,
    study_id: str,
    study_group_id: str,
    study_type: StudyType,
    calculator: CalculatorType,
    calculation_type: CalculationType,
) -> dict[str, str | CalculationType, CalculatorType, StudyType]:
    return {
        "Name": "Test",
        "Notes": "notes",
        "Study Group ID": study_group_id,
        "Study ID": study_id,
        "Study Type": study_type,
        "Calculation ID": calculation_id,
        "Calculation Type": calculation_type,
        "Calculator Type": calculator,
        "Job ID": job_id,
    }


@pytest.fixture(name="valid_calculation")
def fixture_valid_calculation(
    job_id: str,
    calculation_id: str,
    study_id: str,
    study_group_id: str,
    study_type: StudyType,
    calculator: CalculatorType,
    date_created: datetime,
) -> dict[str, str | CalculationType, StudyType]:
    return {
        "Date Created": date_created,
        "Name": "Test",
        "Notes": "notes",
        "Study Group ID": study_group_id,
        "Study ID": study_id,
        "Study Type": study_type,
        "Calculation ID": calculation_id,
        "Calculation Type": calculator,
        "Jobs": [job_id],
    }


@pytest.fixture(name="valid_study")
def fixture_valid_study(
    calculation_id: str,
    study_id: str,
    study_group_id: str,
    study_type: StudyType,
    date_created: datetime,
) -> dict[str, str | StudyType]:
    return {
        "Date Created": date_created,
        "Name": "Test",
        "Notes": "notes",
        "Study Group ID": study_group_id,
        "Study ID": study_id,
        "Study Type": study_type,
        "Calculations": [calculation_id],
    }


@pytest.fixture(name="valid_study_group")
def fixture_valid_study_group(
    study_id: str, study_group_id: str, date_created: datetime
) -> dict[str, str | StudyType]:
    return {
        "Date Created": date_created,
        "Name": "Test",
        "Notes": "notes",
        "Study Group ID": study_group_id,
        "Studies": [study_id],
    }


@pytest.fixture(name="study_type")
def fixture_study_type() -> StudyType:
    return StudyType.ADSORPTION


@pytest.fixture(name="calculation_type")
def fixture_calculation_type() -> CalculationType:
    return CalculationType.RELAXATION


@pytest.fixture(name="calculator", params=[CalculatorType.VASP])
def fixture_calculator(request: pytest.FixtureRequest) -> CalculatorType:
    calculator: CalculatorType = request.param
    return calculator


@pytest.fixture(name="ase_calculator")
def fixture_ase_calculator(calculator: CalculatorType) -> str:
    calc = str(calculator).lower()
    return f"ase.calculators.{calc}.{calc.capitalize()}"


@pytest.fixture(
    name="entry_type", params=("Study Group", "Study", "Calculation", "Job")
)
def fixture_entry_type(request: pytest.FixtureRequest) -> str:
    entry_type: str = request.param
    return entry_type


BUILDING_TASK_INPUTS = """
##########################
## Building Task Inputs ##
##########################
"""


@pytest.fixture(name="files_to_copy", params=[VASP_OUTPUT_FILES])
def fixture_files_to_copy(request: pytest.FixtureRequest) -> list[str]:
    files_to_copy: list[str] = request.param

    return files_to_copy


@pytest.fixture(name="files_to_delete", params=[VASP_OUTPUT_FILES])
def fixture_files_to_delete(request: pytest.FixtureRequest) -> list[str]:
    files_to_delete: list[str] = request.param

    return files_to_delete


@pytest.fixture(name="files_to_carryover", params=[FILES_TO_CARRYOVER])
def fixture_files_to_carryover(request: pytest.FixtureRequest) -> list[str]:
    files_to_carryover: list[str] = request.param

    return files_to_carryover


@pytest.fixture(name="auto_restart", params=[True])
def fixture_auto_restart(request: pytest.FixtureRequest) -> bool:
    auto_restart: bool = request.param
    return auto_restart


@pytest.fixture(name="task_options")
def fixture_task_options(
    files_to_delete: list[str],
    auto_restart: bool,
) -> dict[str, Any]:
    return {
        "files_to_delete": files_to_delete,
        "auto_restart": auto_restart,
    }


@pytest.fixture(name="task_inputs")
def fixture_task_inputs(
    *,
    atoms: Atoms,
    files_to_copy: list[str],
    files_to_delete: list[str],
    files_to_carryover: list[str],
    auto_restart: bool,
) -> TaskInputs:
    return TaskInputs(
        atoms=atoms,
        files_to_copy=files_to_copy,
        files_to_delete=files_to_delete,
        files_to_carry_over=files_to_carryover,
        auto_restart=auto_restart,
    )


BUILDING_CALCULATION_INPUTS = """
##################################
##  Building Calculation Inputs ##
##################################
"""

# Structure Inputs


@pytest.fixture(name="structure_name", params=("in.traj",))
def fixture_structure_name(request: pytest.FixtureRequest) -> str:
    structure_name: str = request.param
    return structure_name


@pytest.fixture(name="atoms")
def fixture_atoms() -> Atoms:
    return Atoms("C")


# Calculator Parameters


@pytest.fixture(
    name="parameters",
)
def fixture_parameters() -> dict[str, Any]:
    return {
        x.name.lower(): x.default
        for x in VaspJob.input_parameters()
        if x.default
    }


@pytest.fixture(name="calculation_inputs")
def fixture_calculation_inputs(
    ase_calculator: CalculatorType, parameters: dict[str, Any]
) -> CalculationInputs:
    return CalculationInputs(
        ase_calculator=ase_calculator,
        parameters=parameters,
    )


BUILDING_PYTHON_SCRIPT = """
#############################
##  Building Python Script ##
#############################
"""


# Imports


@pytest.fixture(name="calculator_as_name", params=[False])
def fixture_calculator_as_name(
    calculator: CalculatorType, request: pytest.FixtureRequest
) -> str | None:
    if request.param:
        return str(calculator).capitalize()[0]
    return None


@pytest.fixture(name="calculator_import")
def fixture_calculator_import(
    calculator: CalculatorType,
    calculator_as_name: str | None,
) -> str:
    calc = str(calculator).lower()
    suffix = f" as {calculator_as_name}" if calculator_as_name else ""

    return f"from ase.calculators.{calc} import {calc.capitalize()}{suffix}"


@pytest.fixture(name="run_py_imports")
def fixture_run_py_imports(
    calculator_import: str,
) -> list[str]:
    imports = [
        "import pathlib",
        "",
        "import ase.io",
        calculator_import,
        "from numpy.linalg import norm",
        "",
    ]
    return imports


# Complete Script


@pytest.fixture(name="run_py")
def fixture_run_py(
    structure_name: str,
    parameters: dict[str, Any],
    calculator: CalculatorType,
    run_py_imports: list[str],
    calculator_as_name: str | None,
) -> list[str]:
    shebang = ["#! /usr/bin/env python3"]

    atoms_assignment = [f"atoms = ase.io.read('{structure_name}')", ""]

    calc_func = calculator_as_name or str(calculator).capitalize()

    calc_def = [f"calc = {calc_func}("]
    calc_config = []

    for k, v in parameters.items():
        calc_config.append(f"    {k}={v!r},")

    command = [")", "", "e = atoms.get_potential_energy()", ""]

    record_keeping = [
        "f = norm(max(atoms.get_forces, key=norm))",
        "",
        "print(f'final energy: {e}')",
        "print(f'max force: {f}')",
        "",
        "with open('final.e', mode='r', encoding='utf-8') as file:",
        "    _ = file.write(f'final energy: {e} eV')",
        "",
        "atoms.write('final.traj')",
    ]

    return (
        shebang
        + run_py_imports
        + atoms_assignment
        + calc_def
        + calc_config
        + command
        + record_keeping
    )


@pytest.fixture(name="write_run_py")
def fixture_write_run_py(
    run_py: list[str], tmp_path: pathlib.Path
) -> Generator[TextIOWrapper, None, None]:
    python_script = tmp_path.joinpath(SETTINGS.PYTHON_SCRIPT)
    python_script = tmp_path.joinpath(SETTINGS.PYTHON_SCRIPT)
    with python_script.open(mode="w", encoding="utf-8") as file:
        file.write("\n".join(run_py))

    with python_script.open(mode="r", encoding="utf-8") as file:
        yield file


BUILDING_SCHEDULER_INPUTS = """
##################################
###  Building Scheduler Inputs ###
##################################
"""


@pytest.fixture(name="cores", params=[12])
def fixture_cores(request: pytest.FixtureRequest) -> int:
    cores: int = request.param
    return cores


@pytest.fixture(name="nodes", params=[1])
def fixture_nodes(request: pytest.FixtureRequest) -> int:
    nodes: int = request.param
    return nodes


@pytest.fixture(name="job_name", params=["vasp.sh"])
def fixture_job_name(request: pytest.FixtureRequest) -> str:
    job_name: str = request.param
    return job_name


@pytest.fixture(name="partitions", params=[[hpc.Partition.RAZI]])
def fixture_partitions(request: pytest.FixtureRequest) -> str:
    partitions: Partition = request.param
    return partitions


@pytest.fixture(name="mem_per_cpu", params=[1024])
def fixture_mem_per_cpu(request: pytest.FixtureRequest) -> int:
    mem_per_cpu: int = request.param

    return mem_per_cpu


@pytest.fixture(name="mail_type")
def fixture_mail_type() -> list[str]:
    mail_type = ["BEGIN", "END", "FAIL", "TIME_LIMIT", "TIME_LIMIT_90"]

    return mail_type


@pytest.fixture(name="slurm_options")
def fixture_slurm_options(
    elapsed: timedelta,
    cores: int,
    nodes: int,
    job_name: str,
    partitions: list[Partition],
    mem_per_cpu: int,
    mail_type: list[str],
) -> dict[str, Any]:
    return {
        "job-name": job_name,
        "partition": partitions,
        "mem-per-cpu": mem_per_cpu,
        "nodes": nodes,
        "ntasks-per-node": cores,
        "time": elapsed,
        "mail-user": "",
        "mail-type": mail_type,
    }


@pytest.fixture(name="scheduler_inputs")
def fixture_scheduler_inputs(
    slurm_options: dict[str, Any],
) -> SchedulerInputs:
    return SchedulerInputs(**slurm_options)


BUILDING_SLURM_SCRIPT = """
##############################
###  Building SLURM Script ###
##############################
"""


@pytest.fixture(name="bash_shebang", params=[True])
def fixture_bash_shebang(request: pytest.FixtureRequest) -> list[str]:
    if request.param:
        return ["#! /usr/bin/bash"]
    return []


@pytest.fixture(name="interspacer", params=("",))
def fixture_interspacer(request: pytest.FixtureRequest) -> str:
    interspacer: str = request.param
    return interspacer


@pytest.fixture(name="misplaced_slurm_option", params=[False])
def fixture_misplaced_slurm_option(
    request: pytest.FixtureRequest,
) -> list[str]:
    if request.param:
        return ["#SBATCH --output=slurm-%A.out", ""]

    return [""]


@pytest.fixture(name="slurm_script_code")
def fixture_slurm_script_code() -> list[str]:
    return [
        'echo " "',
        'echo "### Setting up shell environment ..."',
        'echo " "',
        "module load python ase vasp",
        "",
        f"python3 {SETTINGS.PYTHON_SCRIPT}",
        f"python3 {SETTINGS.PYTHON_SCRIPT}",
        "",
    ]


@pytest.fixture(name="copy_format")
def fixture_copy_format() -> str:
    copy_format = "legacy"
    return copy_format


@pytest.fixture(name="file_copying_logic")
def fixture_file_copying_logic(
    files_to_copy: list[str], copy_format: Literal["legacy", "env_var"]
) -> list[str]:
    if files_to_copy:
        files = ",".join(files_to_copy)
        match copy_format:
            case "legacy":
                files = "{" + files + "}"
                file_copying_logic = [
                    f'cp -v "$SLURM_SUBMIT_DIR"/{files} "$TMP_WORK_DIR"/'
                ]
            case "env_var":
                file_copying_logic = [
                    f'AUTOJOB_FILES_TO_COPY="{files}"',
                    'cp -v "$SLURM_SUBMIT_DIR"/{$AUTOJOB_FILES_TO_COPY} '
                    '"$TMP_WORK_DIR"/',
                ]

        return [*file_copying_logic, "", "sleep 10", ""]

    return [""]


@pytest.fixture(name="deletion_format")
def fixture_deletion_format() -> str:
    deletion_format = "legacy"
    return deletion_format


@pytest.fixture(name="file_deletion_logic")
def fixture_file_deletion_logic(
    files_to_delete: list[str], deletion_format: Literal["legacy", "env_var"]
) -> list[str]:
    if files_to_delete:
        match deletion_format:
            case "legacy":
                file_deletion_logic = textwrap.wrap(
                    f"rm -vf {' '.join(files_to_delete)}",
                    width=40,
                    subsequent_indent=" " * 7,
                )
                for i in range(len(file_deletion_logic) - 1):
                    file_deletion_logic[i] += " \\"
            case "env_var":
                files = " ".join(files_to_delete)
                file_deletion_logic = [
                    f'AUTOJOB_FILES_TO_DELETE="{files}"',
                    'rm "AUTOJOB_FILES_TO_DELETE"',
                ]

        return [*file_deletion_logic, "", "sleep 10", ""]

    return [""]


@pytest.fixture(name="auto_restart_format")
def fixture_auto_restart_format() -> str:
    auto_restart_format = "legacy"
    return auto_restart_format


@pytest.fixture(name="auto_restart_logic")
def fixture_auto_restart_logic(
    *, auto_restart: bool, auto_restart_format: Literal["legacy", "advance"]
) -> list[str]:
    if auto_restart:
        match auto_restart_format:
            case "legacy":
                return [
                    "if [ $restart = true ]; then",
                    "    module unload autojob",
                    "    activate autojob",
                    "    create_relaxation -mvba",
                    "",
                ]
            case "advance":
                return [
                    "autojob advance",
                    "",
                ]

    return [""]


@pytest.fixture(name="slurm_script")
def fixture_slurm_script(
    bash_shebang: list[str],
    interspacer: str,
    slurm_options: list[str],
    slurm_script_code: list[str],
    misplaced_slurm_option: list[str],
    file_copying_logic: list[str],
    file_deletion_logic: list[str],
    auto_restart_logic: list[str],
) -> list[str]:
    """Compose a slurm script"""
    slurm_config = []

    for k, v in slurm_options.items():
        option_name = k.replace("_", "-")
        if len(option_name) == 1:
            prefix = "-"
            suffix = " "
        else:
            prefix = "--"
            suffix = "="

        if isinstance(v, list):
            value = ",".join(str(x) for x in v)
        elif isinstance(v, timedelta):
            value = TimedeltaTuple.from_timedelta(v).to_slurm_time()
        else:
            value = v

        slurm_config.append(f"#SBATCH  {prefix}{option_name}{suffix}{value}")

    if interspacer:
        midpoint = int(len(slurm_config) / 2)
        slurm_config.insert(midpoint, interspacer.strip())

    slurm_config.append("")

    return (
        bash_shebang
        + slurm_config
        + file_copying_logic
        + slurm_script_code
        + misplaced_slurm_option
        + file_deletion_logic
        + auto_restart_logic
    )


@pytest.fixture(name="write_slurm_script")
def fixture_write_slurm_script(
    slurm_script: list[str], tmp_path: pathlib.Path
) -> Generator[TextIOWrapper, None, None]:
    run_sh = tmp_path.joinpath(SETTINGS.SLURM_SCRIPT)
    run_sh = tmp_path.joinpath(SETTINGS.SLURM_SCRIPT)
    with run_sh.open(mode="w", encoding="utf-8") as file:
        file.write("\n".join(slurm_script))

    with run_sh.open(mode="r", encoding="utf-8") as file:
        yield file


TASK_OUTPUTS = """
######################
###  Task Outputs  ###
######################
"""


@pytest.fixture(name="task_outcome")
def fixture_task_outcome() -> TaskOutcome:
    return TaskOutcome.IDLE


@pytest.fixture(name="task_outputs")
def fixture_task_outputs(
    output_atoms: Atoms, task_outcome: TaskOutcome
) -> TaskOutputs:
    return TaskOutputs(
        atoms=output_atoms,
        outcome=task_outcome,
    )


CALCULATION_OUTPUTS = """
#############################
###  Calculation Outputs  ###
#############################
"""


# ! This should be changed to coordinate with the vasprun fixture
@pytest.fixture(name="output_atoms")
def fixture_output_atoms() -> Atoms:
    atoms = Atoms("C")
    atoms.calc = EMT()
    atoms.get_potential_energy()
    return atoms


@pytest.fixture(name="forces")
def fixture_forces(output_atoms: Atoms) -> list[float]:
    forces: list[float] = output_atoms.get_forces()

    return forces


@pytest.fixture(name="energy")
def fixture_energy(output_atoms: Atoms) -> float:
    return output_atoms.get_potential_energy()


@pytest.fixture(name="max_force")
def fixture_max_force(output_atoms: Atoms) -> float:
    return norm(max(output_atoms.get_forces(), key=norm))


@pytest.fixture(name="vasprun")
def fixture_vasprun(
    request: pytest.FixtureRequest, shared_datadir: pathlib.Path
) -> Vasprun | None:
    marker = request.node.get_closest_marker("output_files")
    if marker and ("vasprun_xml" in marker.args or "all" in marker.args):
        return Vasprun(str(shared_datadir.joinpath("vasprun.xml")))
    return None


@pytest.fixture(name="converged")
def fixture_converged(vasprun: Vasprun | None) -> float:
    return False if vasprun is None else vasprun.converged


@pytest.fixture(name="output_structure_name", params=[SETTINGS.OUTPUT_ATOMS])
def fixture_output_structure_name(request: pytest.FixtureRequest) -> str:
    output_structure_name: str = request.param
    return output_structure_name


@pytest.fixture(name="calculation_outputs")
def fixture_calculation_outputs(
    *,
    energy: float,
    converged: bool,
    forces: list[float],
) -> CalculationOutputs:
    return CalculationOutputs(
        energy=energy,
        forces=forces,
        converged=converged,
    )


SCHEDULER_OUTPUTS = """
#######################
## Scheduler Outputs ##
#######################
"""

# SLURM Outputs: Start Time


@pytest.fixture(name="submit_time")
def fixture_submit_time() -> datetime:
    submit_time = datetime(  # noqa: DTZ001
        year=2022,
        month=7,
        day=29,
        hour=9,
        minute=48,
        second=14,
    )
    return submit_time


@pytest.fixture(name="slurm_wait_days", params=[0])
def fixture_slurm_wait_days(request: pytest.FixtureRequest) -> int:
    slurm_wait_days: int = request.param
    return slurm_wait_days


@pytest.fixture(name="slurm_wait_hours", params=[0])
def fixture_slurm_wait_hours(request: pytest.FixtureRequest) -> int:
    slurm_wait_hours: int = request.param
    return slurm_wait_hours


@pytest.fixture(name="slurm_wait_minutes", params=[0])
def fixture_slurm_wait_minutes(request: pytest.FixtureRequest) -> int:
    slurm_wait_minutes: int = request.param
    return slurm_wait_minutes


@pytest.fixture(name="slurm_wait_seconds", params=[1])
def fixture_slurm_wait_seconds(request: pytest.FixtureRequest) -> int:
    slurm_wait_seconds: int = request.param
    return slurm_wait_seconds


@pytest.fixture(name="idle")
def fixture_idle(
    slurm_wait_days: int,
    slurm_wait_hours: int,
    slurm_wait_minutes: int,
    slurm_wait_seconds: int,
) -> timedelta:
    return timedelta(
        days=slurm_wait_days,
        hours=slurm_wait_hours,
        minutes=slurm_wait_minutes,
        seconds=slurm_wait_seconds,
    )


@pytest.fixture(name="start_time")
def fixture_start_time(
    submit_time: datetime,
    idle: timedelta,
) -> datetime:
    return submit_time + idle


# SLURM Outputs: End Time


@pytest.fixture(name="slurm_days", params=[0])
def fixture_slurm_days(request: pytest.FixtureRequest) -> int:
    slurm_day: int = request.param
    return slurm_day


@pytest.fixture(name="slurm_hours", params=[0])
def fixture_slurm_hours(request: pytest.FixtureRequest) -> int:
    slurm_hours: int = request.param
    return slurm_hours


@pytest.fixture(name="slurm_minutes", params=[30])
def fixture_slurm_minutes(request: pytest.FixtureRequest) -> int:
    slurm_minutes: int = request.param
    return slurm_minutes


@pytest.fixture(name="slurm_seconds", params=[43])
def fixture_slurm_seconds(request: pytest.FixtureRequest) -> int:
    slurm_seconds: int = request.param
    return slurm_seconds


@pytest.fixture(name="elapsed")
def fixture_elapsed(
    slurm_days: int, slurm_hours: int, slurm_minutes: int, slurm_seconds: int
) -> timedelta:
    return timedelta(
        days=slurm_days,
        hours=slurm_hours,
        minutes=slurm_minutes,
        seconds=slurm_seconds,
    )


@pytest.fixture(name="end_time")
def fixture_end_time(
    start_time: datetime,
    elapsed: timedelta,
) -> datetime:
    return start_time + elapsed


@pytest.fixture(name="max_rss", params=[18049744.0])
def fixture_max_rss(request: pytest.FixtureRequest) -> int:
    max_rss: int = request.param

    return max_rss


@pytest.fixture(name="partition", params=[Partition.RAZI])
def fixture_partition(request: pytest.FixtureRequest) -> Partition:
    partition: Partition = request.param
    return partition


@pytest.fixture(name="job_stats")
def fixture_job_stats(
    max_rss: int,
    partition: Partition,
    start_time: datetime,
    end_time: datetime,
    submit_time: datetime,
    cores: int,
    nodes: int,
) -> dict[str, int | Partition | datetime]:
    return {
        "MaxRSS": max_rss,
        "Partition": partition,
        "Start": start_time,
        "End": end_time,
        "Submit": submit_time,
        "NCPUS": cores,
        "NNodes": nodes,
    }


@pytest.fixture(name="job_error", params=[None])
def fixture_job_error(request: pytest.FixtureRequest) -> bool:
    job_error: bool = request.param
    return job_error


@pytest.fixture(name="slurm_job_id", params=[123456789])
def fixture_slurm_job_id(request: pytest.FixtureRequest) -> str:
    slurm_job_id: int = request.param
    return slurm_job_id


@pytest.fixture(name="slurm_output_filename")
def fixture_slurm_output_filename(slurm_job_id: int) -> str:
    return f"slurm-{slurm_job_id}.out"


@pytest.fixture(name="scheduler_outputs")
def fixture_scheduler_outputs(
    elapsed: timedelta,
    idle: timedelta,
    slurm_job_id: int,
    job_error: int,
    max_rss: int,
    partition: Partition,
) -> SchedulerOutputs:
    return SchedulerOutputs(
        elapsed=elapsed,
        error=job_error,
        idle_time=idle,
        job_id=slurm_job_id,
        max_rss=max_rss,
        partition=partition,
    )


COMPLETED_OUTPUTS = """
###########################
###  Completed Outputs  ###
###########################
"""


@pytest.fixture(name="task_doc")
def fixture_task_doc(
    task_metadata: TaskMetadata,
    task_inputs: TaskInputs,
    task_outputs: TaskOutputs,
) -> Task:
    return Task(
        task_metadata=task_metadata,
        task_inputs=task_inputs,
        task_outputs=task_outputs,
    )


@pytest.fixture(name="write_task_doc")
def fixture_write_task_doc(
    task_doc: Task, populate_inputs: pathlib.Path
) -> Generator[TextIOWrapper, None, None]:
    task_json = populate_inputs.joinpath(SETTINGS.TASK_FILE)
    with task_json.open(mode="w", encoding="utf-8") as file:
        json.dump(task_doc, file, indent=4, cls=MyEncoder)

    with task_json.open(mode="r", encoding="utf-8") as file:
        yield file


DIRECTORY_POPULATION = """
##############################
###  Directory Population  ###
##############################
"""


@pytest.fixture(name="populate_study_group_directory")
def fixture_populate_study_group_directory() -> pathlib.Path:
    populate_study_group_directory = None

    return populate_study_group_directory


@pytest.fixture(name="populate_study_directory")
def fixture_populate_study_directory() -> pathlib.Path:
    populate_study_directory = None

    return populate_study_directory


@pytest.fixture(name="populate_task_directory")
def fixture_populate_task_directory() -> pathlib.Path:
    populate_task_directory = None

    return populate_task_directory


@pytest.fixture(name="populate_inputs")
def fixture_populate_inputs(
    atoms: Atoms,
    structure_name: str,
    run_py: list[str],
    slurm_script: list[str],
    valid_job: dict[str, Any],
    request: pytest.FixtureRequest,
    tmp_path: pathlib.Path,
) -> pathlib.Path:
    """Main utility fixture for populating an input directory

    Specify which inputs to add to directory using the input_files fixture:

        @pytest.mark.input_files("structure", "python_script")
        def test():...
    """
    all_files = ["structure", "python_script", "slurm_script", "job_json"]
    marker = request.node.get_closest_marker("input_files")

    if marker:
        to_include = all_files if "all" in marker.args else marker.args
    else:
        to_include = []

    for file in to_include:
        match file:
            case "structure":
                logger.debug(f"Structure name: {structure_name}")
                atoms.write(tmp_path.joinpath(structure_name))
            case "python_script":
                with tmp_path.joinpath(SETTINGS.PYTHON_SCRIPT).open(
                    mode="w", encoding="utf-8"
                ) as f:
                    f.write("\n".join(run_py))
            case "slurm_script":
                with tmp_path.joinpath(SETTINGS.SLURM_SCRIPT).open(
                    mode="w", encoding="utf-8"
                ) as f:
                    f.write("\n".join(slurm_script))
            case "job_json":
                with tmp_path.joinpath(SETTINGS.JOB_FILE).open(
                    mode="w", encoding="utf-8"
                ) as f:
                    json.dump(valid_job, f, indent=4, cls=MyEncoder)

    return tmp_path


@pytest.fixture(name="slurm_output_file_to_copy")
def fixture_slurm_output_file_to_copy(job_error: JobError) -> str:
    slurm_output_file_to_copy = SLURM_OUTPUT_FILES[job_error]

    return slurm_output_file_to_copy


@pytest.fixture(name="populate_outputs")
def fixture_populate_outputs(  # noqa: C901
    populate_inputs: pathlib.Path,
    output_atoms: Atoms,
    output_structure_name: str,
    task_doc: Task,
    slurm_output_filename: str,
    slurm_output_file_to_copy: str,
    request: pytest.FixtureRequest,
    shared_datadir: pathlib.Path,
) -> pathlib.Path:
    """Main utility fixture for populating an output directory

    Specify which outputs to add to directory using the output_files fixture:

        @pytest.mark.output_files("structure", "vasprun_xml")
        def test():...
    """
    all_files = [
        "structure",
        "vasprun_xml",
        "task_doc",
        "job_stats",
        "slurm_output_file",
        *VOLUMETRIC_FILES,
        "outcar",
        "contcar",
        "elph_poscars",
        "ase_sort_dat",
    ]
    marker = request.node.get_closest_marker("output_files")

    # Write output atoms to file (or write alternative structure file
    # e.g., vasprun.xml, CONTCAR)
    if marker:
        to_include = all_files if "all" in marker.args else marker.args
    else:
        to_include = []

    for file in to_include:
        match file:
            case "structure":
                output_atoms.write(
                    populate_inputs.joinpath(output_structure_name)
                )
            case "vasprun_xml":
                shutil.copy(
                    shared_datadir.joinpath("vasprun.xml"), populate_inputs
                )
            case "contcar":
                shutil.copy(
                    shared_datadir.joinpath("CONTCAR"), populate_inputs
                )
            case "outcar":
                shutil.copy(shared_datadir.joinpath("OUTCAR"), populate_inputs)
            case "ase_sort_dat":
                shutil.copy(
                    shared_datadir.joinpath("ase-sort.dat"), populate_inputs
                )
            case "task_doc":
                with populate_inputs.joinpath(SETTINGS.TASK_FILE).open(
                    mode="w", encoding="utf-8"
                ) as f:
                    json.dump(task_doc, f, indent=4, cls=MyEncoder)
            case "job_stats":
                shutil.copy(
                    shared_datadir.joinpath(SETTINGS.JOB_STATS_FILE),
                    populate_inputs,
                )
            case "slurm_output_file":
                shutil.copy(
                    shared_datadir.joinpath(slurm_output_file_to_copy),
                    populate_inputs.joinpath(slurm_output_filename),
                )

    return populate_inputs


@pytest.fixture(
    name="post_job_filenames",
    params=(
        "slurm-12345678.out",
        SETTINGS.PYTHON_SCRIPT,
        SETTINGS.PYTHON_SCRIPT,
        "out.txt",
        "OUTCAR",
        "vasprun.xml",
        "in.traj",
        "INCAR",
        "KPOINTS",
        "DOSCAR",
        "CONTCAR",
        "ase-sort.dat",
        "final.e",
        "OSZICAR",
        "POSCAR",
        "REPORT",
        "WAVECAR",
        "vasp.sh",
    ),
)
def fixture_post_job_filenames(request: pytest.FixtureRequest) -> str:
    entry_type: str = request.param
    return entry_type


@pytest.fixture(name="string", params=["Test", "2", "@", "\n", " ", ""])
def fixture_string(request: pytest.FixtureRequest) -> str:
    string: str = request.param
    return string


@pytest.fixture(
    name="non_string", params=[[], {}, True, False, None, set(), 0.0, 0]
)
def fixture_non_string(request: pytest.FixtureRequest) -> Any:
    return request.param
