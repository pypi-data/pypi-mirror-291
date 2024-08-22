import json
import pathlib
from uuid import UUID

import pytest

from autojob import SETTINGS
from autojob.workflow import Workflow


@pytest.fixture(name="workflow")
def fixture_workflow() -> Workflow:
    uuid_1 = str(UUID("12345678123456781234567812345678"))
    uuid_2 = str(UUID("87654321876543218765432187654321"))
    workflow = Workflow({uuid_1: [uuid_2]})
    return workflow


class TestFromDirectory:
    @staticmethod
    def test_should_load_dumped_workflow(
        tmp_path: pathlib.Path, workflow: Workflow
    ) -> None:
        dest = tmp_path.joinpath(SETTINGS.WORKFLOW_FILE)
        with dest.open(mode="w", encoding="utf-8") as file:
            file.write(json.dumps(workflow._graph, indent=4))

        assert Workflow.from_directory(tmp_path)._graph == workflow._graph


class TestGetNextSteps:
    @staticmethod
    def test_should_return_empty_list_for_step_without_successor(
        workflow: Workflow,
    ) -> None:
        assert workflow.get_next_steps("") == []

    @staticmethod
    def test_should_return_successors(
        workflow: Workflow,
    ) -> None:
        uuid_1 = str(UUID("12345678123456781234567812345678"))
        uuid_2 = str(UUID("87654321876543218765432187654321"))
        workflow = Workflow({uuid_1: [uuid_2]})
        assert workflow.get_next_steps(uuid_2) == [uuid_1]
