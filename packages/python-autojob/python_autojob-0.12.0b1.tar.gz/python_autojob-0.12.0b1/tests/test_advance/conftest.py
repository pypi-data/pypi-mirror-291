from pathlib import Path

import pytest

from autojob.utils.files import find_job_dirs


@pytest.fixture(name="vasp_output_dir")
def fixture_vasp_output_dir(shared_datadir: Path) -> Path:
    output_dir = find_job_dirs(shared_datadir.joinpath("g2KCxSrHM9"))[0]

    return output_dir


@pytest.fixture(name="gaussian_output_dir")
def fixture_gaussian_output_dir(shared_datadir: Path) -> Path:
    output_dir = find_job_dirs(shared_datadir.joinpath("gMp4Ge94dq"))[0]

    return output_dir
