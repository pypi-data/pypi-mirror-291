"""This module defines the GUI logic for study configuration.

Specifically, the module provides the :class:`StudyConfigurationTab` which is
the parent :class:`~ttk.Frame` for study configuration and the
:class:`StudyPanel`, :class:`CalculationPanel`, and :class:`CalculatorPanel`
classes which permit selection of study, calculation, and calculator types,
respectively.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from autojob.coordinator import classification
from autojob.coordinator.gui import widgets

if TYPE_CHECKING:
    from autojob.coordinator.gui import gui


class StudyPanel(widgets.RadiobuttonPanel):
    """A :class:`~widgets.RadiobuttonPanel` for selecting study type."""

    def __init__(self, parent: ttk.Frame, columns: int) -> None:
        """Initialize a `StudyPanel`.

        Args:
            parent: The :class:`tkinter.ttk.Frame` in which the `StudyPanel` will
                reside.
            columns: The number of columns to use to display study types.
        """
        super().__init__(
            parent, "Select Study Type", classification.StudyType, columns
        )


class CalculationPanel(widgets.RadiobuttonPanel):
    """A :class:`~widgets.RadiobuttonPanel` for selecting calculation type."""

    def __init__(self, parent: ttk.Frame, columns: int) -> None:
        """Initialize a `CalculationPanel`.

        Args:
            parent: The :class:`tkinter.ttk.Frame` in which the
                `CalculationPanel` will reside.
            columns: The number of columns to use to display study types.
        """
        super().__init__(
            parent,
            "Select Calculation Type",
            classification.CalculationType,
            columns,
        )


class CalculatorPanel(widgets.RadiobuttonPanel):
    """A :class:`~widgets.RadiobuttonPanel` for selecting calculator type."""

    def __init__(self, parent: ttk.Frame, columns: int) -> None:
        """Initialize a `CalculatorPanel`.

        Args:
            parent: The :class:`tkinter.ttk.Frame` in which the
                `CalculatorPanel` will reside.
            columns: The number of columns to use to display study types.
        """
        super().__init__(
            parent,
            "Select Calculator Type",
            # TODO: replace with parameters.CalculatorType
            classification.CalculatorType,
            columns,
        )


class StudyConfigurationTab(ttk.Frame):
    """A :class:`tkinter.ttk.Frame` from configuring studies.

    Attributes:
        parent: A `ttk.Notebook` in which the `StudyConfigurationTab` will
            reside.
        app: The :class:`~gui.GUI` instance for the GUI application.
        study_panel: The :class:`~widgets.RadiobuttonPanel` for selecting
            the study type to use for the study group.
        calculation_panel: The :class:`~widgets.RadiobuttonPanel` for selecting
            the calculation type to use for the study group.
        calculator_panel: The :class:`~widgets.RadiobuttonPanel` for selecting
            the calculator to use for the study group.
    """

    def __init__(self, main_app: "gui.GUI") -> None:
        """Initialize a `StudyConfigurationTab`.

        Args:
            main_app: The :class:`~gui.GUI` instance for the GUI application.
        """
        super().__init__(main_app.notebook)
        self.parent = main_app.notebook
        self.app: gui.GUI = main_app

        # Create panels
        self.study_panel = StudyPanel(self, 3)  # TODO: set '3' dynamically
        self.calculation_panel = CalculationPanel(self, 3)
        self.calculator_panel = CalculatorPanel(self, 5)

        # Configure panels
        self.study_panel.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)
        self.calculation_panel.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)
        self.calculator_panel.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)

    def load(self) -> None:
        """Do nothing."""
