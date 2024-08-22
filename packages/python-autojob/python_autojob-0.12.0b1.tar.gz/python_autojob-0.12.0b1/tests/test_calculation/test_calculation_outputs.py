import pathlib

from ase import Atoms
import pytest

from autojob.calculation.vasp import vasp

BADER_CHARGE_JOB_ID = "jJPQg3Puwz"


class TestGetOutputAtoms:
    @staticmethod
    @pytest.mark.output_files("structure")
    def test_should_retrieve_existing_output_atoms_named_final_traj(
        populate_outputs: pathlib.Path,
        atoms: Atoms,
    ) -> None:
        retrieved_atoms = vasp.get_output_atoms(dir_name=populate_outputs)
        assert retrieved_atoms == atoms

    @staticmethod
    @pytest.mark.output_files("structure", "vasprun_xml", "ase_sort_dat")
    def test_should_retrieve_output_atoms_under_alternate_name1(
        populate_outputs: pathlib.Path,
        output_atoms: Atoms,
    ) -> None:
        retrieved_atoms = vasp.get_output_atoms(dir_name=populate_outputs)
        assert retrieved_atoms == output_atoms

    @staticmethod
    @pytest.mark.output_files("structure", "contcar", "ase_sort_dat")
    def test_should_retrieve_output_atoms_under_alternate_name2(
        populate_outputs: pathlib.Path,
        output_atoms: Atoms,
    ) -> None:
        retrieved_atoms = vasp.get_output_atoms(dir_name=populate_outputs)
        assert retrieved_atoms == output_atoms

    @staticmethod
    @pytest.mark.output_files
    @pytest.mark.parametrize("output_structure_name", "fake.traj")
    def test_should_raise_file_not_found_error_if_no_structure_found(
        populate_outputs: pathlib.Path,
    ) -> None:
        with pytest.raises(FileNotFoundError):
            _ = vasp.get_output_atoms(dir_name=populate_outputs)


class TestVaspLoadCalculationOutputs:
    @staticmethod
    @pytest.fixture(name="outputs")
    def fixture_outputs(datadir: pathlib.Path) -> pathlib.Path:
        outputs = datadir.joinpath(BADER_CHARGE_JOB_ID)

        return outputs

    @staticmethod
    def test_should_load_outputs(
        outputs: pathlib.Path,
    ) -> None:
        assert vasp.load_calculation_outputs(outputs)

    @staticmethod
    @pytest.mark.output_files("vasprun_xml", "contcar", "structure", "outcar")
    def test_should_load_vasprun_xml(populate_outputs: pathlib.Path) -> None:
        assert vasp.load_calculation_outputs(dir_name=populate_outputs)
