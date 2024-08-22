import pathlib

from autojob import SETTINGS
from autojob.advance.advance import archive_task
from autojob.task import Task


class TestArchiveTask:
    @staticmethod
    def test_should_dump_task_to_json(
        task_doc: Task, tmp_path: pathlib.Path
    ) -> None:
        assert archive_task(
            dst=tmp_path, task=task_doc, archive_mode="json"
        ) == tmp_path.joinpath(SETTINGS.TASK_FILE)

    @staticmethod
    def test_should_not_dump_task_if_archive_mode_is_none(
        task_doc: Task, tmp_path: pathlib.Path
    ) -> None:
        assert (
            archive_task(dst=tmp_path, task=task_doc, archive_mode="None")
            is None
        )
