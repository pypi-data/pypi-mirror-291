import pytest

# TODO: replace with parameters.CalculatorType
from autojob.coordinator.classification import CalculationType
from autojob.coordinator.classification import CalculatorType
from autojob.coordinator.classification import StudyType
from autojob.coordinator.job import JobError

DEFAULT_JOB_ERROR = JobError.TIME_LIMIT


@pytest.fixture(
    name="id_stem",
    params=[
        "111111111",
        "123456789",
    ],
)
def fixture_id_stem(request: pytest.FixtureRequest) -> str:
    id_stem: str = request.param
    return id_stem


@pytest.fixture(
    name="study_type",
    params=list(StudyType),
)
def fixture_study_type(request: pytest.FixtureRequest) -> StudyType:
    study_type: StudyType = request.param
    return study_type


@pytest.fixture(
    name="calculation_type",
    params=list(CalculationType),
)
def fixture_calculation_type(
    request: pytest.FixtureRequest,
) -> CalculationType:
    calculation_type: CalculationType = request.param
    return calculation_type


@pytest.fixture(
    name="calculator",
    params=list(CalculatorType)[:3],
)
def fixture_calculator(request: pytest.FixtureRequest) -> CalculatorType:
    calculator: CalculatorType = request.param
    return calculator


# ! Change to job state enum
@pytest.fixture(name="task_state", params=["success", "failed"])
def fixture_task_state(request: pytest.FixtureRequest) -> str:
    task_state: str = request.param
    return task_state


@pytest.fixture(name="job_error")
def fixture_job_error(task_state: str) -> bool:
    if task_state == "success":
        return None

    return DEFAULT_JOB_ERROR
