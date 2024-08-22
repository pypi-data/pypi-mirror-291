"""GUI elements for displaying study group summaries."""

import tkinter as tk
from tkinter import ttk
from typing import TypedDict

from autojob.coordinator import job
from autojob.coordinator.gui import gui
from autojob.coordinator.gui import widgets


class SummaryFrame(ttk.LabelFrame):
    """A `Frame` summarizing to-be-created jobs.

    Attributes:
        parent: The :class:`SummaryTab` in which the `SummaryFrame` resides.
        study_configuration_tab: The :class:`StudyConfigurationTab`.
        label: The :class:`tkinter.ttk.Label` for `Frame`.
    """

    def __init__(
        self, parent: "SummaryTab", app: "gui.GUI", title: str
    ) -> None:
        """Initialize a `SummaryFrame`.

        Args:
            parent: The :class:`SummaryTab` in which the `SummaryFrame` resides.
            app: The running :class:`.gui.GUI`.
            title: The title for the `SummaryFrame`.
        """
        super().__init__(parent, text=title.capitalize() + " Type")
        self.parent: SummaryTab = parent

        self.study_configuration_tab = app.tabs["Study Configuration"]
        self.label = ttk.Label(self)

        self.load()

        self.organize()

    def load(self) -> None:
        """Load the text for the label."""
        if "study" in self["text"].lower():
            panel = self.study_configuration_tab.study_panel
        elif "calculation" in self["text"].lower():
            panel = self.study_configuration_tab.calculation_panel
        elif "calculator" in self["text"].lower():
            panel = self.study_configuration_tab.calculator_panel

        index = panel.rb_var.get()
        keys = list(panel.rbs)
        study_type = keys[index]
        rad_button = panel.rbs[study_type]
        text = rad_button["text"]

        self.label.configure(text=text)

    def organize(self) -> None:
        """Pack the label."""
        self.label.pack()


class StudySummaryFrame(SummaryFrame):
    """Summarize the study type."""

    def __init__(self, parent: ttk.Frame, app: "gui.GUI") -> None:
        """Initialize a `StudySummaryFrame`.

        Args:
            parent: The :class:`SummaryTab` in which the
                `StudySummaryFrame` resides.
            app: The running :class:`.gui.GUI`.
        """
        super().__init__(parent, app, "Study")


class CalculationSummaryFrame(SummaryFrame):
    """Summarize the calculation type."""

    def __init__(self, parent: ttk.Frame, app: "gui.GUI") -> None:
        """Initialize a `CalculationSummaryFrame`.

        Args:
            parent: The :class:`SummaryTab` in which the
                `CalculationSummaryFrame` resides.
            app: The running :class:`.gui.GUI`.
        """
        super().__init__(parent, app, "Calculation")


class CalculatorSummaryFrame(SummaryFrame):
    """Summarize the calculator type."""

    def __init__(self, parent: ttk.Frame, app: "gui.GUI") -> None:
        """Initialize a `CalculatorSummaryFrame`.

        Args:
            parent: The :class:`SummaryTab` in which the
                `CalculatorSummaryFrame` resides.
            app: The running :class:`.gui.GUI`.
        """
        super().__init__(parent, app, "Calculator")


class JobSummaryFrame(ttk.LabelFrame):
    """Summarize the jobs to be created.

    Attributes:
        parent: The :class:`SummaryTab` in which the `JobSummaryFrame`
            resides.
        tbf: A :class:`.widgets.TreeviewFrame` describing the to-be-created
            jobs.
        jobs: A dictionary mapping structures to calculation and submission
            parameter dictionaries. Each nested dictionary maps parameters
            to lists of values.
    """

    def __init__(self, parent: "SummaryTab") -> None:
        """Initialize a `JobSummaryFrame`.

        Args:
            parent: The :class:`SummaryTab` in which the `JobSummaryFrame`
            resides.
        """
        super().__init__(parent, text="All Jobs")

        self.parent: SummaryTab = parent
        self.tbf = widgets.TreeviewFrame(self)
        self.tbf.treeview.configure(
            columns=("Structure"), displaycolumns=(0), height=15
        )
        self.tbf.treeview.column("#0", anchor=tk.CENTER, width=300)
        self.tbf.treeview.column("Structure", width=1200)
        self.tbf.treeview.heading("#0", text="Job Number")
        self.tbf.treeview.heading("Structure", text="Structure Path")
        self.tbf.treeview.configure(show=("tree", "headings"))
        self.jobs: dict[
            str,  # structures
            dict[
                str,  # type of parameter (calculation or submission)
                dict,  # parameter values
            ],
        ]
        self.tbf.pack(expand=True, fill=tk.BOTH, padx=10, pady=10, side=tk.TOP)

    def populate(self) -> None:
        """Populate the `Treeview` with calculation and submission parameter values."""
        jobs: list[dict[str, dict]] = self.parent.app.coordinator.jobs

        i = 1

        for new_job in jobs:
            structure = new_job["structure"]
            job_iid = self.tbf.treeview.insert(
                "", "end", text=str(i), values=(structure,)
            )

            calc_params = new_job["parameters"]["calculation parameters"]
            self.add_calc_params(calc_params, job_iid)

            subm_params = new_job["parameters"]["submission parameters"]
            self.add_subm_params(subm_params, job_iid)

            i += 1

    def add_calc_params(
        self, calc_params: dict[job.CalculationParameter, str], job_iid: str
    ) -> None:
        """Add the calculation parameter values to the `Treeview`."""
        title = "Calculation Parameters"
        parent_iid = self.tbf.treeview.insert(job_iid, "end", text=title)

        for parameter, value in calc_params.items():
            param_iid = self.tbf.treeview.insert(
                parent_iid, "end", text=str(parameter)
            )

            self.tbf.treeview.insert(param_iid, "end", text=str(value))

    def add_subm_params(self, subm_params: dict, job_iid: str) -> None:
        """Add the submission parameter values to the `Treeview`."""
        title = "Submission Parameters"
        parent_iid = self.tbf.treeview.insert(job_iid, "end", text=title)

        for parameter, value in subm_params.items():
            param_iid = self.tbf.treeview.insert(
                parent_iid, "end", text=parameter
            )
            if parameter == "run time":
                days = value["days"]
                days_plural = "" if days == 1 else "s"
                days_str = f"{days} day{days_plural}"

                hrs = value["hours"]
                hrs_plural = "" if hrs == 1 else "s"
                hrs_str = f"{hrs} hour{hrs_plural}"

                mins = value["minutes"]
                mins_plural = "" if mins == 1 else "s"
                mins_str = f"{mins} minute{mins_plural}"

                text = f"{days_str} {hrs_str} {mins_str}"

                self.tbf.treeview.insert(param_iid, "end", text=text)
            elif parameter == "memory":
                text = f"{value[0]} {value[1]}"
                self.tbf.treeview.insert(param_iid, "end", text=text)
            elif parameter == "partitions":
                for partition in value:
                    self.tbf.treeview.insert(param_iid, "end", text=partition)
            else:
                self.tbf.treeview.insert(param_iid, "end", text=str(value))

    def load(self) -> None:
        """Reload the displayed jobs in the `Treeview`."""
        self.tbf.clear_treeview()
        self.populate()


class WarningsFrame(ttk.LabelFrame):
    """View automatically generated warnings.

    Attributes:
        warnings: A list of :class:`tkinter.ttk.Label`s containing
            warnings.
    """

    def __init__(self, parent: "SummaryTab") -> None:
        """Initialize a `WarningsFrame`.

        Args:
            parent: The :class:`SummaryTab` in which the `JobSummaryFrame`
                resides.
        """
        super().__init__(parent, text="Warnings")
        self.warnings: list[ttk.Label] = []

    def new_structure_warning(self) -> None:
        """Create a structure warning."""

    def new_parameter_warning(self) -> None:
        """Create a parameter warning."""

    def load(self) -> None:
        """Reload the displayed warnings."""
        if not self.warnings:
            label = ttk.Label(self, text="None")
            self.warnings = [label]

        for warning in self.warnings:
            warning.grid(padx=10, pady=10, sticky=tk.W)


class CreateJobsFrame(ttk.LabelFrame):
    """Frame containing job creation button and compute canada format prompt.

    Attributes:
        parent: The :class:`SummaryTab` in which the frame resides.
        var: An `IntVar` indicating whether the user has opted for the jobs to
            be created in compute canada format.
        checkb: A `Checkbutton` to select the job format.
        button: A `Button` to initiate job creation.
    """

    def __init__(self, parent: "SummaryTab") -> None:
        """Initialize a `CreateJobsFrame`.

        Args:
            parent: The :class:`SummaryTab` in which the frame resides.
        """
        super().__init__(parent, text="Finalize")
        self.parent = parent
        self.var = tk.IntVar()
        self.checkb = ttk.Checkbutton(
            self, text="Compute Canada Format?", variable=self.var
        )

        def complete() -> None:
            """Create jobs."""
            self.parent.app.coordinator.compute_canada_format = (
                self.var.get() != 0
            )
            _ = self.parent.app.coordinator.create_directories()

        self.button = ttk.Button(self, command=complete, text="Complete")

        self.checkb.grid(column=0, padx=25, pady=10, row=0)
        self.button.grid(column=1, padx=25, pady=10, row=0)

    def load(self) -> None:
        """Do nothing."""


class SummaryFrames(TypedDict):
    """The subframes of a `SummaryTab`."""

    study_summary: StudySummaryFrame
    calculation_summary: CalculationSummaryFrame
    calculator_summary: CalculatorSummaryFrame
    job_summary: JobSummaryFrame
    warnings: WarningsFrame
    completion: CreateJobsFrame


class SummaryTab(ttk.Frame):
    """A GUI element summarizing study group parameters.

    Attributes:
        parent: The :class:`tkinter.ttk.Notebook` in which the `SummaryTab`
            resides.
        app: The running :class:`.gui.GUI`
        container: The container frame for placing subframes.
        summaries: A :class:`SummaryFrames` typed dictionary containing the
            subframes of the `SummaryTab`.
    """

    def __init__(self, main_app: "gui.GUI") -> None:
        """Initialize a `SummaryTab`.

        Args:
            main_app: _description_
        """
        super().__init__(main_app.notebook)
        self.parent: ttk.Notebook = main_app.notebook
        self.app: gui.GUI = main_app

        self.container = ttk.Frame(self)

        self.summaries: SummaryFrames = self.create()

        self.organize()

    def create(self) -> SummaryFrames:
        """Creates the subframes of the `SummaryTab`."""
        summaries: SummaryFrames = {}

        summaries["study_summary"] = StudySummaryFrame(
            self.container, self.app
        )
        summaries["calculation_summary"] = CalculationSummaryFrame(
            self.container, self.app
        )
        summaries["calculator_summary"] = CalculatorSummaryFrame(
            self.container, self.app
        )
        summaries["job_summary"] = JobSummaryFrame(self)

        summaries["warnings"] = WarningsFrame(self)

        summaries["completion"] = CreateJobsFrame(self)

        return summaries

    def organize(self) -> None:
        """Pack frames."""
        self.container.pack(fill=tk.BOTH, side=tk.TOP)

        self.summaries["study_summary"].grid(
            column=0, ipadx=10, padx=50, pady=50, row=0
        )
        self.summaries["calculation_summary"].grid(
            column=1, ipadx=10, padx=50, pady=50, row=0
        )
        self.summaries["calculator_summary"].grid(
            column=2, ipadx=10, padx=50, pady=50, row=0
        )

        self.summaries["job_summary"].pack(fill=tk.BOTH, side=tk.TOP)

        (cols, _) = self.container.grid_size()
        for col in range(cols):
            self.container.columnconfigure(col, weight=1)

        self.summaries["warnings"].pack(pady=5, side=tk.TOP)
        self.summaries["completion"].pack(pady=5, side=tk.TOP)

    def load(self) -> None:
        """Load frames."""
        for key in list(self.summaries):
            self.summaries[key].load()
