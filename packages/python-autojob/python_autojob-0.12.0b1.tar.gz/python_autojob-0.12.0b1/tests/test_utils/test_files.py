import pathlib
from typing import TextIO

import pytest

from autojob.utils.files import extract_structure_name
from autojob.utils.files import find_slurm_file
from autojob.utils.files import get_slurm_job_id


@pytest.fixture(name="dummy_slurm_file")
def fixture_dummy_slurm_file(populate_outputs: pathlib.Path) -> pathlib.Path:
    dummy_slurm_file = populate_outputs.joinpath("slurm-000000000.out")
    with dummy_slurm_file.open(mode="w", encoding="utf-8") as file:
        _ = file.write("")

    return dummy_slurm_file


class TestExtractStructureFilename:
    @staticmethod
    @pytest.mark.parametrize(
        "structure_name", ["in.traj", "Cu.traj", "relax.traj"]
    )
    def test_should_return_structure(
        structure_name: str,
        write_run_py: TextIO,
    ) -> None:
        extracted_structure_name = extract_structure_name(
            python_script=write_run_py
        )
        assert structure_name == extracted_structure_name


class TestFindSlurmFile:
    @staticmethod
    @pytest.fixture(name="slurm_job_id", params=[111111111, 123456789])
    def fixture_slurm_job_id(request: pytest.FixtureRequest) -> int:
        slurm_job_id: int = request.param
        return slurm_job_id

    @staticmethod
    @pytest.mark.output_files("slurm_output_file")
    def test_should_return_slurm_out_file(
        populate_outputs: pathlib.Path, slurm_output_filename: str
    ) -> None:
        slurm_file = find_slurm_file(dir_name=populate_outputs)
        assert slurm_file == populate_outputs.joinpath(slurm_output_filename)

    @staticmethod
    @pytest.mark.output_files("slurm_output_file")
    def test_should_return_slurm_file_of_newest_job(
        populate_outputs: pathlib.Path, dummy_slurm_file: pathlib.Path
    ) -> None:
        slurm_file = find_slurm_file(dir_name=populate_outputs)
        assert slurm_file != dummy_slurm_file

    @staticmethod
    @pytest.mark.output_files
    @pytest.mark.parametrize("slurm_job_id", [123456789])
    def test_should_raise_file_not_found_error_if_no_slurm_file_present(
        populate_outputs: pathlib.Path,
    ) -> None:
        with pytest.raises(FileNotFoundError):
            _ = find_slurm_file(dir_name=populate_outputs)


class TestGetSlurmJobID:
    @staticmethod
    @pytest.fixture(name="slurm_job_id", params=[111111111, 123456789])
    def fixture_slurm_job_id(request: pytest.FixtureRequest) -> int:
        slurm_job_id: int = request.param
        return slurm_job_id

    @staticmethod
    @pytest.mark.output_files("slurm_output_file")
    def test_should_find_valid_slurm_file(
        populate_outputs: pathlib.Path, slurm_job_id: int
    ) -> None:
        assert get_slurm_job_id(job_dir=populate_outputs) == slurm_job_id

    @staticmethod
    def test_should_raise_file_not_found_error_if_no_valid_slurm_file(
        populate_outputs: pathlib.Path,
    ) -> None:
        with pytest.raises(FileNotFoundError):
            _ = get_slurm_job_id(job_dir=populate_outputs)

    @staticmethod
    @pytest.mark.output_files("slurm_output_file")
    def test_should_not_return_id_of_older_job(
        populate_outputs: pathlib.Path,
        dummy_slurm_file: pathlib.Path,
    ) -> None:
        assert get_slurm_job_id(job_dir=populate_outputs) != dummy_slurm_file


class TestCreateJobStatsFile:
    pass
