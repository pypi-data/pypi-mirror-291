"""This module defines the logic for the main Coordinator GUI.

Importantly, this module defines the :class:`~gui.GUI` class
and :func:`~gui.run` function used to execute the Coordinator GUI.

Example::

    >>> from autojob.coordinator.gui import gui
    >>> gui.run()
"""

import pathlib
import tkinter as tk
from tkinter import ttk

from autojob.coordinator import coordinator
from autojob.coordinator.gui import job_submission as js
from autojob.coordinator.gui import parameter_selection as ps
from autojob.coordinator.gui import structure_selection as ss
from autojob.coordinator.gui import study_configuration as sc
from autojob.coordinator.gui import submission_configuration as sbc
from autojob.coordinator.gui import summary as sm


class GUI:
    """The main GUI for `autojob.coordinator`.

    Attributes:
        parent: The top level widget for the GUI application.
        coordinator: The :class:`~Coordinator` responsible for managing
            study group creation.
        template: A string representing the path to the template of a
            previously created coordinator study group. Defaults to None.
        notebook: A :class:`ttk.Notebook` used to host the configuration tabs.
        tabs: The tabs of the notebook.
    """

    def __init__(
        self,
        top_level: tk.Tk,
        template: str | None,
        dest: pathlib.Path | None = None,
    ) -> None:
        """Initialize the `coordinator` GUI.

        Args:
            top_level: The top-level :class:`tkinter.Tk` instance.
            template: The filename of a template with which to pre-populate
                the GUI.
            dest: The root directory for study group creation. Defaults to the
                current working directory.
        """
        self.parent: tk.Tk = top_level
        self.coordinator: coordinator.Coordinator = coordinator.Coordinator(
            self, dest=dest or pathlib.Path.cwd()
        )

        self.template = template
        self.notebook: ttk.Notebook = ttk.Notebook(self.parent)

        self.tabs: dict[
            str,
            sc.StudyConfigurationTab
            | ss.StructureSelectionTab
            | ps.ParameterSelectionTab
            | sbc.SubmissionConfigurationTab
            | js.JobSubmissionTab
            | sm.SummaryTab,
        ] = {}

        self.create_tabs()
        self.organize()
        self.add_tabs_to_notebook()

        self.notebook.bind("<<NotebookTabChanged>>", self.load)
        self.notebook.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def create_tabs(self) -> None:
        """Create :class:`ttk.Frame`s for each configuration tab."""
        self.tabs["Study Configuration"] = sc.StudyConfigurationTab(self)
        self.tabs["Structure Selection"] = ss.StructureSelectionTab(self)
        self.tabs["Parameter Selection"] = ps.ParameterSelectionTab(self)
        self.tabs["Submission Configuration"] = sbc.SubmissionConfigurationTab(
            self
        )
        self.tabs["Job Submission"] = js.JobSubmissionTab(self)
        self.tabs["Summary"] = sm.SummaryTab(self)

    def organize(self) -> None:
        """Organize each configuration tab."""
        for tab in iter(self.tabs.values()):
            tab.pack(fill="both", expand=True)

    def add_tabs_to_notebook(self) -> None:
        """Add each configuration tab to the notebook."""
        for title, tab in self.tabs.items():
            self.notebook.add(tab, text=title)

    def load(self, event: tk.Event) -> None:
        """Load each tab in the GUI.

        Args:
            event: The event triggering the GUI to load.
        """
        if not event:
            pass

        for tab in iter(self.tabs.values()):
            tab.load()


def configure_root(root: tk.Tk) -> None:
    """Configure the root window.

    Args:
        root: The top-level :class:`tkinter.Tk` instance.
    """
    root.title("Create Study/Study Group")
    root.attributes("-fullscreen", True)


def run(
    template: pathlib.Path | None = None, dest: pathlib.Path | None = None
) -> None:
    """Run the main coordinator GUI.

    Args:
        template: The template file from which to recreate the study group.
            Defaults to None.
        dest: The root directory for study group creation.
    """
    root = tk.Tk()
    configure_root(root)
    GUI(root, template, dest=dest)

    root.mainloop()
