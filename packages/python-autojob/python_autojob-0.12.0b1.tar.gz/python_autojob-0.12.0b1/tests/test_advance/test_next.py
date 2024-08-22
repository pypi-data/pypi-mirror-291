from collections.abc import Callable
from pathlib import Path
from typing import Any

from ase.calculators.vasp import Vasp
import pytest

from autojob import SETTINGS
from autojob.advance.advance import update_task_metadata
from autojob.calculation.calculation import Calculation
from autojob.coordinator.classification import CalculationType
from autojob.next import substitute_context
from autojob.next.relaxation import restart_relaxation
from autojob.next.vibration import create_vibration
from autojob.study import StudyType
from autojob.task import Task


@pytest.mark.filterwarnings(
    "ignore:.*Pydantic serializer warnings.*:UserWarning"
)
class TestLoadCompletedTask:
    @pytest.fixture(
        name="utility", params=[restart_relaxation, create_vibration]
    )
    @staticmethod
    def fixture_utility(
        request: pytest.FixtureRequest,
    ) -> Callable[[Path], Path]:
        utility: Callable[[Path], Path] = request.param

        return utility

    @staticmethod
    def test_should_work_with_vasp(
        vasp_output_dir: Path, utility: Callable[[Path], Path]
    ) -> None:
        assert utility(old_job=vasp_output_dir)

    @staticmethod
    def test_should_work_with_gaussian(
        gaussian_output_dir: Path, utility: Callable[[Path], Path]
    ) -> None:
        SETTINGS.SLURM_SCRIPT = "gaussian.sh"
        assert utility(old_job=gaussian_output_dir)


@pytest.fixture(name="study_group_id", scope="class")
def fixture_study_group_id() -> str:
    study_group_id = "g123456789"

    return study_group_id


@pytest.fixture(name="study_type", scope="class")
def fixture_study_type() -> StudyType:
    study_type = StudyType.SENSITIVITY

    return study_type


@pytest.fixture(name="calculation_type", scope="class")
def fixture_calculation_type() -> CalculationType:
    calculation_type = CalculationType.RELAXATION

    return calculation_type


@pytest.fixture(name="tags", scope="class")
def fixture_tags() -> list[str]:
    tags = ["j123456789"]

    return tags


@pytest.fixture(name="context", scope="class")
def fixture_context(
    calculation_type: CalculationType,
    study_group_id: str,
    study_type: StudyType,
    tags: list[str],
) -> dict[str, Any]:
    context = Task.create_shell()
    context.task_metadata.study_group_id = study_group_id
    context.task_metadata.study_type = study_type
    context.task_metadata.calculation_type = calculation_type
    context.task_metadata.tags = tags

    return context.model_dump()


@pytest.fixture(name="updated_task", scope="class")
def fixture_updated_task(
    calculation_type: CalculationType,
    context: dict[str, Any],
) -> Task:
    updated_task = Calculation.create_shell()
    updated_task.calculation_inputs.ase_calculator = Vasp

    legacy_mode = True
    task_type = (
        "Calculation"
        if calculation_type == CalculationType.RELAXATION
        else str(calculation_type)
    )

    to_return = updated_task.model_dump(exclude_none=True)

    update_task_metadata(
        task_shell=to_return,
        task_type=task_type,
        context=context,
        legacy_mode=legacy_mode,
    )

    return to_return


class TestUpdateTaskMetadata:
    @staticmethod
    def test_should_update_ids(
        updated_task: dict[str, Any], study_group_id: str
    ) -> None:
        assert (
            updated_task["task_metadata"]["study_group_id"] == study_group_id
        )

    @staticmethod
    def test_should_update_study_type(
        updated_task: dict[str, Any], study_type: StudyType
    ) -> None:
        assert updated_task["task_metadata"]["study_type"] == str(study_type)

    @staticmethod
    def test_should_update_calculator_type(
        updated_task: dict[str, Any],
    ) -> None:
        assert (
            updated_task["task_metadata"]["calculator_type"]
            == updated_task["calculation_inputs"][
                "ase_calculator"
            ].__name__.lower()
        )

    @staticmethod
    def test_should_update_calculation_type(
        updated_task: dict[str, Any], calculation_type: CalculationType
    ) -> None:
        assert (
            updated_task["task_metadata"]["calculation_type"]
            == calculation_type
        )

    @staticmethod
    def test_should_update_tags(
        updated_task: dict[str, Any], tags: list[str], context: dict[str, Any]
    ) -> None:
        new_tags = list(tags)
        job_id = context["task_metadata"]["task_id"]
        new_tags.append(job_id)
        assert updated_task["task_metadata"]["tags"] == new_tags


class TestSubstituteContext:
    @staticmethod
    def test_should_substitute_values() -> None:
        placeholder = "structure"
        key = "time"
        value = "value"

        template = "{" + placeholder + "}"
        mods = {key: template}
        context = {placeholder: value}

        new_mods = substitute_context(mods, context)
        assert new_mods[key] == value

    @staticmethod
    @pytest.mark.parametrize("value", [1, 1.0, None])
    def test_should_not_substitute_non_strings(value: Any) -> None:
        key = "time"

        mods = {key: value}
        context = {}

        new_mods = substitute_context(mods, context)
        assert new_mods[key] == value
