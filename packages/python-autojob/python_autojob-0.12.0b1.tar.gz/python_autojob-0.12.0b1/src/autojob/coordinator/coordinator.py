"""Coordinate the creation and submission of jobs.

The :class:`Coordinator` class stores references to the calculator
and submission parameter groups used and can generate and submit jobs
created from these parameter groups.
"""

from collections.abc import Iterable
import datetime
from itertools import product
import json
import logging
from pathlib import Path
import shutil
import subprocess
from typing import TYPE_CHECKING
from typing import Any

import click
import shortuuid

from autojob import SETTINGS
from autojob.advance.advance import submit_new_task
from autojob.calculation.calculation import FILES_TO_COPY
from autojob.calculation.calculation import FILES_TO_DELETE
from autojob.calculation.parameters import CalculatorType
from autojob.coordinator import classification
from autojob.coordinator import scripter
from autojob.coordinator import validation
from autojob.coordinator.gui import groups
from autojob.coordinator.gui import gui

if TYPE_CHECKING:
    from autojob.coordinator import job


logger = logging.getLogger(__name__)


class Coordinator:
    """Create and submit jobs from parameter groups.

    Attributes:
        app: The running :class:`.gui.GUI` instance.
        submit_dir: The directory in which new study groups will be created.
        slurm_scripts: A list of paths to slurm scripts.
        study_uuids: A list of UUIDs of the studies in the study groups.
        compute_canada_format: Whether or not the slurm scripts are to be
            created in ComputeCanada format.
    """

    def __init__(self, app: "gui.GUI", dest: Path | None = None) -> None:
        """Initialize a `Coordinator`.

        Args:
            app: The running :class:`.gui.GUI` instance.
            dest: The directory in which new study groups will be created.
                Defaults to the current working directory.
        """
        self.app: gui.GUI = app
        self.submit_dir = dest or Path.cwd()
        # set by running self.create_directories()
        self.slurm_scripts: list[Path] = []
        self.study_uuids: dict[str, str] = {}
        self.compute_canada_format = False

    @property
    def structure_groups(self) -> dict[str, groups.StructureGroup]:
        """A dictionary mapping structure group names to structure groups."""
        return self.app.tabs[
            "Structure Selection"
        ].panel.group_button_frame.structure_groups

    @property
    def adsorbates(self) -> dict[str, list[str]]:
        """A dictionary mapping structure group names to adsorbate lists."""
        # Get adsorbates by structure group
        # self.app.tabs['Structure Selection']
        # .panels['adsorbate selection'].adsorbates

    @property
    def complexes(self) -> dict[str, dict[str, dict[str, str]]]:
        """A dictionary mapping structure group names to nested dictionaries.

        Each nested dictionary maps structure names to a maps between adsorbate
        names and adsorbate-complex structure files.

        Example:
            group_name = "group 1"
            structure = "structure 1"
            adsorbate = "adsorbate 1"
            complexes = coordinator.complexes
            group = complexes[group_name]

            # A map from adsorbate names to adsorbate complex file names
            adsorbate_to_structure_complex = group[structure]

            # The file name for an adsorbate complex
            complex_structure = adsorbate_to_structure_complex[adsorbate]
        """
        # Get adsorbate-catalyst complexes by structure group, structure, and
        # adsorbate

    # TODO: implement
    @property
    def adsorption_groups(self) -> dict[str, list[dict[str, list]]]:
        """A dictionary mapping structure group names to adsorption groups."""
        if self.study_type != classification.StudyType.ADSORPTION:
            return {}

        adsorption_groups: dict[
            str,  # structure group names
            list[dict[str, str]],  # references or complex  # job
        ] = []

        for s_group, structures in self.structure_groups.items():
            for structure in structures:
                for calculation_parameters in product(
                    self.calc_params[s_group].values.values()
                ):
                    calc_params = dict(
                        zip(
                            self.calc_params.keys(),
                            calculation_parameters,
                            strict=True,
                        )
                    )
                    subm_params = self.subm_params_for(structure, calc_params)

                    if not subm_params:
                        continue

                    # Create job for catalyst reference
                    parameters = {
                        "calculation parameters": calc_params,
                        "submission parameters": subm_params,
                    }
                    new_job = {
                        "structure": structure,
                        "parameters": parameters,
                        "structure group": s_group,
                    }

                    # Create job for each adsorbate reference
                    for adsorbate in self.adsorbates[s_group]:
                        ads_calc_params = self.calc_params[s_group][
                            "adsorbate"
                        ]
                        ads_subm_params = self.subm_params_for(
                            adsorbate, ads_calc_params
                        )
                        ads_parameters = {
                            "calculation parameters": ads_calc_params,
                            "submission parameters": ads_subm_params,
                        }
                        ads_job = {
                            "structure": adsorbate,
                            "parameters": ads_parameters,
                            "structure group": s_group,
                        }

                        # Create job for catalyst-adsorbate complex
                        structure_complexes = self.complexes[s_group][
                            structure
                        ]
                        complex_structure = structure_complexes[adsorbate]
                        complex_subm_params = self.subm_params_for(
                            complex_structure, calc_params
                        )
                        complex_parameters = {
                            "calculation parameters": calc_params,
                            "submission parameters": complex_subm_params,
                        }
                        complex_job = {
                            "structure": complex_structure,
                            "parameters": complex_parameters,
                            "structure group": s_group,
                        }

                        # Add jobs to adsorption group
                        if s_group in adsorption_groups:
                            adsorption_groups[s_group].append(
                                {
                                    "catalyst reference": new_job,
                                    "adsorbate reference": ads_job,
                                    "catalyst-adsorbate complex": complex_job,
                                }
                            )
                        else:
                            adsorption_groups[s_group] = [
                                {
                                    "catalyst reference": new_job,
                                    "adsorbate reference": ads_job,
                                    "catalyst-adsorbate complex": complex_job,
                                }
                            ]

        return adsorption_groups

    # TODO: Change all "groups" to be attributes of main GUI
    @property
    def submission_parameter_groups(
        self,
    ) -> dict[str, groups.SubmissionParameterGroup]:
        """A mapping from names to submission parameter groups."""
        return self.app.tabs[
            "Submission Configuration"
        ].button_frame.submission_parameter_groups

    # TODO: modify to include adsorbates
    @property
    def calc_params(
        self,
    ) -> dict[str, groups.CalculationParameterGroup]:
        """A mapping from names to calculator parameter groups."""
        return self.app.tabs["Parameter Selection"].calc_params

    @property
    def subm_params(
        self,
    ) -> dict[str, dict[str, dict | float | int | tuple | str]]:
        """A mapping from names to submission parameter groups."""
        return self.app.tabs["Job Submission"].submission_parameters

    @property
    def structures(self) -> list[str]:
        """A list of structure file names."""
        return self.app.tabs[
            "Structure Selection"
        ].panel.structure_selection_frame.structures

    @property
    def structures_without_calc_params(self) -> list[str]:
        """A list of structure file names without calculation parameters."""
        no_calc_param_structures: list[str] = []

        for structure in self.structures:
            structure_groups = self.structure_groups_with([structure])
            if not structure_groups:
                no_calc_param_structures.append(structure)

        return no_calc_param_structures

    @property
    def structures_without_subm_params(self) -> list[dict]:
        """A list of structure file names without submission parameters."""
        structures_without_subm_params: list[dict] = []

        for s_group, structure_groups in self.structure_groups.items():
            for structure in structure_groups.structures:
                for calculation_parameters in product(
                    self.calc_params[s_group].values.values()
                ):
                    calc_params = dict(
                        zip(
                            self.calc_params[s_group].keys(),
                            calculation_parameters,
                            strict=True,
                        )
                    )
                    subm_params = self.subm_params_for(structure, calc_params)
                    if not subm_params:
                        structures_without_subm_params.append(
                            {
                                "structure": structure,
                                "calculation parameters": calc_params,
                            }
                        )
        return structures_without_subm_params

    @property
    def studies(
        self,
    ) -> dict[
        str, list[dict[str, str | CalculatorType | dict[str, dict[str, Any]]]]
    ]:
        """A dictionary mapping study names to all jobs within that study."""
        studies: dict[
            str,
            list[dict[str, str | CalculatorType | dict[str, dict[str, Any]]]],
        ] = {}

        for new_job in self.jobs:
            s_group = new_job["structure group"]
            if s_group in studies:
                studies[s_group].append(new_job)
            else:
                studies[s_group] = [new_job]

        return studies

    @property
    def jobs(
        self,
    ) -> list[dict[str, str | CalculatorType | dict[str, dict[str, Any]]]]:
        """A list of jobs.

        Each job is represented as a mapping from parameters to their values.
        """
        match self.study_type:
            case classification.StudyType.ADSORPTION.value:
                return self.adsorption_jobs
            case classification.StudyType.MECHANISM.value:
                return []
            case classification.StudyType.SENSITIVITY.value:
                return self.sensitivity_jobs

    @property
    def sensitivity_jobs(
        self,
    ) -> list[dict[str, str | CalculatorType | dict[str, dict[str, Any]]]]:
        """A list of sensitivity jobs."""
        jobs: list[
            dict[str, str | CalculatorType | dict[str, dict[str, Any]]]
        ] = []

        for sg_name, structure_group in self.structure_groups.items():
            for structure in structure_group.structures:
                defined_calculation_parameters: list[
                    job.CalculationParameter
                ] = self.calc_params[sg_name].defined_calculation_parameters
                for parameter_values in product(
                    *self.calc_params[sg_name].defined_values
                ):
                    calc_params: dict[job.CalculationParameter, Any] = dict(
                        zip(
                            defined_calculation_parameters,
                            parameter_values,
                            strict=True,
                        )
                    )
                    subm_params = self.subm_params_for(structure, calc_params)

                    if subm_params:
                        parameters = {
                            "calculation parameters": calc_params,
                            "submission parameters": subm_params,
                        }
                        new_job = {
                            "structure": str(structure),
                            "parameters": parameters,
                            "structure group": sg_name,
                            "calculator type": self.calculator_type,
                        }
                        jobs.append(new_job)
        return jobs

    @property
    def adsorption_jobs(self) -> list[dict]:
        """A list of adsorption jobs."""
        jobs: list[dict] = []

        for _, a_groups in self.adsorption_groups.items():
            for a_group in a_groups:
                for structure in iter(a_group):
                    jobs.append(a_group[structure])

        return jobs

    @property
    def study_type(self) -> str:
        """The study type."""
        study_panel = self.app.tabs["Study Configuration"].study_panel
        var = study_panel.rb_var.get()
        study_type = list(study_panel.rbs)[var].value
        return study_type

    @property
    def calculation_type(self) -> str:
        """The calculation type."""
        calculation_panel = self.app.tabs[
            "Study Configuration"
        ].calculation_panel
        var = calculation_panel.rb_var.get()
        calculation_type = list(calculation_panel.rbs)[var].value
        return calculation_type

    @property
    def calculator_type(self) -> str:
        """The calculator type."""
        calculator_panel = self.app.tabs[
            "Study Configuration"
        ].calculator_panel
        var = calculator_panel.rb_var.get()
        calculator_type = list(calculator_panel.rbs)[var].value
        return calculator_type

    def calc_param_from(
        self, param_name: str, cp_groups: list[str] | None = None
    ) -> "job.CalculationParameter":
        """Returns the parameter associated with the name and structure group.

        Args:
            param_name: Name of the :class:`.jobCalculationParameter` to be found.
            cp_groups: A list of names of structure groups to search. Defaults to a
                list of all structure groups.

        Returns:
            The :class:`.job.CalculationParameter` matching ``param_name``.
            If ``cp_groups`` is given, this method finds the first
            :class:`.job.CalculationParameter` defined in a structure
            group named ``cp_groups`` with the name attribute matching
            ``param_name``. Otherwise, this method finds the first
            :class:`.job.CalculationParameter` with name attribute matching
            ``param_name``.

        Raises:
            ValueError: No :class:`.job.CalculationParameter` found matching
                ``param_name``.
        """
        cp_groups = cp_groups or self.app.tabs["Parameter Selection"].params

        for cp_group in self.calc_params.values():
            for param in cp_group.values:
                if param.name == param_name:
                    return param

        group_str = ", ".join(cp_groups)

        err_str = (
            f"No CalculationParameter found matching {param_name} "
            f" in structure groups: {group_str}."
        )

        raise ValueError(err_str)

    def calc_params_for(self, structures: list[Path]) -> list[str]:
        """Finds calculation parameters corresponding to provided structures.

        Args:
            structures: A list of structures whose parameters are to be found.

        Returns:
            The names of all CalculationParameters applicable to at least one
            structure in ``structures``.
        """
        params = set()

        groups_with_structures = self.structure_groups_with(structures)

        for group in groups_with_structures:
            params.update([x.name for x in self.calc_params[group].values])

        return validation.alphanum_sort(params)

    def calc_param_values_for(
        self,
        structures: list[Path],
        params: list["job.CalculationParameter"],
    ) -> dict[str, list[float | int | str]]:
        """Finds values corresponding to provided structures and parameters.

        Args:
            structures: Structure for which the calculation parameters are to
                obtained.
            params: Parameter whose values are to be obtained.

        Returns:
            A dictionary mapping calculator parameter names to a list of its
            values for provided structures. Each value in each list of values
            corresponds to at least one structure in ``structures``.

        Note:
            Not all values will be applicable for all selected structures
            as the function aggregates all potential values for all selected
            structures.
        """
        values: list[str] = []

        groups_with_structures = self.structure_groups_with(structures)

        param_values: dict[str, list[str]] = {}

        for param in params:
            values = set()
            for group in groups_with_structures:
                try:
                    values = values.union(
                        self.calc_params[group].values[param]
                    )
                except KeyError:
                    if group in self.calc_params:
                        print("Parameter not applicable to group.")
                    else:
                        raise

                    continue

            values = [str(x) for x in values]
            values = validation.alphanum_sort(values)
            values = validation.iter_to_native(values)

            param_values[param.name] = values

        return param_values

    def subm_params_for(
        self,
        structure: Path,
        calc_params: dict["job.CalculationParameter", str],
    ) -> dict[str, dict | int | list | None]:
        """Finds submission parameters for a given structure and parameters.

        Args:
            structure: The structure for the calculation.
            calc_params: The structure-specific parameters for the
                calculation.

        Returns:
            The submission parameters for the calculation.

        Note:
            If the calculation satisfies the conditions set forth by multiple
            parameter groups, the function returns the submission parameters
            corresponding to the alphanumeric first.
        """
        # Parameter groups applicable to 'structure' with given calculation
        # parameters
        sp_groups_for_structure: list[str] = []
        for (
            sp_group_name,
            sp_group,
        ) in self.submission_parameter_groups.items():
            if structure in sp_group.values:
                in_parameter_group = True
                # The parameter which defines the parameter group that are
                # applicable to 'structure'
                p_group_params: dict[
                    job.CalculationParameter,
                    list[str],  # parameter names  # parameter values
                ] = self.submission_parameter_groups[sp_group_name].values[
                    structure
                ]
                for calc_param, values in p_group_params.items():
                    if calc_params[calc_param] in values:
                        continue

                    if calc_param in calc_params and len(values) == 0:
                        continue

                    in_parameter_group = False
                    break

                if in_parameter_group:
                    sp_groups_for_structure.append(sp_group_name)

        sp_groups_for_structure.sort()

        if sp_groups_for_structure:
            return self.subm_params[sp_groups_for_structure[0]]

        return {}

    def structure_groups_with(self, structures: Iterable[Path]) -> list[str]:
        """Retrieve all structure groups containing structures.

        Args:
            structures: A list of structures to be found in
                :attr:`Coordinator.structure_groups`.

        Returns:
            The list of structure groups containing at least one of the
            selected structures.
        """
        groups_with_structures: list[str] = []

        for group in self.structure_groups:
            group_structures = set(self.structure_groups[group].structures)
            if group_structures.intersection(structures):
                groups_with_structures.append(group)

        groups_with_structures = validation.alphanum_sort(
            groups_with_structures
        )

        return groups_with_structures

    # TODO: Replace create_* methods with
    # TODO: StudyGroup/Study/Calculation.to_directory()
    def create_directories(self) -> Path:
        """Creates study group directory tree.

        Returns:
            A Path representing the study group directory
        """
        study_group_id = "g" + shortuuid.uuid()[:9]
        study_group_dir = self.submit_dir.joinpath(study_group_id)
        study_group_dir.mkdir()

        metadata = {
            "Name": "",
            "Notes": "",
            "Date Created": str(datetime.datetime.now(tz=datetime.UTC)),
            "Study Group ID": study_group_id,
            "Studies": [],
        }

        for s_group in iter(self.studies):
            study_id = self.create_study_directory(
                study_group_id, study_group_dir, s_group
            )
            metadata["Studies"].append(study_id)

        filename = study_group_dir.joinpath(SETTINGS.STUDY_GROUP_FILE)

        with filename.open(mode="x", encoding="utf-8") as file:
            json.dump(metadata, file, sort_keys=False, indent=4)
        click.echo(f"Study group created: {study_group_dir.name}")
        return study_group_dir

    def create_study_directory(
        self, study_group_id: str, study_group_dir: Path, s_group: str
    ) -> str:
        """Creates study directory tree.

        Returns:
            A Path representing the study directory
        """
        study_id = "s" + shortuuid.uuid()[:9]
        study_dir = study_group_dir.joinpath(study_id)
        study_dir.mkdir()

        study_details = {
            "Name": s_group,
            "Notes": "",
            "Date Created": str(datetime.datetime.now(tz=datetime.UTC)),
            "Study Group ID": study_group_id,
            "Study ID": study_id,
            "Study Type": self.study_type,
            "Calculations": [],
        }

        match self.study_type:
            case classification.StudyType.ADSORPTION.value:
                study_details["Adsorption Groups"] = []

                for a_group in self.adsorption_groups[s_group]:
                    calc_ids: dict[str, str] = {}
                    for structure in iter(a_group):
                        calc = a_group[structure]
                        calc_id = self.create_calculation_directory(
                            study_group_id, study_id, study_dir, calc
                        )
                        calc_ids[structure] = calc_id

                    study_details["Adsorption Groups"].append(calc_ids)
            case classification.StudyType.MECHANISM.value:
                # List[Dict[str, bool]] (str = calc ID, bool = is desorbed?)
                study_details["Step Intermediates"] = []
            case classification.StudyType.SENSITIVITY.value:
                for calc in self.studies[s_group]:
                    calc_id = self.create_calculation_directory(
                        study_group_id, study_id, study_dir, calc
                    )
                    study_details["Calculations"].append(calc_id)

        file_text = json.dumps(study_details, sort_keys=False, indent=4)

        filename = study_dir.joinpath(SETTINGS.STUDY_FILE)

        with filename.open(mode="x", encoding="utf-8") as file:
            file.write(file_text)

        return study_id

    def create_calculation_directory(
        self,
        study_group_id: str,
        study_id: str,
        study_dir: Path,
        calc: dict[str, str | CalculatorType | dict[str, dict[str, Any]]],
    ) -> str:
        """Creates calculation directory tree.

        Returns:
            A Path representing the calculation directory
        """
        calc_id = "c" + shortuuid.uuid()[:9]
        calc_dir = study_dir.joinpath(calc_id)
        calc_dir.mkdir()
        calc_details = {
            "Name": "",
            "Notes": "",
            "Date Created": str(datetime.datetime.now(tz=datetime.UTC)),
            "Study Group ID": study_group_id,
            "Study ID": study_id,
            "Study Type": self.study_type,
            "Calculation ID": calc_id,
            "Calculation Type": self.calculation_type,
            "Jobs": [],
        }

        job_id = self.create_job_directory(
            study_group_id, study_id, calc_id, calc_dir, calc
        )
        calc_details["Jobs"].append(job_id)

        file_text = json.dumps(calc_details, sort_keys=False, indent=4)

        filename = calc_dir.joinpath(SETTINGS.CALCULATION_FILE)

        with filename.open(mode="x", encoding="utf-8") as file:
            file.write(file_text)

        return calc_id

    def create_job_directory(
        self,
        study_group_id: str,
        study_id: str,
        calc_id: str,
        calc_dir: Path,
        calc: dict[str, str | CalculatorType | dict[str, dict[str, Any]]],
    ) -> str:
        """Creates job directories and input files for jobs.

        Args:
            study_group_id: The study group ID of the job.
            study_id: The study ID of the job.
            calc_id: The calculation ID of the job.
            calc_dir: The calculation root directory of the job.
            calc: A dictionary mapping parameter names to their values. The
                following keys are guaranteed.
                    - "calculator type": A CalculatorType.
                    - "structure": The structure used in the job
                    - "parameters": A dictionary containing calculation (key:
                        "calculation parameters") and submission parameters
                        (key: "submission parameters")

        Returns:
            A string representing the job ID.
        """
        job_id = "j" + shortuuid.uuid()[:9]
        job_dir = calc_dir.joinpath(job_id)
        job_dir.mkdir()

        # TODO: Calculator Type, etc. should not be set two different ways
        # e.g.,: via `calc` and self.
        job_details = {
            "Name": "",
            "Notes": "",
            "Study Group ID": study_group_id,
            "Study ID": study_id,
            "Study Type": self.study_type,
            "Calculation ID": calc_id,
            "Calculation Type": self.calculation_type,
            "Calculator Type": self.calculator_type,
            "Job ID": job_id,
        }

        file_text = json.dumps(job_details, sort_keys=False, indent=4)

        filename = job_dir.joinpath(SETTINGS.JOB_FILE)

        with filename.open(mode="x", encoding="utf-8") as file:
            file.write(file_text)

        shutil.copy(calc["structure"], job_dir)

        calculation_parameters = calc["parameters"]["calculation parameters"]
        calculator = str(calc["calculator type"])
        structure = Path(calc["structure"]).name
        scripter.Scripter.create_python_script(
            parameters=calculation_parameters,
            calculator=calculator,
            structure=structure,
            job_dir=job_dir,
        )
        structure_name = structure.rstrip(".traj").split("/")[-1]
        submission_parameters = calc["parameters"]["submission parameters"]
        restart_limit = submission_parameters["restart limit"]
        submission_parameters["auto_restart"] = (
            restart_limit is None or restart_limit > 0
        )
        submission_parameters["files_to_delete"] = FILES_TO_DELETE
        submission_parameters["files_to_copy"] = FILES_TO_COPY
        slurm_script = scripter.Scripter.create_slurm_script(
            calculator=calculator,
            submission_parameters=submission_parameters,
            job_dir=job_dir,
            compute_canada_format=self.compute_canada_format,
            structure=structure_name,
        )

        self.slurm_scripts.append(slurm_script)

        return job_id

    def run_jobs(self) -> None:
        """Create and submit jobs of a new study group."""
        self.create_directories()
        for script in self.slurm_scripts:
            try:
                submit_new_task(script.parent)
            except subprocess.CalledProcessError as err:
                logger.warning(
                    f"Unable to submit job in {script.parent} due to: "
                    f"{err.args[0]}"
                )
