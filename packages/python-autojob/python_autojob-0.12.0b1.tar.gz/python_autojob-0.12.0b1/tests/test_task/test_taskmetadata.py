import json
import pathlib
from uuid import uuid4

from pydantic import UUID4
import pytest

from autojob import SETTINGS
from autojob.calculation.parameters import CalculatorType
from autojob.coordinator.classification import CalculationType
from autojob.study import StudyType
from autojob.task import TaskMetadata
from autojob.utils.files import get_uri

LEGACY_KEYS = [
    "Name",
    "Notes",
    "Study Group ID",
    "Study ID",
    "Calculation ID",
    "Job ID",
]


@pytest.fixture(name="label", params=["", "label"])
def fixture_label(request: pytest.FixtureRequest) -> str:
    label: str = request.param
    return label


@pytest.fixture(name="tags", params=[["tag1", "tag2"], []])
def fixture_tags(request: pytest.FixtureRequest) -> list[str]:
    tags: list[str] = request.param
    return tags


@pytest.fixture(name="uri", params=[True, False])
def fixture_uri(
    tmp_path: pathlib.Path, request: pytest.FixtureRequest
) -> str | None:
    if request.param:
        return get_uri(tmp_path)
    return None


@pytest.fixture(name="study_group_id", params=[True, False])
def fixture_study_group_id(
    id_stem: str, request: pytest.FixtureRequest
) -> str:
    if request.param:
        return uuid4()
    return f"g{id_stem}"


@pytest.fixture(name="study_id", params=[True, False])
def fixture_study_id(id_stem: str, request: pytest.FixtureRequest) -> str:
    if request.param:
        return uuid4()
    return f"s{id_stem}"


@pytest.fixture(name="workflow_step_id", params=[True, False])
def fixture_workflow_step_id(request: pytest.FixtureRequest) -> UUID4:
    if request.param:
        return uuid4()
    return None


@pytest.fixture(name="calculation_id")
def fixture_calculation_id(id_stem: str) -> str:
    return f"c{id_stem}"


@pytest.fixture(name="task_id")
def fixture_task_id() -> UUID4:
    return uuid4()


@pytest.fixture(name="job_id")
def fixture_job_id(id_stem: str) -> str:
    return f"j{id_stem}"


class TestTaskMetadataValidation:
    @staticmethod
    def test_should_instantiate_dict(task_metadata: TaskMetadata) -> None:
        assert task_metadata

    @staticmethod
    @pytest.mark.parametrize("use_task_aliases", [True, False])
    def test_should_work_with_legacy_aliases(
        *,
        task_metadata: TaskMetadata,
        use_task_aliases: bool,  # noqa: ARG004
    ) -> None:
        assert task_metadata

    @staticmethod
    @pytest.mark.parametrize("tags", ["", "tag1; tag2"])
    def test_should_convert_semicolon_list_to_list(
        tags: str, task_metadata: TaskMetadata
    ) -> None:
        tag_list = [tag.strip() for tag in tags.split(";")]
        assert all(tag in tag_list for tag in task_metadata.tags)


class TestFromDirectory:
    @staticmethod
    @pytest.fixture(name="job_dir")
    def fixture_job_dir(
        tmp_path: pathlib.Path,
        label: str,
        tags: list[str],
        study_group_id: str | UUID4 | None,
        study_id: str | UUID4 | None,
        job_id: str,
        calculation_id: str,
        study_type: StudyType,
        calculation_type: CalculationType,
        calculator: CalculatorType,
    ) -> pathlib.Path:
        job_file = tmp_path.joinpath(SETTINGS.JOB_FILE)
        details = {
            "Name": label,
            "Notes": "; ".join(tags),
            "Study Group ID": str(study_group_id),
            "Study ID": str(study_id),
            "Study Type": study_type.value,
            "Calculation ID": calculation_id,
            "Calculation Type": calculation_type.value,
            "Calculator Type": calculator.value,
            "Job ID": job_id,
        }
        with job_file.open(mode="w", encoding="utf-8") as file:
            json.dump(details, file, indent=4)

        return job_file.parent

    @staticmethod
    def test_should_load_from_legacy_directory(job_dir: pathlib.Path) -> None:
        assert TaskMetadata.from_directory(dir_name=job_dir)
