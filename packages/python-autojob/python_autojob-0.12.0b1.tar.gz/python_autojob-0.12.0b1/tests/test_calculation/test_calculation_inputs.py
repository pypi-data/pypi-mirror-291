import pathlib
from typing import Any
from typing import TextIO

from ase import Atoms
from ase.build import bulk
from ase.build import molecule
import pytest

from autojob.calculation.calculation import CalculationInputs

# TODO: replace with parameters.CalculatorType
from autojob.coordinator.classification import CalculatorType


@pytest.fixture(
    name="calculator",
    params=list(CalculatorType)[:3],
)
def fixture_calculator(request: pytest.FixtureRequest) -> CalculatorType:
    calculator: CalculatorType = request.param
    return calculator


@pytest.fixture(
    name="structure_name", params=("in.traj", "Cu.traj", "relax.traj")
)
def fixture_structure_name(request: pytest.FixtureRequest) -> str:
    structure_name: str = request.param
    return structure_name


@pytest.fixture(
    name="atoms",
    params=[
        Atoms("C"),
        bulk("Cu"),
        molecule("NH3"),
    ],
)
def fixture_atoms(request: pytest.FixtureRequest) -> Atoms:
    atoms: Atoms = request.param
    return atoms


@pytest.fixture(
    name="calculator_as_name", params=["initial", "capitalized", None]
)
def fixture_calculator_as_name(
    calculator: CalculatorType, request: pytest.FixtureRequest
) -> str | None:
    match request.param:
        case "initial":
            return str(calculator).capitalize()[0]
        case "capitalized":
            return str(calculator).capitalize()
    return None


class TestCalculationInputs:
    @staticmethod
    def test_should_instantiate_dict() -> None:
        calculation_inputs = CalculationInputs(atoms=Atoms("C"), parameters={})
        assert calculation_inputs


class TestExtractImportedASECalculators:
    @staticmethod
    def test_should_extract_calculators_from_run_py(
        write_run_py: TextIO,
        calculator: str,
        calculator_as_name: str | None,
    ) -> None:
        extracted_calculators = (
            CalculationInputs.extract_imported_ase_calculators(
                stream=write_run_py
            )
        )
        assert extracted_calculators[0] == (
            str(calculator).capitalize(),
            calculator_as_name,
        )

    @staticmethod
    def test_should_extract_calculators_from_run_py_if_calc_aliased(
        write_run_py: TextIO,
        calculator_as_name: str | None,
    ) -> None:
        extracted_parameters = (
            CalculationInputs.extract_imported_ase_calculators(
                stream=write_run_py
            )
        )
        extracted_calculator_as_name = extracted_parameters[0][1]
        assert extracted_calculator_as_name == calculator_as_name


class TestExtractCalculationParameters:
    @staticmethod
    def test_should_extract_parameters_from_run_py(
        write_run_py: TextIO,
        parameters: dict[str, Any],
        calculator: CalculatorType,
    ) -> None:
        (
            _,
            extracted_parameters,
        ) = CalculationInputs.extract_calculation_parameters(
            stream=write_run_py
        )
        assert calculator == extracted_parameters.pop("calculator", None)
        assert extracted_parameters == parameters


class TestCalculationInputsFromDirectory:
    @staticmethod
    @pytest.mark.input_files("python_script")
    def test_should_load_calculation_inputs_from_directory(
        populate_inputs: pathlib.Path,
        calculation_inputs: CalculationInputs,
        calculator: CalculatorType,
    ) -> None:
        assert (
            calculation_inputs.model_dump()
            == CalculationInputs.from_directory(
                dir_name=populate_inputs,
                calculator_type=calculator,
            ).model_dump()
        )
