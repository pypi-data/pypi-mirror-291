"""Tools for DFT job automation on massively parallel computing resources."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import timedelta
import importlib
from json import JSONEncoder
import logging
from typing import Any
import warnings

from ase import Atoms
from ase import __version__ as ase_version
from ase.io.jsonio import decode
from ase.io.jsonio import encode
from monty.json import MSONable

from autojob.coordinator.classification import CalculationType
from autojob.coordinator.classification import CalculatorType
from autojob.coordinator.classification import StudyType
from autojob.coordinator.job import JobError
from autojob.hpc import Partition
from autojob.settings import AutojobSettings
from autojob.utils.parsing import TimedeltaTuple

logger = logging.getLogger(__name__)


if tuple(ase_version) <= tuple("3.22.1"):
    warnings.warn(
        "Your ASE version ({ase_version}) is <= 3.22.1. Please upgrade your "
        "ASE version: pip install --upgrade https://gitlab.com/ase/ase/-/"
        "archive/master/ase-master.zip",
        UserWarning,
        stacklevel=1,
    )


class MyEncoder(JSONEncoder):
    """Encode custom types."""

    def default(self, o: Any) -> Any:
        """The default encoder."""
        logger.debug(f"Encoding {o!r}")

        if isinstance(o, Atoms):
            encoded_o = {
                "@class": "Atoms",
                "@module": "ase.atoms",
                "atoms_json": encode(o),
            }

        elif isinstance(o, MSONable):
            encoded_o = o.as_dict()

        elif isinstance(
            o, CalculationType | JobError | CalculatorType | StudyType | tuple
        ):
            encoded_o = {
                "@class": o.__class__.__name__,
                "value": getattr(o, "value", o),
            }

        elif isinstance(o, timedelta):
            encoded_o = {
                "@class": "Timedelta",
                "value": TimedeltaTuple.from_timedelta(o).to_slurm_time(),
            }

        elif isinstance(o, Partition):
            encoded_o = {"@class": o.__class__.__name__, "value": str(o)}

        elif isinstance(o, Mapping):
            encoded_o = {k: self.default(v) for k, v in o.items()}

        else:
            encoded_o = super().default(o)

        logger.debug(f"Encoded {o!r} as: {encoded_o}")
        return encoded_o


def my_object_hook(d: dict) -> Any:
    """Decode custom types."""
    logger.debug(f"Decoding {d!r}")

    match d.get("@class"):
        case "Atoms":
            decoded_d = decode(d["atoms_json"])
        case "Timedelta":
            decoded_d = TimedeltaTuple.from_slurm_time(
                d["value"]
            ).to_timedelta()
        case "CalculationType":
            decoded_d = CalculationType(d["value"])
        case "CalculatorType":
            decoded_d = CalculatorType(d["value"])
        case "StudyType":
            decoded_d = StudyType(d["value"])
        case "Partition":
            decoded_d = Partition(d["value"])
        case "JobError":
            decoded_d = JobError(d["value"])
        case None:
            decoded_d = d
        case _:
            parts = d["@module"].split(".")
            package = ".".join(parts[:-1])
            mod = importlib.import_module(name=d["@module"], package=package)
            cls = getattr(mod, d["@class"])
            decoded_d = cls.from_dict(d)

    logger.debug(f"Decoded {d!r} as: {decoded_d!r}")
    return decoded_d


SETTINGS = AutojobSettings()
