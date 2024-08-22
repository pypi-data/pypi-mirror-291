from pathlib import Path

from autojob import SETTINGS
from autojob.task import Task


class TestLoadCompletedTask:
    @staticmethod
    def test_should_load_completed_vasp_task(vasp_output_dir: Path) -> None:
        assert Task.from_directory(vasp_output_dir, magic_mode=True)

    @staticmethod
    def test_should_load_completed_gaussian_task(
        gaussian_output_dir: Path,
    ) -> None:
        SETTINGS.SLURM_SCRIPT = "gaussian.sh"
        assert Task.from_directory(gaussian_output_dir, magic_mode=True)
