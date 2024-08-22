"""VASP-specific Task details."""

from autojob.calculation.vasp.vasp import FILES_TO_CARRYOVER
from autojob.calculation.vasp.vasp import load_calculation_outputs

__all__ = ["load_calculation_outputs", "FILES_TO_CARRYOVER"]
