"""Utilities for creating tasks from existing task directories."""

from typing import TYPE_CHECKING
from typing import Any

from autojob.hpc import SchedulerInputs
from autojob.parametrizations import VariableReference

if TYPE_CHECKING:
    from autojob.calculation.calculation import Calculation


def substitute_context(
    mods: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    """Substitute context values into formatted strings.

    Args:
        mods: A dictionary mapping parameter names to values. String values
            will be subsituted according to context values.
        context: A dictionary mapping variable names to their values.
            Variables with names corresponding to template names will be
                substituted.

    Returns:
        A copy of `mods` with templatted values substituted for their variable
        values.
    """
    new_mods: dict[str, Any] = {}

    for key, value in mods.items():
        if isinstance(value, str):
            new_mods[key] = value.format(**context)
        else:
            new_mods[key] = value

    return new_mods


def create_parametrization(
    previous: "Calculation",
    calc_mods: dict[str, Any],
    slurm_mods: dict[str, Any],
) -> list[VariableReference[Any]]:
    """Create a parametrization from parameter modifications.

    Args:
        previous: A :class:`.calculation.Calculation` representing the previous calculation.
        calc_mods: A dictionary containing modifications to calculator
            parameters.
        slurm_mods: A dictionary containing modifications to SLURM
            parameters.

    Returns:
        A list of ``VariableReference`` s that can be used to set the values
        of the new calculation.
    """
    parameters = {**previous.calculation_inputs.parameters}
    parameters.update(calc_mods)
    scheduler_inputs = previous.scheduler_inputs.model_dump(exclude_none=True)
    context = previous.task_metadata.model_dump(exclude_none=True)
    context["structure"] = previous.task_inputs.atoms.info.get(
        "structure", "{structure}"
    )
    mods = substitute_context(slurm_mods, context)

    SchedulerInputs.update_values(scheduler_inputs, mods)
    parametrization: list[VariableReference] = [
        VariableReference(
            set_path=["calculation_inputs", "parameters"],
            constant=parameters,
        ),
        VariableReference(
            set_path=["calculation_inputs", "ase_calculator"],
            constant=previous.calculation_inputs.ase_calculator,
        ),
        VariableReference(
            set_path=["scheduler_inputs"],
            constant=scheduler_inputs,
        ),
    ]
    return parametrization
