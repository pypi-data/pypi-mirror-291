"""I/O functions for the utility scripts (compiled here for consistency)."""

from csv import DictWriter
from datetime import UTC
from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any
from typing import Literal

from autojob.calculation.calculation import Calculation
from autojob.calculation.infrared import Infrared
from autojob.calculation.vibration import Vibration

logger = logging.getLogger(__name__)


def flatten_calculations(
    calculations: list[Calculation],
) -> list[dict[str, Any]]:
    """Flatten each calculation into a CSV-friendly format.

    Args:
        calculations: The calculations to flatten.

    Returns:
        A list of dictionaries mapping calculation fields (e.g., ``energy``,
        ``forces``, ``zpe_correction``) to their values. The keys of
        nested dictionaries such as the calculation parameters are also
        accessible.
    """
    flattened_calculations = []

    for calculation in calculations:
        metadata = calculation.task_metadata.model_dump(mode="json")
        info = (
            calculation.task_inputs.atoms.info
            if calculation.task_inputs.atoms
            else {}
        )
        calc_inputs = calculation.calculation_inputs

        calc_outputs_shell = {}

        if calc_outputs := calculation.calculation_outputs:
            calc_outputs_shell = calc_outputs.model_dump(mode="json")

        slurm_outputs_shell = {}

        if slurm_outputs := calculation.scheduler_outputs:
            slurm_outputs_shell = slurm_outputs.model_dump(mode="json")

        vib_outputs_shell = {}

        if isinstance(calculation, Vibration) and (
            vib_outputs := calculation.vibration_outputs
        ):
            vib_outputs_shell = vib_outputs.model_dump(mode="json")

        ir_outputs_shell = {}

        if isinstance(calculation, Infrared) and (
            ir_outputs := calculation.infrared_outputs
        ):
            ir_outputs_shell = ir_outputs.model_dump(mode="json")

        task_outcome = (
            calculation.task_outputs.outcome
            if calculation.task_outputs
            else None
        )

        flattened = {
            **metadata,
            **info,
            **calc_inputs.parameters,
            **calc_inputs.model_dump(mode="json", exclude={"parameters"}),
            **calc_outputs_shell,
            **slurm_outputs_shell,
            **vib_outputs_shell,
            **ir_outputs_shell,
            "outcome": task_outcome,
        }
        flattened_calculations.append(flattened)

    return flattened_calculations


def archive_json(
    calculations: list[Calculation],
    dest: Path | None = None,
) -> None:
    """Archive a list of calculations in JSON format.

    Args:
        calculations: A list of calculations to archive.
        dest: The filename to use archive the calculation. Defaults to
            ``"database_<TIME_STAMP>.json"`` where ``TIME_STAMP`` is the
            current time in ISO format.
    """
    time_stamp = (
        datetime.now(UTC)
        .isoformat()
        .replace(":", "_")
        .replace("+", "_")
        .replace("-", "_")
        .replace(".", "_")
    )
    json_archive = dest or Path.cwd().joinpath(f"{time_stamp}.json")
    to_dump = {
        d.task_metadata.task_id: d.model_dump(mode="json")
        for d in calculations
    }
    with json_archive.open(mode="w", encoding="utf-8") as file:
        json.dump(
            to_dump,
            fp=file,
            indent=4,
            sort_keys=True,
        )

    logger.info("JSON archive written to %s", json_archive)


def archive_csv(
    calculations: list[Calculation],
    dest: Path | None = None,
) -> None:
    """Archive a list of calculations in CSV format.

    Args:
        calculations: A list of calculations to archive.
        dest: The filename to use archive the calculation. Defaults to
            ``"database_<TIME_STAMP>.csv"`` where ``TIME_STAMP`` is the
            current time in ISO format.
    """
    time_stamp = (
        datetime.now(UTC)
        .isoformat()
        .replace(":", "_")
        .replace("+", "_")
        .replace("-", "_")
        .replace(".", "_")
    )
    csv_archive = dest or Path.cwd().joinpath(f"{time_stamp}.csv")
    flattened = flatten_calculations(calculations)
    fieldnames: set[str] = set()

    for flat in flattened:
        fieldnames = fieldnames.union(
            key
            for key, v in flat.items()
            if not isinstance(v, list | dict | None)
        )

    with csv_archive.open(mode="w", encoding="utf-8") as file:
        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in flattened:
            writer.writerow({k: row.get(k, None) for k in fieldnames})

    logger.info("CSV archive written to %s", csv_archive)


def archive(
    filename: str,
    archive_mode: Literal["csv", "json", "both"],
    harvested: list[Calculation],
) -> None:
    """Archive completed calculations with the given format.

    Args:
        filename: The filename with which to archive the calculations.
        archive_mode: The format with which to archive the calculations. Must
            be one of ``"csv"``, ``"json"``, or ``"both"``.
        harvested: The list of calculations to archive.
    """
    time_stamp = (
        datetime.now(UTC)
        .isoformat()
        .replace(":", "_")
        .replace("+", "_")
        .replace("-", "_")
        .replace(".", "_")
    )
    stem = f"{filename}_{time_stamp}"

    if archive_mode == "csv":
        dest = Path(f"{stem}.{archive_mode}")
        archive_csv(calculations=harvested, dest=dest)
    elif archive_mode == "json":
        dest = Path(f"{stem}.{archive_mode}")
        archive_json(calculations=harvested, dest=dest)
    elif archive_mode == "both":
        csv_dest = Path(f"{stem}.csv")
        json_dest = Path(f"{stem}.json")
        archive_csv(calculations=harvested, dest=csv_dest)
        archive_json(calculations=harvested, dest=json_dest)
