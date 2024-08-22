"""Write Python and SLURM scripts.

.. deprecated:: Use :meth:`.calculation.Calculation.to_directory` instead.
"""

import pathlib
import stat
from typing import TYPE_CHECKING
from typing import Any

from ase import io
import jinja2

from autojob import SETTINGS
from autojob.hpc import SchedulerInputs
from autojob.utils.parsing import TimedeltaTuple

if TYPE_CHECKING:
    from autojob.coordinator import job

_MAX = 10


class Scripter:
    """Template scripts with parameter values."""

    @staticmethod
    def get_loader() -> jinja2.BaseLoader:
        """Return the Jinja template loader."""
        if SETTINGS.TEMPLATE_DIR:
            loader = jinja2.FileSystemLoader(SETTINGS.TEMPLATE_DIR)
        else:
            loader = jinja2.PackageLoader(__name__.split(".", maxsplit=1)[0])
        return loader

    @staticmethod
    def create_python_script(
        parameters: dict["job.CalculationParameter", Any],
        calculator: str,
        structure: str,
        job_dir: pathlib.Path,
        template: str = SETTINGS.PYTHON_TEMPLATE,
    ) -> pathlib.Path:
        """Creates the Python script.

        Args:
            parameters: A map from :class:`.job.CalculationParameter`s to their values.
            calculator: The name of the ASE calculator in use.
            structure: The filename of the structure to use.
            job_dir: The directory in which to write the Python script.
            template: The name of the template to use.
        """
        parameters = Scripter.parse_kpts(parameters)
        parameters = Scripter.parse_dipol(structure, parameters)
        parameters = {
            str(key): repr(value)
            for key, value in parameters.items()
            if value is not None
        }

        env = jinja2.Environment(
            loader=Scripter.get_loader(),
            autoescape=False,  # noqa: S701
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        template = env.get_template(template)
        filename = job_dir.joinpath(SETTINGS.PYTHON_SCRIPT)

        with filename.open(mode="x", encoding="utf-8") as file:
            file.write(
                template.render(
                    calculator=calculator,
                    structure=structure,
                    parameters=parameters,
                    run_bader=False,
                    run_chargemol=False,
                )
            )
            st = filename.stat()
            filename.chmod(
                st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
            )

        return filename

    # TODO: Remove and add step prior to script creation that creates "KPTS"
    @staticmethod
    def parse_kpts(
        parameters: dict["job.CalculationParameter", Any],
    ) -> tuple | None:
        """Convert the specified k-points into a valid form."""
        kx, ky, kz = (None, None, None)

        placeholder = {}

        for key, value in parameters.items():
            if str(key).startswith("KPTS_"):
                match str(key)[-1]:
                    case "X":
                        kx = value
                    case "Y":
                        ky = value
                    case "Z":
                        kz = value
            else:
                placeholder[key] = value

        if None not in (kx, ky, kz):
            placeholder["kpts"] = (kx, ky, kz)

        return placeholder

    @staticmethod
    def parse_dipol(  # noqa: PLR0912
        structure: pathlib.Path,
        parameters: dict["job.CalculationParameter", Any],
    ) -> tuple | None:
        """Convert the specified dipole information into a valid form."""
        dx, dy, dz = (None, None, None)

        placeholder = {}

        for key, value in parameters.items():
            if str(key).startswith("DIPOL_"):
                match str(key)[-1]:
                    case "X":
                        if value == "x-centre-of-mass":
                            atoms = io.read(structure)
                            dx = atoms.get_center_of_mass(scaled=True)[0]
                        else:
                            dx = value
                    case "Y":
                        if value == "y-centre-of-mass":
                            atoms = io.read(structure)
                            dy = atoms.get_center_of_mass(scaled=True)[1]
                        else:
                            dy = value
                    case "Z":
                        if value == "z-centre-of-mass":
                            atoms = io.read(structure)
                            dz = atoms.get_center_of_mass(scaled=True)[2]
                        else:
                            dz = value
            else:
                placeholder[key] = value

        if None not in (dx, dy, dz):
            placeholder["dipol"] = (dx, dy, dz)

        return placeholder

    @staticmethod
    def create_slurm_script(
        *,
        calculator: str,
        submission_parameters: dict,
        job_dir: pathlib.Path,
        compute_canada_format: bool,
        structure: str,
        slurm_script: str | None = None,
        template_file: str = SETTINGS.SLURM_TEMPLATE,
    ) -> pathlib.Path:
        """Creates the SLURM script.

        Args:
            calculator: The name of the ASE calculator in use.
            submission_parameters: A map from submission parameter names to
                their values.
            job_dir: The directory in which to write the SLURM script.
            compute_canada_format: Whether or not the script is to be rendered
                in ComputeCanada format.
            structure: The filename of the structure to use.
            slurm_script: The name to give the SLURM script when writing.
                Defaults to ``SETTINGS.SLURM_SCRIPT``.
            template_file: The name of the template to use. Defaults to
                ``SETTINGS.SLURM_TEMPLATE``.
        """
        partitions = submission_parameters["partitions"]
        nodes = submission_parameters["nodes"]
        memory = (
            f"{int(submission_parameters['memory'][0])}"
            f"{submission_parameters['memory'][1]}"
        )
        cores = submission_parameters["cores"]
        days = submission_parameters["run time"]["days"]
        hours = submission_parameters["run time"]["hours"]
        mins = submission_parameters["run time"]["minutes"]
        auto_restart = submission_parameters["auto_restart"]
        files_to_copy = submission_parameters["files_to_copy"]
        files_to_delete = submission_parameters["files_to_delete"]
        mail_type = submission_parameters["mail-type"]
        mail_user = submission_parameters["mail-user"]
        account = submission_parameters["account"]

        delta = TimedeltaTuple(
            days=days, hours=hours, minutes=mins
        ).to_timedelta()

        job_name = f"{structure}-{job_dir.parent.name}"

        parameters = SchedulerInputs(
            job_name=job_name,
            partition=partitions,
            mem_per_cpu=memory,
            nodes=nodes,
            cores_per_node=cores,
            time=delta,
            mail_type=mail_type,
            mail_user=mail_user,
            account=account,
        ).model_dump(exclude_none=True, by_alias=True, mode="json")

        slurm_parameters = {}

        for k, v in parameters.items():
            key = f"--{k}" if len(k) > 1 else f"-{k}"
            if v:
                slurm_parameters[key] = v

        env = jinja2.Environment(
            loader=Scripter.get_loader(),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        template = env.get_template(template_file)
        slurm_script = slurm_script or SETTINGS.SLURM_SCRIPT
        filename = job_dir.joinpath(slurm_script)

        with filename.open(mode="x", encoding="UTF-8") as file:
            file.write(
                template.render(
                    parameters=slurm_parameters,
                    auto_restart=auto_restart,
                    files_to_copy=files_to_copy,
                    files_to_delete=files_to_delete,
                    compute_canada_format=compute_canada_format,
                    calculator=calculator,
                    python_script=SETTINGS.PYTHON_SCRIPT,
                    slurm_script=slurm_script,
                )
            )

        return filename
