import datetime
from datetime import timedelta
import logging
import pathlib
from typing import Any
from typing import TextIO

from ase import Atoms
from pydantic import ValidationError
import pytest

from autojob.hpc import Partition
from autojob.hpc import SchedulerInputs
from autojob.hpc import SchedulerOutputs
from autojob.hpc import validate_memory
from autojob.utils.parsing import TimedeltaTuple

logger = logging.getLogger(__name__)

DEFAULT_ELAPSED = timedelta(days=1, hours=0, minutes=0, seconds=0)

DEFAULT_SHEBANG = ["#!/usr/bin/bash"]


class TestSchedulerInputsTime:
    @staticmethod
    def test_should_validate_timedelta(
        elapsed: datetime.timedelta,
    ) -> None:
        assert SchedulerInputs(time=elapsed).time == elapsed

    @staticmethod
    def test_should_validate_slurm_time(
        elapsed: datetime.timedelta,
    ) -> None:
        assert (
            SchedulerInputs.model_validate(
                {
                    "time": TimedeltaTuple.from_timedelta(
                        elapsed
                    ).to_slurm_time()
                },
                context={"format": "slurm"},
            ).time
            == elapsed
        )

    @staticmethod
    def test_should_not_validate_invalid_string() -> None:
        with pytest.raises(ValidationError):
            SchedulerInputs(time="0")


class TestSchedulerInputsMailType:
    @staticmethod
    @pytest.fixture(name="name", params=["mail_type", "mail-type"])
    def fixture_name(request: pytest.FixtureRequest) -> str:
        name: str = request.param
        return name

    @staticmethod
    def test_should_validate_list_of_strings(
        name: str, mail_type: list[str]
    ) -> None:
        assert (
            SchedulerInputs.model_validate({name: mail_type}).mail_type
            == mail_type
        )

    @staticmethod
    def test_should_validate_comma_separated_strings_in_slurm_format(
        name: str,
        mail_type: list[str],
    ) -> None:
        assert (
            SchedulerInputs.model_validate(
                {name: ",".join(mail_type)}, context={"format": "slurm"}
            ).mail_type
            == mail_type
        )


class TestSchedulerInputsMemory:
    @staticmethod
    @pytest.fixture(name="name", params=["mem", "mem_per_cpu", "mem-per-cpu"])
    def fixture_name(request: pytest.FixtureRequest) -> str:
        name: str = request.param
        return name

    @staticmethod
    def test_should_validate_int(name: str, mem_per_cpu: int) -> None:
        assert (
            getattr(
                SchedulerInputs.model_validate({name: mem_per_cpu}),
                name.replace("-", "_"),
            )
            == mem_per_cpu
        )

    @staticmethod
    def test_should_validate_memory_string(
        name: str,
        mem_per_cpu: int,
    ) -> None:
        assert (
            getattr(
                SchedulerInputs.model_validate(
                    {name: mem_per_cpu}, context={"format": "slurm"}
                ),
                name.replace("-", "_"),
            )
            == mem_per_cpu
        )


class TestSchedulerInputsPartition:
    @staticmethod
    @pytest.fixture(name="name", params=["partition", "partitions"])
    def fixture_name(request: pytest.FixtureRequest) -> str:
        name: str = request.param
        return name

    @staticmethod
    def test_should_validate_list_of_partitions(
        name: str, partitions: list[Partition]
    ) -> None:
        assert (
            SchedulerInputs.model_validate({name: partitions}).partitions
            == partitions
        )

    @staticmethod
    def test_should_validate_memory_string(
        name: str,
        partitions: list[Partition],
    ) -> None:
        assert (
            SchedulerInputs.model_validate(
                {name: ",".join(p.cluster_name for p in partitions)},
                context={"format": "slurm"},
            ).partitions
        ) == partitions


class TestSchedulerInputs:
    @staticmethod
    def test_should_instantiate_dict(
        scheduler_inputs: SchedulerInputs,
    ) -> None:
        assert scheduler_inputs


class TestExtractSchedulerInputs:
    @staticmethod
    @pytest.fixture(name="extracted_parameters")
    def fixture_extracted_parameters(
        write_slurm_script: TextIO,
    ) -> dict[str, Any]:
        extracted_parameters = SchedulerInputs.extract_scheduler_inputs(
            stream=write_slurm_script
        )
        return extracted_parameters

    # This functional test tests a number of cases by virtue of the
    # parametrization (see the "slurm_script" fixture and its requested
    # fixtures). Some key tests:
    #   - with/without bash shebang at top of file
    #   - various values for slurm parameters
    #   - with/without auto-restart logic and files deleted
    #   - slurm options interspersed with code

    @staticmethod
    @pytest.mark.parametrize(("files_to_delete", "auto_restart"), [([], True)])
    def test_should_read_all_and_only_options_in_heading(
        slurm_options: dict[str, Any],
        extracted_parameters: dict[str, Any],
    ) -> None:
        assert (
            extracted_parameters["time"]
            == TimedeltaTuple.from_timedelta(
                slurm_options["time"]
            ).to_slurm_time()
        )
        assert extracted_parameters["partition"] == ",".join(
            p.cluster_name for p in slurm_options["partition"]
        )
        assert extracted_parameters["nodes"] == str(slurm_options["nodes"])
        assert extracted_parameters["job-name"] == slurm_options["job-name"]
        assert extracted_parameters["mail-type"] == ",".join(
            slurm_options["mail-type"]
        )
        assert extracted_parameters["mail-user"] == slurm_options["mail-user"]
        assert extracted_parameters["mem-per-cpu"] == str(
            slurm_options["mem-per-cpu"]
        )
        assert extracted_parameters["ntasks-per-node"] == str(
            slurm_options["ntasks-per-node"]
        )


class TestUpdateValues:
    @staticmethod
    def test_should_update_memory() -> None:
        old_kw = "mem"
        old_value = 1
        inputs = {old_kw: old_value}
        new_kw = "mem_per_cpu"
        new_value = 2
        mods = {new_kw: new_value}
        SchedulerInputs.update_values(inputs, mods)
        assert old_kw not in inputs
        assert inputs[new_kw] == mods[new_kw]

    @staticmethod
    def test_should_update_time() -> None:
        parameter = "nodes"
        value = 1
        mods = {parameter: value}
        inputs = {}
        SchedulerInputs.update_values(inputs, mods)
        assert inputs[parameter] == value


class TestSchedulerInputsFromDirectory:
    @staticmethod
    @pytest.mark.input_files("slurm_script")
    @pytest.mark.parametrize(
        ("atoms", "structure_name", "run_py"), [(Atoms("C"), "in.traj", [""])]
    )
    def test_should_load_scheduler_inputs(
        populate_inputs: pathlib.Path,
        scheduler_inputs: SchedulerInputs,
    ) -> None:
        loaded_inputs = SchedulerInputs.from_directory(
            dir_name=populate_inputs
        )
        assert loaded_inputs.model_dump() == scheduler_inputs.model_dump()


class TestSchedulerOutputsValidate:
    @staticmethod
    @pytest.fixture(name="val")
    def fixture_val() -> float:
        val = 1.0
        return val

    @staticmethod
    @pytest.fixture(name="units")
    def fixture_units() -> str:
        units = "MB"
        return units

    @staticmethod
    @pytest.fixture(name="num_type")
    def fixture_num_type() -> type[int | float]:
        num_type = int
        return num_type

    @staticmethod
    def test_should_validate_start_and_submit_time_as_idle(
        submit_time: datetime.datetime,
        start_time: datetime.datetime,
        idle: datetime.datetime,
    ) -> None:
        outputs = {
            "Submit": submit_time.isoformat(),
            "Start": start_time.isoformat(),
        }
        assert (
            SchedulerOutputs.model_validate(
                outputs, context={"format": "slurm"}
            ).idle_time
            == idle
        )

    @staticmethod
    def test_should_validate_end_and_start_time_as_elapsed(
        submit_time: datetime.datetime,
        end_time: datetime.datetime,
        start_time: datetime.datetime,
        elapsed: datetime.datetime,
    ) -> None:
        outputs = {
            "Submit": submit_time.isoformat(),
            "End": end_time.isoformat(),
            "Start": start_time.isoformat(),
        }
        assert (
            SchedulerOutputs.model_validate(
                outputs, context={"format": "slurm"}
            ).elapsed
            == elapsed
        )

    @staticmethod
    def test_should_validate_missing_time(
        submit_time: datetime.datetime,
    ) -> None:
        outputs = {
            "Submit": submit_time.isoformat(),
        }
        assert SchedulerOutputs.model_validate(outputs)

    @staticmethod
    def test_should_validate_integer_memory(
        val: float, num_type: type[int | float], units: str
    ) -> None:
        memory = f"{num_type(val)}{units}"
        assert validate_memory(memory, lambda x: x, None) == val

    @staticmethod
    @pytest.mark.parametrize("units", [""])
    def test_should_validate_memory_without_units(
        val: float, num_type: type[int | float], units: str
    ) -> None:
        memory = f"{num_type(val)}{units}"
        assert validate_memory(memory, lambda x: x, None) == val

    @staticmethod
    @pytest.mark.parametrize("num_type", [float])
    def test_should_validate_decimal_memory(
        val: float, num_type: type[int | float], units: str
    ) -> None:
        memory = f"{num_type(val)}{units}"
        assert validate_memory(memory, lambda x: x, None) == val


class TestSchedulerOutputsFromDirectory:
    @staticmethod
    @pytest.fixture(name="slurm_output_file_to_copy")
    def fixture_slurm_output_file_to_copy() -> str:
        return "slurm-22189181.out"

    @staticmethod
    @pytest.mark.output_files("job_stats", "slurm_output_file")
    def test_should_load_scheduler_outputs(
        populate_outputs: pathlib.Path,
    ) -> None:
        assert SchedulerOutputs.from_directory(populate_outputs)
