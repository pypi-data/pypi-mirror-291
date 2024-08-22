from pathlib import Path

from autojob import SETTINGS
from autojob.calculation.parameters import CalculatorType
from autojob.calculation.vibration import Vibration


class TestVibration:
    @staticmethod
    def test_should_load_vibrational_calculation(
        datadir: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(SETTINGS, "PYTHON_SCRIPT", "run", raising=True)
        vib_calc = Vibration.from_directory(
            dir_name=datadir.joinpath("jD9gnRZLHK"),
            calculator_type=CalculatorType.VASP,
            strict=False,
        )
        assert vib_calc
