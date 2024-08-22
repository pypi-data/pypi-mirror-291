"""Create workflows from multiple step."""

from collections.abc import Iterable
from copy import deepcopy
from graphlib import TopologicalSorter
import json
import pathlib
from typing import Any
from typing import Literal
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field

from autojob import SETTINGS
from autojob.parametrizations import VariableReference

AnchorLevel = Literal[0, 1]


class Step(BaseModel):
    """A step in a workflow."""

    workflow_step_id: UUID
    task_type: str
    progression: Literal["independent", "dependent"] = Field(
        default="independent",
        description="How the step is connected to the tasks of the previous "
        "step. 'dependent' indicates that the given step cannot start until "
        "every task in the previous step has completed. 'independent' "
        "indicates the opposite.",
    )
    parametrizations: list[list[VariableReference[Any]]] = Field(min_length=1)


class Workflow(TopologicalSorter):
    """The structure of a workflow."""

    def __init__(self, graph: dict[str, Iterable[str]]) -> None:
        """Initialize a `Workflow`.

        Args:
            graph: A directed-acyclic graph representing the workflow.
        """
        self._graph = {k: list(v) for k, v in deepcopy(graph).items()}
        super().__init__(graph)

    def __getitem__(self, key: Any) -> list[str]:
        """Get the ancestors of the step indicated by `key`."""
        return self._graph[key]

    def get_predecessors(self, step_id: str) -> list[str]:
        """Return the immediate ancestors of a workflow step.

        Args:
            step_id: A string representation of a workflow step ID.
        """
        return self._graph[step_id]

    def get_next_steps(
        self, step_id: str, record: list[str] | None = None
    ) -> list[str]:
        """Get all successors of a step.

        Args:
            step_id: A string representation of a workflow step ID
            record: A list of strings where each string represents the workflow
                step ID of a completed task. If None, all successive steps will
                be returned. Defaults to None.

        Returns:
            A list of strings where each string represents a workflow step ID.
        """
        active_steps: list[str] = []

        for successor, predecessors in self._graph.items():
            if step_id in predecessors and (
                record is None
                or all(predecessor in record for predecessor in predecessors)
            ):
                active_steps.append(successor)

        return active_steps

    @classmethod
    def from_directory(cls, dir_name: pathlib.Path) -> "Workflow":
        """Construct a `Workflow` from a directory."""
        workflow_file = dir_name.joinpath(SETTINGS.WORKFLOW_FILE)
        with workflow_file.open(mode="r", encoding="utf-8") as wf:
            return cls(json.load(wf))
