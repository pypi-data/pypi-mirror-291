"""Associate calculations with a reaction mechanism."""

import logging
import math
import re
from typing import Any
from typing import NamedTuple

from autojob.coordinator.classification import CalculationType

logger = logging.getLogger(__name__)

_re_id1 = re.compile(r"based on (?P<id>(?:c|j)[A-Za-z0-9]{9})(;)?\b")
_re_id2 = re.compile(
    r"(?:(?!converged|calculation|converging))(?P<id>(?:c|j)[A-Za-z0-9]{9})\b"
)


class ElementaryStep(NamedTuple):
    """An elementary reaction step relative to a reference.

    Attributes:
        net_hydrogens: The net number of hydrogens transferred from the
            reference to the ``ElementaryStep``. Defaults to 0.
        net_electrons: The net number of electrons transferred from the
            reference to the ``ElementaryStep``. Defaults to 0.
        net_water_lost: The net number of water atoms lost from the
            reference to the ``ElementaryStep``. Defaults to 0.
        reference: The reference state for the ``ElementaryStep``. Defaults to
            None. If provided, `reference` can be used to relate
            `ElementaryS`tep` s defined for different references.

    Note:
        ``net_water_lost`` is defined opposite to how ``net_hydrogens`` and
        ``net_electrons`` are defined so that simple tuple comparisons can
        be used to order ``ElementaryStep`` s according to typical
        electronchemical reactions. However, this ordering is not absolute
        as there may be reaction mechanisms for which electron transfer
        precedes proton transfer.
    """

    net_hydrogens: int = 0
    net_electrons: int = 0
    net_water_lost: int = 0
    reference: str | None = None

    def apply_comp_hydrogen_model(
        self,
        energy_h2: float,
        energy_h2o: float,
        *,
        initial: float,
        final: float,
        applied_potential: float = 0.0,
    ) -> float:
        """Calculate an energy using the computational hydrogen electrode (CHE).

        This method follows the formalism outlined in:

        J. K. Nørskov, J. Rossmeisl, A. Logadottir, L. Lindqvist, J. R. Kitchin, T. Bligaard, and H. Jónsson
        The Journal of Physical Chemistry B 2004 108 (46), 17886-17892
        DOI: 10.1021/jp047349j

        Args:
            energy_h2: The energy of gas phase hydrogen to use for the
                calculation.
            energy_h2o: The energy of gas phase water to use for the
                alculation.
            initial: The energy of the referece state to use for the
                calculation. This should be the energy of the species
                identified by
                :attr:`autojob.harvest.mechanism.ElementaryStep.reference`.
            final: The energy of the final state to use for the calculation.
            applied_potential: The applied potential in Volts.

        Returns:
            The energy under the CHE formalism.
        """
        return (
            final
            - initial
            - energy_h2 * (self.net_hydrogens / 2)
            + energy_h2o * self.net_water_lost
            - applied_potential * self.net_electrons
        )


class MechanisticEntry(NamedTuple):
    """Calculated thermodynamic data for an elementary step.

    Attributes:
        elementary_step: The :class:`ElementaryStep` with which the
            ``MechanisticEntry`` is associated.
        name: A string labeling the entry. For example, the catalyst or
            molecule name.
        energy: A float representing the calculated energy for the entry.
    """

    elementary_step: ElementaryStep
    name: str
    energy: float


STEPS = {
    "CO2": ElementaryStep(),
    "COOH": ElementaryStep(1, 1),
    "OCHO": ElementaryStep(1, 1),
    "CO": ElementaryStep(2, 2, 1),
    "HCOOH": ElementaryStep(2, 2),
    "H": ElementaryStep(),
}


def find_ancestors(
    jobs: list[dict[str, Any]],
    data: dict[str, Any],
    ancestor_calculation: str,
    ancestor_job: str,
) -> list[dict[str, Any]]:
    """Find the ancestor calculations of given calculation."""
    ancestors = []
    for job in jobs:
        if (
            job.get("Calculation ID", None) == ancestor_calculation
            and job.get("Job ID", None) == ancestor_job
        ):
            if data["Calculation Type"] != str(CalculationType.VIB):
                grandparent_calculation = grandparent_job = None
                if match := _re_id2.search(data["Calculation Notes"]):
                    grandparent_calculation = match.group("id")
                if match := _re_id2.search(data["Job Notes"]):
                    grandparent_job = match.group("id")

                if None in (grandparent_calculation, grandparent_job):
                    logger.warning(
                        f"Unable to determine grandparents of {data['Job ID']}"
                        f" (parents of {ancestor_job})"
                    )
                else:
                    ancestors.extend(
                        find_ancestors(
                            jobs, job, grandparent_calculation, grandparent_job
                        )
                    )
            ancestors.append(job)
    return ancestors


def find_ancestor(
    graph: dict[str, str],
    data: dict[str, Any],
    all_data: list[dict[str, Any]],
) -> str:
    """Find the ancestor calculation of given calculation."""
    job_id = current_job = data["Job ID"]
    calculations_to_jobs: dict[str, list[str]] = {}

    for d in all_data:
        calculation_id = d["Calculation ID"]
        if calculation_id not in calculations_to_jobs:
            calculations_to_jobs[calculation_id] = []
        calculations_to_jobs[calculation_id].append(d["Job ID"])

    missing = "Ancestor ({0}) of job ({1} from {2}) not in data set"
    ancestor_job, ancestor_calculation = graph[job_id]

    while ancestor_job in graph and ancestor_job != current_job:
        current_job = ancestor_job
        ancestor_job, ancestor_calculation = graph[current_job]

        # Try to find upstream job using calculation
        if (
            any([ancestor_job, ancestor_calculation])
            and ancestor_job not in graph
        ):
            ancestors = calculations_to_jobs.get(
                ancestor_calculation, [ancestor_job]
            )
            ancestor_job = ancestors[0] if ancestors else ancestor_job

    if ancestor_job is None:
        return current_job

    logger.warning(missing.format(ancestor_job, current_job, job_id))
    return ancestor_job


def build_job_graph(
    all_data: list[dict[str, Any]],
) -> dict[str, tuple[str | None, str | None]]:
    """Build directed acyclic graph representing the connectivity of the jobs.

    Args:
        all_data: A list of dictionaries representing job data. Job
            connectivity is determined based on the "Job Notes" key.

    Returns:
        A dictionary mapping jobs to their ancestor (``job``,
        ``calculation``). If the ancestor of a job cannot be found, its
        ancestor is (None, None).
    """
    graph: dict[str, tuple[str | None, str | None]] = {}

    for data in all_data:
        ancestor_calculation = ancestor_job = None
        if match := _re_id1.search(data["Job Notes"]):
            ancestor_job = match.group("id")
        elif matches := _re_id2.findall(data["Job Notes"]):
            ancestor_job = matches[-1] if matches[-1] != ancestor_job else None
        if matches := _re_id2.findall(data["Calculation Notes"]):
            ancestor_calculation = (
                matches[-1] if matches[-1] != ancestor_calculation else None
            )
        graph[data["Job ID"]] = (ancestor_job, ancestor_calculation)

    return graph


def aggregate_mechanism_data(
    all_data: list[dict[str, Any]],
) -> list[list[dict[str, Any]]]:
    """Group all data deemed to belong to the same mechanism entry.

    Data is determined to be grouped based on whether any other calculation ids
    appear in their "Calculation Notes" key.

    Args:
        all_data: A list of dictionaries containing the data. Each dictionary
            must contain the following keys:
            - "Calculation Notes"
            - "Job Notes"

    Returns:
        A list of lists of dictionaries grouped by mechanism entry.
    """
    # Build reaction network based on metadata
    graph = build_job_graph(all_data)
    networks: dict[str, list[dict[str, Any]]] = {}

    for data in all_data:
        head_node = find_ancestor(graph, data, all_data)

        if head_node not in networks:
            networks[head_node] = []
        networks[head_node].append(data)

    grouped_data = []
    for network in networks.values():
        grouped_data.append(
            sorted(network, key=lambda d: d.get("SLURM Job ID", math.inf))
        )

    return grouped_data
