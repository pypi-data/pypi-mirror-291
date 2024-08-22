from io import TextIOWrapper
import pathlib

from ase import Atoms
import pytest

from autojob.task import TaskInputs


class TestExtractFilesToCopy:
    @staticmethod
    @pytest.mark.parametrize("copy_format", ["env_var"])
    def test_should_read_from_env_var(
        files_to_copy: list[str], slurm_script: list[str]
    ) -> None:
        assert TaskInputs.extract_files_to_copy(slurm_script) == files_to_copy

    @staticmethod
    @pytest.mark.parametrize("copy_format", ["legacy"])
    def test_should_read_from_simple_command(
        files_to_copy: list[str], slurm_script: list[str]
    ) -> None:
        assert TaskInputs.extract_files_to_copy(slurm_script) == files_to_copy


class TestExtractFilesToDelete:
    @staticmethod
    @pytest.mark.parametrize("deletion_format", ["legacy"])
    def test_should_read_from_env_var(
        files_to_delete: list[str], slurm_script: list[str]
    ) -> None:
        assert (
            TaskInputs.extract_files_to_delete(slurm_script) == files_to_delete
        )

    @staticmethod
    @pytest.mark.parametrize("deletion_format", ["env_var"])
    def test_should_read_from_multiline_command(
        files_to_delete: list[str], slurm_script: list[str]
    ) -> None:
        assert (
            TaskInputs.extract_files_to_delete(slurm_script) == files_to_delete
        )


class TestCheckAutoRestart:
    @staticmethod
    @pytest.mark.parametrize("auto_restart_format", ["legacy"])
    def test_should_read_from_restart_relaxation(
        *, auto_restart: bool, slurm_script: list[str]
    ) -> None:
        assert TaskInputs.check_auto_restart(slurm_script) == auto_restart

    @staticmethod
    @pytest.mark.parametrize("auto_restart_format", ["advance"])
    def test_should_read_from_autojob_advance(
        *, auto_restart: bool, slurm_script: list[str]
    ) -> None:
        assert TaskInputs.check_auto_restart(slurm_script) == auto_restart


class TestGetInputAtoms:
    @staticmethod
    def test_should_retrieve_input_atoms(
        atoms: Atoms,
        write_run_py: TextIOWrapper,
        structure_name: str,
    ) -> None:
        dir_name = pathlib.Path(write_run_py.name).parent
        atoms.write(dir_name.joinpath(structure_name))

        assert TaskInputs.get_input_atoms(dir_name=dir_name) == atoms


class TestFromDirectory:
    @staticmethod
    @pytest.mark.input_files("all")
    def test_should_recreate_task_inputs_without_carryover_files(
        task_inputs: TaskInputs, populate_inputs: pathlib.Path
    ) -> None:
        loaded_inputs = TaskInputs.from_directory(dir_name=populate_inputs)
        assert loaded_inputs.model_dump(
            exclude=["files_to_carryover"]
        ) == task_inputs.model_dump(exclude=["files_to_carryover"])
