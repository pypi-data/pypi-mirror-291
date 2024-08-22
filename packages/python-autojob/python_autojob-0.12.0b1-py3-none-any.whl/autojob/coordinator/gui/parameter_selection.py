"""Specify calculator parameters."""

import importlib
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from typing import TypeVar

import numpy as np

from autojob.coordinator import job
from autojob.coordinator import validation
from autojob.coordinator.gui import groups
from autojob.coordinator.gui import widgets

if TYPE_CHECKING:
    from autojob.coordinator.gui import gui


class GroupSelectionCombobox(ttk.Combobox):
    """Select a CalculatorParameterGroup.

    Attributes:
        parent: The `ParameterSelectionTab` in which the `GroupSelectionCombobox` is embedded.
        var: A :class:`tkinter.StringVar` storing the name of the active CalculatorParameterGroup.

    Note:
        The `.load()` function of the parent frame is called during the validation
        function for the combobox.
    """

    def __init__(self, parent: "ParameterSelectionTab"):
        """Initialize a `GroupSelectionCombobox`.

        Args:
            parent: The parent `ParameterSelectionTab` in which the combobox
                resides.
        """
        var = tk.StringVar()
        values = list(parent._calc_params)

        super().__init__(
            parent,
            state="readonly",
            textvariable=var,
            validate="focus",
            values=values,
        )

        def display_structure_calc_params(reason: str) -> bool:
            if reason != "forced":
                self.parent.load()

            return True

        cmd = self.register(display_structure_calc_params)

        self.configure(validatecommand=(cmd, "%V"))

        self.parent: ParameterSelectionTab = parent

        self.var = var

    def load(self) -> None:
        """Populate the list of calculator parameters to display."""
        self["values"] = list(self.parent.calc_params)

        if self["values"]:
            if self.current() == -1:
                self.current(0)
        else:
            self.set("")


class ParameterRadiobuttonFrame(ttk.LabelFrame):
    """Select the parameter entry method.

    Attributes:
        parent: The `ParameterSelectionTab` in which the
            `ParameterRadiobuttonFrame` is embedded.
        rb_var:
        rbs:
        str_vars:
    """

    def __init__(self, parent: "ParameterSelectionTab") -> None:
        """Initialize a `ParameterRadiobuttonFrame`.

        Args:
            parent: The `ParameterSelectionTab` in which the
                `ParameterRadiobuttonFrame` is embedded.
        """
        super().__init__(parent, text="Select parameter entry method")
        self.parent: ParameterPanel = parent

        self.rb_var, self.rbs, self.str_vars = self.create_radio_buttons()

        self.place_radio_buttons()

    def create_radio_buttons(
        self,
    ) -> tuple[tk.IntVar, list[ttk.Radiobutton], list[tk.StringVar]]:
        """Create the input method `Radiobutton`s.

        Returns:
            A 3-tuple (`rb_var`, `rbs`, `str_vars`) where `rb_var` is the
            :class:`tkinter.IntVar` indicating which input method `Radiobutton`
            is selected, `rbs` is a list of the input method `Radiobutton`s,
            and `str_vars` is a list of the :class:`tkinter.StringVar`s
            associated with the labels of each `Radiobutton`.
        """
        rb_var = tk.IntVar(value=-1)

        if self.parent.param.explicit_values:
            labels = ["from list"]
        elif len(self.parent.param.specials) == 0:
            labels = ["by typing", "as range"]
        else:
            labels = ["from list", "by typing", "as range"]

        rbs: list[ttk.Radiobutton] = []
        str_vars: list[tk.StringVar] = []

        for i, label in enumerate(labels):
            str_var = tk.StringVar(value=label)

            rb = ttk.Radiobutton(
                self, textvariable=str_var, value=i, variable=rb_var
            )

            rbs.append(rb)
            str_vars.append(str_var)

        return rb_var, rbs, str_vars

    def place_radio_buttons(self) -> None:
        """Grid the `Radiobutton`s."""
        for i, _ in enumerate(self.rbs):
            self.rbs[i].grid(column=i, padx=5, pady=2, row=0)


class ParameterInputFrame(ttk.Frame):
    """A frame containing the input widget for parameter specification.

    Attributes:
        parent: The `ParameterInputSection` in which the
            `ParameterInputFrame` is embedded.
        text: Descriptive text for the parameter.
        finite_int_range: Whether the `ParameterInputFrame` is used to
            specify the value restricted to a finite range of integers.
        label: The :class:`tkinter.ttk.Label` for the `ParameterInputFrame`.
        widg: The Tkinter widget used to input the value of the paramter.
        var: A :class:`tkinter.StringVar` storing the value of the parameter.
    """

    def __init__(self, parent: "ParameterInputSection", text: str) -> None:
        """Initialize a `ParameterInputFrame`.

        Args:
            parent: The `ParameterInputSection` in which the
            `ParameterInputFrame` is embedded.
            text: Descriptive text for the parameter.
        """
        super().__init__(parent)
        self.parent: ParameterInputSection = parent
        self.text = text or ""

        parameter: job.CalculationParameter = self.parent.parent.param
        self.finite_int_range = parameter.is_finite_int_range()

        self.label: ttk.Label = self.create_label()

        self.widg, self.var = self.create_widg()

        self.label.grid(column=0, padx=5, pady=5, row=0)
        self.widg.grid(column=1, padx=5, pady=5, row=0)

    def create_label(self) -> ttk.Label:
        """Create the label displaying the parameter help text."""
        if self.text:
            label = ttk.Label(self, text=f"{self.text}:")
        else:
            label = ttk.Label(self, text="")

        return label

    def create_widg(
        self,
    ) -> tuple[ttk.Combobox | ttk.Entry | tk.Spinbox, tk.StringVar]:
        """Create the widget used to input the parameter value."""
        if self.text == "select":
            return self.create_combobox()
        if (
            self.text in ["enter", "start", "stop", "# of steps"]
            and self.finite_int_range
        ):
            return self.create_spinbox()
        if (
            self.text in ["enter", "start", "stop", "# of steps"]
            and not self.finite_int_range
        ):
            return self.create_entry()
        if self.text == "":
            return ttk.Frame(self), tk.StringVar()

        msg = (
            f"Values of 'text' ({self.text}) "
            f"and 'finite_int_range' ({self.finite_int_range}) "
            "parameters passed to constructor unsupported."
        )
        raise ValueError(msg)

    def create_combobox(self) -> tuple[ttk.Combobox, tk.StringVar]:
        """Create a `Combobox` to select parameter values.

        Returns a 2-tuple (`cb`, `var`) where `cb` is the `Combobox`
        and `var` is the associated `StringVar`.
        """
        cb_var = tk.StringVar()

        if self.parent.parent.param.specials:
            values = self.parent.parent.param.specials
        else:
            values = self.parent.parent.param.values

        combo_box = ttk.Combobox(
            self,
            state="readonly",
            textvariable=cb_var,
            values=values,
            width=15,
        )

        return combo_box, cb_var

    def create_entry(self) -> tuple[ttk.Entry, tk.StringVar]:
        """Create an `Entry` for specifying parameter values.

        Returns a 2-tuple (`entry`, `var`) where `entry` is the
        `Entry` and `var` is the associated `StringVar`.
        """
        var = tk.StringVar()

        entry = ttk.Entry(self, textvariable=var, width=5)

        return entry, var

    def create_spinbox(self) -> tuple[tk.Spinbox, tk.StringVar]:
        """Create an `Spinbox` for specifying parameter values.

        Returns a 2-tuple (`sb`, `var`) where `sb` is the
        `Spinbox` and `var` is the associated `StringVar`.
        """
        var = tk.StringVar()

        spin_box = tk.Spinbox(
            self,
            from_=self.parent.parent.param.values[0],
            textvariable=var,
            to=self.parent.parent.param.values[1],
        )

        return spin_box, var


class ParameterInputSection(ttk.Frame):
    """A container frame for `ParameterInputFrame`s.

    Attributes:
        parent: The `ParameterPanel` in which the
            `ParameterInputSection` is embedded.
        input_frames: The `ParameterInputFrame`s for speciying
            parameter values.
    """

    def __init__(self, parent: "ParameterPanel") -> None:
        """Initialize a `ParameterInputSection`.

        Args:
            parent: The `ParameterPanel` in which the
            `ParameterInputSection` is embedded.
        """
        super().__init__(parent)
        self.parent: ParameterPanel = parent

        self.input_frames: list[ParameterInputFrame] = (
            self.create_input_frames()
        )

        self.place_input_sections()

    def frame_titles(self) -> list[str]:
        """Determine the frame titles based on the parameter type.

        Returns:
            A list of strings representing frame titles.

            "select": present unless the parameter has no special values and
                the only title present if the parameter is set by
                explicit values.

            Possibilities: "select" only, all but "select", all
        """
        titles = ["select", "enter", "start", "stop", "# of steps"]

        if self.parent.param.explicit_values:
            for i in range(1, 5):
                titles[i] = None
        elif not self.parent.param.specials:
            titles[0] = None

        return titles

    def create_input_frames(self) -> list[ParameterInputFrame]:
        """Create the input frames for specifying parameter values.

        The input frames created depends on the type of parameter.
        """
        entries = self.frame_titles()
        input_frames: list[ParameterInputFrame] = []

        for entry in entries:
            input_frames.append(ParameterInputFrame(self, entry))

        return input_frames

    def place_input_sections(self) -> None:
        """Place the created `ParameterInputSection`s."""
        for i, _ in enumerate(self.input_frames):
            self.input_frames[i].grid(
                column=0, padx=5, pady=5, row=i, sticky=tk.E
            )


class ParameterPanel(ttk.LabelFrame):
    """A Frame containing GUI elements for defining parameter values.

    Attributes:
        parent: The `ParameterSelectionTab` to which this panel belongs.
        param: The parameter whose parametrization is represented by the
            panel.
        rbf: The `ParameterRadiobuttonFrame` used select the input method.
        input_section: The `LabelFrame` used to enable entering paramtrization
            values.
        lbf: The :class:`~.widgets.ListboxFrame` used to display the parameter values.
        button_frame: The `Frame` in which the add/clear/delete buttons reside.
        default_button: The `Button` used to reset the parameter value to its
            default value.
        check_var: The variable storing the state of `default_button`.
    """

    def __init__(
        self, parent: "ParameterSelectionTab", param: job.CalculationParameter
    ) -> None:
        """Initialize a `ParameterPanel`.

        Args:
            parent: The `ParameterSelectionTab` in which the
            `ParameterInputSection` is embedded.
            param: The calculation parameter corresponding to the
                `ParameterPanel`.
        """
        title = f"{param.name}: {param.description}"
        super().__init__(parent, text=title, name=param.name.lower())

        self.parent: ParameterSelectionTab = parent
        self.param: job.CalculationParameter = param

        self.rbf: ParameterRadiobuttonFrame = ParameterRadiobuttonFrame(self)
        self.input_section: ParameterInputSection = ParameterInputSection(self)
        self.lbf: widgets.ListboxFrame = widgets.ListboxFrame(self)

        self.button_frame: ttk.Frame = self.create_button_frame()
        self.default_button, self.check_var = self.create_default_button()

        self.organize()

        self.configure_rbs()

        if self.param.default is not None:
            self.default_button.invoke()

    def create_button_frame(self) -> ttk.Frame:
        """Create the frame in which the add/clear/delete buttons reside."""
        background = ttk.Style().lookup("TFrame", "background")
        style: ttk.Style = ttk.Style()
        style.configure("button.TFrame", background=background)
        subframe = ttk.Frame(self, style="button.TFrame")

        add_button = ttk.Button(
            subframe, text="add", command=self.add_parameter_values, width=5
        )

        rm_button = ttk.Button(
            subframe,
            text="remove",
            command=self.remove_parameter_values,
            width=5,
        )

        clr_button = ttk.Button(
            subframe,
            text="clear",
            command=self.clear_parameter_values,
            width=5,
        )

        add_button.grid(column=0, padx=5, pady=10, row=0)
        rm_button.grid(column=0, padx=5, pady=10, row=1)
        clr_button.grid(column=0, padx=5, pady=10, row=2)

        subframe.rowconfigure(0, weight=1)
        subframe.rowconfigure(1, weight=1)
        subframe.rowconfigure(2, weight=1)

        return subframe

    def add_parameter_values(self) -> None:
        """Validates parameter values and adds new values.

        Duplicates are removed and the entries in the :class:`tkinter.Listbox`
        are sorted.
        """
        active_input_method = self.rbf.str_vars[self.rbf.rb_var.get()].get()

        # Record validity of entries
        validation_results: list[bool] = self._entry_validation(
            active_input_method
        )

        # Format entries according to validity
        self._format_entries(active_input_method, validation_results)

        if False not in validation_results:
            if active_input_method == "from list":
                vals = [self.input_section.input_frames[0].var.get()]

            elif active_input_method == "by typing":
                vals = [self.input_section.input_frames[1].var.get()]

            elif active_input_method == "as range":
                start = float(self.input_section.input_frames[2].var.get())
                end = float(self.input_section.input_frames[3].var.get())
                steps = int(self.input_section.input_frames[4].var.get())
                vals = list(np.linspace(start, end, steps))
            else:
                msg = (
                    f"Active input method ({active_input_method}) "
                    "not supported."
                )
                raise ValueError(msg)
            active_group: str = self.parent.group_selection_cb.var.get()

            self.parent.calc_params[active_group].add_values(self.param, vals)

            self.load()

    def _entry_validation(self, active_input_method: str) -> list[bool]:
        """Validate the value in a parameter entry widget.

        This is a callback for Tkinter validation.
        """
        match active_input_method:
            case "from list":
                param_var = self.input_section.input_frames[0].var
                is_valid = [self._validate(param_var)]
            case "by typing":
                param_var = self.input_section.input_frames[1].var
                is_valid = [self._validate(param_var)]
            case "as range":
                param_vars = [
                    self.input_section.input_frames[2].var,
                    self.input_section.input_frames[3].var,
                    self.input_section.input_frames[4].var,
                ]
                is_valid = self._validate_range(param_vars)
            case _:
                msg = (
                    'Invalid "active_input_method. '
                    '"active_input_method" must be one of: '
                    '"from list", "by typing", and "as range".'
                )
                raise ValueError(msg)
        return is_valid

    def _validate(self, var: tk.StringVar) -> bool:
        """Validates value from var.get().

        Resolves issue with values being stored as strings in ttk.Entry
        widgets by attempting to cast the value from var.get() into the
        various allowed types for 'param' and validating the cast value.

        Args:
            var (tk.Variable): A tk.Variable object whose value is to be
                validated.

            param: InputParameter to use for validation.

        Returns:
            bool: True if the value obtained by var.get() is valid. False
            otherwise.
        """
        return self.param.validate(validation.val_to_native(var.get()))

    def _validate_range(self, param_vars: list[tk.StringVar]) -> list[bool]:
        """Validates whether the range specified is valid.

        Args:
            param_vars (List[tk.StringVar]): The list of tk.StringVar's which
            represent the start, stop, and steps entries.

        Returns:
            List[bool]: Booleans indicating which entries are valid.
        """
        validation_results: list[bool] = [False, False, False]

        # Validate start and stop values
        validation_results[0] = self._validate(param_vars[0])
        validation_results[1] = self._validate(param_vars[1])

        # Check that the start value is less than or equal to the stop value
        if (
            validation_results[0]
            and validation_results[1]
            and float(param_vars[0].get()) > float(param_vars[1].get())
        ):
            validation_results[0] = False
            validation_results[1] = False

        # Verify that the number of steps specified is a nonnegative integer
        try:
            steps = float(param_vars[2].get())
            if steps % 1 != 0 and steps < 0:
                raise ValueError(
                    "Number of steps must be a " + "nonnegative integer."
                )

            validation_results[2] = True
        except ValueError:
            validation_results[2] = False
            return validation_results

        # If values are restricted to integers, verify that each value in range
        # will be an integer
        if float not in self.param.allowed_types:
            start = int(param_vars[0].get())
            stop = int(param_vars[1].get())

            if steps < 2:  # noqa: PLR2004
                validation_results[2] = True
            else:
                validation_results[2] = (stop - start) % (steps - 1) == 0

        return validation_results

    def _format_entries(
        self, active_input_method: str, validation_results: list[bool]
    ) -> None:
        """Format the text in the all `EntryFrame`s based on validity.

        Args:
            active_input_method: A string indicating how the parameter is
                being defined. One of "from list", "by typing", or "as range".
            validation_results: A list of booleans of length equal to the
                number of input frames, which indicates the validity
                of the input in the corresponding input frame.
        """
        widgs: list[ttk.Combobox | ttk.Entry | tk.Spinbox] = []

        if active_input_method == "from list":
            widgs.append(self.input_section.input_frames[0].widg)
        elif active_input_method == "by typing":
            widgs.append(self.input_section.input_frames[1].widg)
        elif active_input_method == "as range":
            widgs.append(self.input_section.input_frames[2].widg)
            widgs.append(self.input_section.input_frames[3].widg)
            widgs.append(self.input_section.input_frames[4].widg)

        for i, widg in enumerate(widgs):
            if validation_results[i]:
                colour = "white"
                style_prefix = "valid."
            else:
                colour = "red"
                style_prefix = "invalid."

            if isinstance(widg, tk.Spinbox):
                widg.configure(foreground=colour)
            else:
                style: ttk.Style = ttk.Style()
                style_name: str = style_prefix + widg.winfo_class()
                style.configure(style_name, foreground=colour)
                widg.configure(style=style_name)

    def remove_parameter_values(self) -> None:
        """Remove selected parameter values."""
        selected = self.lbf.listbox.curselection()

        active_group: str = self.parent.group_selection_cb.var.get()

        self.parent.calc_params[active_group].remove_values(
            self.param, selected
        )

        self.load()

    def clear_parameter_values(self) -> None:
        """Remove all parameter values."""
        self.lbf.listbox.selection_set(0, self.lbf.listbox.size() - 1)
        self.remove_parameter_values()

    def create_default_button(self) -> tuple[ttk.Checkbutton, tk.IntVar]:
        """Create the 'Use default value' `Checkbutton` and `IntVar`."""
        var = tk.IntVar()
        check_b = ttk.Checkbutton(
            self,
            command=self.use_default,
            text="Use default value",
            variable=var,
        )
        return check_b, var

    def use_default(self) -> None:
        """Use the default value for the parameter."""
        self.clear_parameter_values()

        if self.check_var.get() == 1:
            statespec = ["disabled"]
            state = tk.DISABLED
            active_group: str = self.parent.group_selection_cb.var.get()
            self.parent.calc_params[active_group].add_values(
                self.param, [str(self.param.default)]
            )
            self.load()

            # Deactivate input frames
            for frame in self.input_section.input_frames:
                try:
                    frame.widg.state(statespec=statespec)
                except AttributeError:
                    frame.widg.configure(state=state)
        else:
            statespec = ["!disabled"]
            state = tk.NORMAL
            self.set_parameter_entry_method()

        for rb in self.rbf.rbs:
            rb.state(statespec=statespec)

        self.lbf.listbox.configure(state=state)

        for child in self.button_frame.winfo_children():
            child.state(statespec=statespec)

    def organize(self) -> None:
        """Grid GUI elements."""
        self.rbf.grid(column=0, padx=5, pady=5, row=0)
        self.input_section.grid(
            column=0, columnspan=2, padx=5, pady=5, row=1, rowspan=4
        )
        self.lbf.grid(
            column=3, columnspan=2, row=1, rowspan=4, sticky=tk.N + tk.S
        )
        self.button_frame.grid(column=2, padx=5, row=3, rowspan=3, sticky=tk.S)
        if self.param.default is not None:
            self.default_button.grid(
                column=4, padx=5, pady=5, row=0, sticky=tk.N + tk.E
            )

        (cols, _) = self.grid_size()

        for i in range(cols):
            self.columnconfigure(i, weight=1)

    def configure_rbs(self) -> None:
        """Activate/deactivate `Radiobutton`s based on valid entry methods."""
        for rb in self.rbf.rbs:
            rb.configure(command=self.set_parameter_entry_method)

        self.rbf.rbs[0].invoke()

    def set_parameter_entry_method(self) -> None:
        """Determines the flags for each widget and calls self.set_states.

        Raises:
            ValueError: If string corresponding to active Radiobutton is
            unexpected.
        """
        active_input_method = self.rbf.str_vars[self.rbf.rb_var.get()].get()

        if active_input_method == "from list":
            self.set_states([1, 0, 0, 0, 0])
        elif active_input_method == "by typing":
            self.set_states([0, 1, 0, 0, 0])
        elif active_input_method == "as range":
            self.set_states([0, 0, 1, 1, 1])
        else:
            msg = (
                "The variable 'rb' does not correspond to the"
                "value of an expected Radiobutton"
            )
            raise ValueError(msg)

    def set_states(self, flags: list[int]) -> None:
        """Sets the states of the parameter entry widgets.

        Args:
            flags: The indices correspond to the widgets as
            follows:
                0: Widget with label "select"
                1: Widget with label "enter"
                2: Widget with label "start"
                3: Widget with label "stop"
                4: Widget with label "steps"
        """
        for i, flag in enumerate(flags):
            _Widg = TypeVar(
                "_Widg", ttk.Combobox, ttk.Entry, tk.Spinbox, ttk.Frame
            )
            widg: _Widg = self.input_section.input_frames[i].widg

            if flag == 0:
                if isinstance(widg, tk.Spinbox):
                    widg.configure(state=tk.DISABLED)
                else:
                    widg.state(statespec=["disabled"])
            elif flag == 1:
                if isinstance(widg, tk.Spinbox):
                    widg.configure(state=tk.NORMAL)
                else:
                    widg.state(statespec=["!disabled"])

    def load(self) -> None:
        """Load the displayed parameter values."""
        group = self.parent.group_selection_cb.var.get()
        param_values = [
            str(val)
            for val in self.parent.calc_params[group].values[self.param]
        ]
        self.lbf.clear_listbox()

        for val in param_values:
            self.lbf.listbox.insert(tk.END, val)


class ParameterSelectionCombobox(ttk.Combobox):
    """A `Combobox` to slect a parameter whose values to display.

    Args:
        parent: The `ParameterSelectionTab` to which this Combobox belongs.
        var: A :class:`tkinter.StringVar` which stores the name of the
            parameter whose values are being displayed.
    """

    def __init__(self, parent: "ParameterSelectionTab") -> None:
        """Initialize an `ParameterSelectionCombobox`.

        Args:
            parent: The `ParameterSelectionTab` to which this Combobox belongs.
        """
        values: list[str] = [param.name for param in parent.params]
        text_var = tk.StringVar(value=values[0])

        super().__init__(
            parent,
            state="readonly",
            textvariable=text_var,
            validate="all",
            values=values,
        )

        self.parent: ParameterSelectionTab = parent
        self.var = text_var
        cmd = self.register(self.change_parameter_panel)
        self.configure(validatecommand=cmd)

    def load(self) -> None:
        """Populate the `Combobox` with parameter names."""
        values: list[str] = [param.name for param in self.parent.params]
        self.configure(values=values)

        if values:
            if self.current() == -1:
                self.current(0)
        else:
            self.set("")

    def change_parameter_panel(self) -> bool:
        """Display a new `ParameterPanel` for the parameter. Returns True."""
        if not self.winfo_viewable():
            return True

        if self.var.get() == "":
            if self.parent.panel_to_display:
                self.parent.panel_to_display.pack_forget()

            return True

        self.parent.panel_to_display.pack_forget()

        for panel in self.parent.param_panels:
            if panel.param.name == self.var.get():
                self.parent.panel_to_display = panel

        self.parent.panel_to_display.pack(padx=5, pady=5, side=tk.TOP)

        return True


class ParameterSelectionTab(ttk.Frame):
    """A GUI element for defining parameter values.

    Attributes:
        parent: The :class:`tkinter.ttk.Notebook` in which the
            `ParameterSelectionTab` resides.
        app: The running :class:`gui.GUI` instance.
        group_selection_cb: The :class:`GroupSelectionCombobox` for selecting
            the active calculation parameter group.
        param_panels: The :class:`ParameterPanel`s for each calculation
            parameter.
        panel_to_display: The :class:`ParameterPanel` to display.
        param_selection_cb: The :class:`tkinter.Combobox` used to select the
            active parameter.
    """

    def __init__(self, main_app: "gui.GUI") -> None:
        """Initialize a `ParameterSelectionTab`.

        Args:
            main_app: The running :class:`gui.GUI` instance.
        """
        super().__init__(main_app.notebook)
        self.parent: ttk.Notebook = main_app.notebook
        self.app: gui.GUI = main_app

        self._params: list[job.CalculationParameter] = (
            self.load_parameter_list()
        )
        self._calc_params: dict[str, groups.CalculationParameterGroup] = (
            self.load_calc_params()
        )

        self.group_selection_cb = GroupSelectionCombobox(self)

        self.param_panels: list[ParameterPanel] = []
        self.panel_to_display: ParameterPanel | None = None

        self.param_selection_cb: ParameterSelectionCombobox | None = None

    @property
    def params(self) -> list[job.CalculationParameter]:
        """Return the calculation parameters."""
        return self._params.copy()

    @params.setter
    def params(self, new_params: list[job.CalculationParameter]):
        self._params = new_params

    # BUG: Changing calculator after loading tab doesn't change parameter panels
    # TODO: Call this upon loading and check if changed
    def load_parameter_list(self) -> list[job.CalculationParameter]:
        """Return the parameter list based on the selected calculator."""
        calc_name = self.app.coordinator.calculator_type
        module_name = f"autojob.coordinator.{calc_name.lower()}"
        class_name = calc_name.capitalize() + "Job"
        module = importlib.import_module(module_name)
        job_type: job.Job = getattr(module, class_name)
        params = job_type.input_parameters()
        return params

    def load_panels(self) -> None:
        """Load the parameter panels."""
        if self.group_selection_cb.var.get() != "":
            if self.param_panels:
                for panel in self.param_panels:
                    panel.load()
            else:
                self.param_panels = self.create_param_panels()
                self.panel_to_display: ParameterPanel = self.param_panels[0]
        elif self.param_panels:
            for panel in self.param_panels:
                panel.destroy()

            self.param_panels = []
            self.panel_to_display = None

    @property
    def calc_params(
        self,
    ) -> dict[str, groups.CalculationParameterGroup]:
        """A map from parameter group names to the parameter group."""
        return self._calc_params.copy()

    @calc_params.setter
    def calc_params(
        self,
        new_calc_params: dict[str, groups.CalculationParameterGroup],
    ):
        self._calc_params = new_calc_params
        self.group_selection_cb.load()

    def load_calc_params(
        self,
    ) -> dict[str, groups.CalculationParameterGroup]:
        """Updates or creates calculation parameters.

        Returns:
            A dictionary mapping the names of
            :class:`.groups.CalculationParameterGroup`s to the groups
            themselves.
        """
        new_calc_params = {}

        current_s_groups = list(self.app.coordinator.structure_groups)

        # Populate 'new_calc_params' with old values
        if hasattr(self, "_calc_params"):
            old_calc_params = self.calc_params

            for group in old_calc_params:
                if group in current_s_groups:
                    new_calc_params[group] = old_calc_params[group]

        for group in current_s_groups:
            if group not in list(new_calc_params):
                new_calc_params[group] = groups.CalculationParameterGroup(
                    self.params
                )

        return new_calc_params

    def create_param_panels(
        self,
    ) -> list[ParameterPanel]:
        """The `ParameterPanels` of the `ParameterSelectionTab`."""
        param_panels: list[ParameterPanel] = []

        # Create parameter panels
        for param in self.params:
            param_panels.append(ParameterPanel(self, param))

        return param_panels

    def organize(self) -> None:
        """Pack the GUI elements."""
        self.group_selection_cb.pack(padx=5, pady=5, side=tk.TOP)

        if self.group_selection_cb.var.get() != "":
            self.param_selection_cb.pack(padx=5, pady=5, side=tk.TOP)
        else:
            self.param_selection_cb.pack_forget()
            self.param_selection_cb.current(0)

        if self.panel_to_display is not None:
            self.panel_to_display.pack(padx=5, pady=5, side=tk.TOP)

    def load(self) -> None:
        """Load the GUI elements."""
        self._params = self.load_parameter_list()

        self._calc_params = self.load_calc_params()

        self.group_selection_cb.load()

        if self.param_selection_cb is None:
            self.param_selection_cb = ParameterSelectionCombobox(self)
        else:
            self.param_selection_cb.load()

        self.load_panels()

        self.organize()
