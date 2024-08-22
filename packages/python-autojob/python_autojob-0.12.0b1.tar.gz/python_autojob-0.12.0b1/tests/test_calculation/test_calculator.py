from copy import deepcopy

import pytest

from autojob.calculation.calculators import CalculatorConfiguration
from autojob.calculation.parameters import CalculatorParameter
from autojob.calculation.parameters import MappingParameter
from autojob.calculation.parameters import NumberMappingParameter
from autojob.calculation.parameters import NumberParameter
from autojob.calculation.parameters import NumberRange
from autojob.calculation.parameters import NumberSequenceParameter
from autojob.calculation.parameters import SequenceParameter


@pytest.fixture(name="calculator_configuration")
def fixture_calculculator_configuration():
    param1 = CalculatorParameter(
        name="Param1",
        allowed_types=(str,),
        special_values=[],
        default="Normal",
        description="first parameter",
    )
    param2 = NumberParameter(name="Param2", allow_floats=True, default=1)
    param3 = SequenceParameter(
        member_types=[str], name="Param3", default=["chicken"]
    )
    param4 = NumberSequenceParameter(
        name="Param4",
        allow_floats=False,
        number_range=NumberRange(lower_bound=0, upper_bound=10),
    )
    param5 = MappingParameter(
        member_types=[str], name="Param5", default={"a": 1}
    )
    param6 = NumberMappingParameter(
        name="Param6",
        allow_floats=True,
        number_range=NumberRange(lower_bound=-10),
    )
    return CalculatorConfiguration(
        calculator_parameters=(param1, param2, param3, param4, param5, param6)
    )


class TestCalculatorConfigurationEquals:
    @staticmethod
    def test_should_equate_to_copy(
        calculator_configuration: CalculatorConfiguration,
    ):
        dupe = deepcopy(calculator_configuration)
        assert dupe == calculator_configuration


class TestCalculatorConfigurationMSONable:
    @staticmethod
    def test_should_recreate_calculator_configuration(
        calculator_configuration: CalculatorConfiguration,
    ):
        assert calculator_configuration == CalculatorConfiguration.from_dict(
            calculator_configuration.as_dict()
        )
