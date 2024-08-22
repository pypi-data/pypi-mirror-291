import pathlib

from ase import Atoms
import pytest

from autojob.task import TaskOutputs


class TestGetOutputAtoms:
    @staticmethod
    @pytest.mark.output_files("structure")
    def test_should_retrieve_output_atoms(
        atoms: Atoms, populate_outputs: pathlib.Path
    ) -> None:
        assert TaskOutputs.get_output_atoms(dir_name=populate_outputs) == atoms
