from pathlib import Path

from autojob.coordinator.gui import gui


class TestGUI:
    @staticmethod
    def test_should_run_gui(tmp_path: Path) -> None:
        assert gui.run(dest=tmp_path) is None
