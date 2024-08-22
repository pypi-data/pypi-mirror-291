"""GUI elements for the submission configuration panel.

Exported classes:
    GroupButtonFrame: a :class:`.ttk.Frame `subclass containing a button which
        handles the logic of creating submission parameter groups.
    GroupSummary: :class:`tkinter.TopLevel` subclass used to display a summary
        for a submission parameter group.
    SelectionPanel: :class:`.ttk.LabelFrame` subclass used as base class for
        submission configuration panels (i.e., :class:`StructureSelectionPanel`,
        :class:`ValueSelectionPanel`)
    SelectionFrame: :class:`.ttk.Frame` subclass used to display values to be
        selected.
    SpecButton: :class:`.ttk.Button` subclass that adds selected values from
        :class:`SelectionFrame` to :class:`ViewFrame`
    ViewFrame: :class:`ttk.Frame` subclass used to display selected values.
    ButtonFrame: :class:`.ttk.Frame` subclass for adding and removing values
        from :class:`ViewFrame`.
    ParameterSelectionCombobox: :class:`.ttk.Combobox` subclass for adding
        specifications to submission parameter groups.
    StructureSelectionPanel: :class:`SelectionPanel` subclass for selecting
        structures for submission parameter group.
    ValueSelectionPanel: :class:`SelectionPanel` subclass for selecting
        parameter values for submission parameter group.
    AddToGroupFrame: :class:`.ttk.Frame` subclass for adding new specifications
        to submission parameter groups.
    SubmissionConfigurationTab: :class:`.ttk.Frame` subclass for configuring
        submission parameters.
"""

import pathlib
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from typing import Any

from autojob.coordinator import coordinator
from autojob.coordinator import job
from autojob.coordinator import validation
from autojob.coordinator.gui import groups
from autojob.coordinator.gui import widgets

if TYPE_CHECKING:
    from autojob.coordinator.gui import gui


class GroupButtonFrame(ttk.Frame):
    """A container frame for `ttk.GroupButton`s.

    Attributes:
        parent: The :class:`~SubmissionConfigurationTab` in which the
            `GroupButtonFrame` resides.
        create_group_entry: The `ttk.Entry` widget used to enter the group
            name.
        create_group_button: The `ttk.Button` widget used to enter the group
            name.
        entry_var: The `tk.StringVar` storing the group name.
        del_group_cb: The `ttk.Combobox` used to select a group to delete.
        del_group_button: The `ttk.Button` used to delete a group.
        cb_var: The `tk.StringVar` referencing the group to delete.
        view_group_button: The `ttk.Button` used to view all submission groups
            that have been created.
        group_summary: A :class:`~GroupSummary` object used to view the groups
            that have been created.
    """

    def __init__(self, parent: "SubmissionConfigurationTab") -> None:
        """Initialize a `GroupButtonFrame`.

        Args:
            parent: The :class:`~SubmissionConfigurationTab` in which the
            `GroupButtonFrame` resides.
        """
        super().__init__(parent)
        self.parent: SubmissionConfigurationTab = parent

        self._submission_parameter_groups: dict[
            str, groups.SubmissionParameterGroup
        ] = {}

        (
            self.create_group_entry,
            self.create_group_button,
            self.entry_var,
        ) = self.create_create_group()

        (
            self.del_group_cb,
            self.del_group_button,
            self.cb_var,
        ) = self.create_del_group()

        (self._placeholder, self.view_group_button) = self.create_view_group()

        self.group_summary: tk.Toplevel | None = None

        self.organize()

    # TODO: confirm type
    @property
    def submission_parameter_groups(
        self,
    ) -> dict[str, groups.SubmissionParameterGroup]:
        """A map from group names to submission parameter groups."""
        return self._submission_parameter_groups.copy()

    # TODO: confirm type
    @submission_parameter_groups.setter
    def submission_parameter_groups(
        self, new_groups: dict[str, list[str]]
    ) -> None:
        """Set the submission parameter groups.

        The `GroupButtonFrame` is reloaded after setting.

        Args:
            new_groups: WIP
        """
        self._submission_parameter_groups = new_groups
        self.parent.load()

    def create_create_group(
        self,
    ) -> tuple[ttk.Entry, ttk.Button, tk.StringVar]:
        """Create the widgets for creating submission parameter groups.

        Returns:
            A 3-tuple (`entry`, `button`, `var`). `entry` is the `ttk.Entry`
            widget in which one specifies the name of a new submission
            parameter group. `button` is a `ttk.Button` used to finalize
            submission parameter group creation. `var` is the `tk.StringVar`
            associated with `entry`.
        """
        var: tk.StringVar = tk.StringVar()
        entry = ttk.Entry(self, textvariable=var, width=8)
        button = ttk.Button(
            self, command=self.create_group, text="Create group"
        )

        return entry, button, var

    def create_group(self) -> None:
        """Create a submission parameter group.

        The text in `GroupButtonFrame.create_group_entry` is coloured red if a
        submission parameter group with the same name already exists.
        """
        new_group = self.entry_var.get()

        if new_group == "":
            return

        if new_group not in list(self._submission_parameter_groups):
            self._submission_parameter_groups[new_group] = (
                groups.SubmissionParameterGroup()
            )
            colour = ttk.Style().lookup("TEntry", "foreground")
            self.parent.load()
        else:
            colour = "red"

        style = ttk.Style()
        style.configure("group.TEntry", foreground=colour)
        self.create_group_entry.configure(style="group.TEntry")

    def create_del_group(
        self,
    ) -> tuple[ttk.Combobox, ttk.Button, tk.StringVar]:
        """Creates a group of widgets for deleting submission parameter groups.

        Returns:
            A 3-tuple (`combo_box`, `button`, `var`). `combo_box` is a
            `ttk.Combobox` used to select a submission parameter group to
            delete. `button` is a `ttk.Button` that when pressed, deletes a
            group. `var` is a `tk.StringVar` containing the name of the
            selected group.
        """
        var = tk.StringVar()
        combo_box = ttk.Combobox(
            self,
            state="readonly",
            textvariable=var,
            width=8,
        )
        button = ttk.Button(self, command=self.del_group, text="Delete group")

        return combo_box, button, var

    def del_group(self) -> None:
        """Delete a submission parameter group."""
        to_del = self.cb_var.get()
        del self._submission_parameter_groups[to_del]

    def create_view_group(self) -> tuple[ttk.Frame, ttk.Button]:
        """Create a group of widgets for viewing submission parameter groups.

        Returns:
            A tuple (`placeholder`, `button`). `placeholder` is an empty
            `ttk.Frame` used for alignment. `button` is a `ttk.Button` used to
            view existing submission parameter groups.
        """
        placeholder = ttk.Frame(self)
        button = ttk.Button(self, command=self.view_groups, text="View groups")

        return placeholder, button

    def view_groups(self) -> None:
        """View created submission parameter groups in a new window."""
        self.group_summary = GroupSummary(self)

    def load(self) -> None:
        """Load the widgets in `GroupButtonFrame` with updated data."""
        self.del_group_cb["values"] = validation.alphanum_sort(
            self._submission_parameter_groups
        )

        if self._submission_parameter_groups:
            if self.del_group_cb.current() == -1:
                self.del_group_cb.current(0)
        else:
            self.del_group_cb.set("")

        if self.group_summary:
            self.group_summary.load()

    def update_groups(
        self, group: str, new_group: dict[str, dict[str, list[str]]]
    ) -> None:
        """Update the selected group with the new spec.

        Args:
            group: The name of the active submission parameter group.
            new_group: A dictionary mapping structures to
                mappings from calculation parameter names to values.
        """
        self._submission_parameter_groups[group].update(new_group)

    def organize(self) -> None:
        """Organize `ttk.Entries` and `ttk.Buttons` in 2x3 grid."""
        self.create_group_entry.grid(
            column=0, padx=40, row=0, sticky=tk.W + tk.E
        )
        self.create_group_button.grid(
            column=0, padx=40, row=1, sticky=tk.W + tk.E
        )

        self.del_group_cb.grid(column=1, padx=40, row=0, sticky=tk.W + tk.E)
        self.del_group_button.grid(
            column=1, padx=40, row=1, sticky=tk.W + tk.E
        )

        self._placeholder.grid(column=2, padx=40, row=0, sticky=tk.W + tk.E)
        self.view_group_button.grid(
            column=2, padx=40, row=1, sticky=tk.W + tk.E
        )

        (cols, _) = self.grid_size()

        for i in range(cols):
            self.columnconfigure(i, weight=1)


class GroupSummary(tk.Toplevel):
    """View a summary of all created submission parameter groups.

    Attributes:
        controller: The :class:`GroupButtonFrame` responsible for launching
            the `GroupSummary`.
        tbf: The :class:`.widgets.TreeviewFrame` containing the summary of all
            submission parameter groups.
    """

    def __init__(self, controller: GroupButtonFrame) -> None:
        """Initialize a `GroupSummary`.

        Args:
            controller: The :class:`GroupButtonFrame` responsible for launching
            the `GroupSummary`.
        """
        super().__init__(height=300, padx=20, pady=20, width=400)

        self.controller: GroupButtonFrame = controller
        self.tbf = widgets.TreeviewFrame(self)
        self.tbf.treeview.pack(fill=tk.BOTH)

        self.populate()
        self.title("Parameter Groups")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.tbf.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.lift()

    # TODO: refactor
    def populate(self) -> None:
        """Populate `GroupSummary.tbf` with each submission parameter group."""
        self.tbf.clear_treeview()

        submission_parameter_groups: dict[
            str, groups.SubmissionParameterGroup  # groups
        ] = self.controller.submission_parameter_groups

        # ? maybe use itertools.groupby?
        for group in validation.alphanum_sort(submission_parameter_groups):
            group_iid = self.tbf.treeview.insert("", "end", text=group)
            structures = list(submission_parameter_groups[group].values)
            structures.sort()
            for structure in structures:
                structure_iid = self.tbf.treeview.insert(
                    group_iid, "end", text=str(structure)
                )
                params = submission_parameter_groups[group].values[structure]

                for param in params:
                    param_iid = self.tbf.treeview.insert(
                        structure_iid, "end", text=str(param)
                    )
                    values = [
                        str(x)
                        for x in submission_parameter_groups[group].values[
                            structure
                        ][param]
                    ]
                    values = validation.alphanum_sort(values)
                    for value in values:
                        self.tbf.treeview.insert(param_iid, "end", text=value)

    def load(self) -> None:
        """Reload the displayed submission parameter groups."""
        self.populate()

    def on_close(self) -> None:
        """Delete `GroupSummary`."""
        self.controller.group_summary = None
        self.destroy()


class SelectionPanel(ttk.LabelFrame):
    """Select and view items.

    Attributes:
        parent: The :class:`SubmissionConfigurationTab` to which the
            :class:`SelectionPanel` belongs.
        selection_frame: A :class:`SelectionFrame` from which users select
            items.
        view_frame: A :class:`ViewFrame` displaying selected items.
        button_frame: A `ttk.Frame` with `ttk.Button`s for item removing and
            clearing.
        spec_button: A `ttk.Button` controlling spec addition.
    """

    def __init__(self, parent: Any, text: str) -> None:
        """Initialize a `SelectionPanel`.

        Args:
            parent: The :class:`SubmissionConfigurationTab` to which the
            :class:`SelectionPanel` belongs.
            text: The text used to indicate what is being selected.
        """
        super().__init__(parent, text="Select " + text)
        self.parent: SubmissionConfigurationTab = parent
        self.selection_frame = SelectionFrame(self, text)
        self.view_frame = ViewFrame(self)
        self.button_frame = ButtonFrame(self)
        self.spec_button = SpecButton(self)
        self.organize()

    def organize(self) -> None:
        """Organize buttons and frames into 1x4 grid."""
        self.selection_frame.grid(column=0, row=0, sticky=tk.W + tk.E)

        self.spec_button.grid(column=1, row=0, padx=10)
        self.view_frame.grid(column=2, row=0, sticky=tk.W + tk.E)
        self.button_frame.grid(column=3, row=0, padx=10)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

    def load(self) -> None:
        """Load the selection and view frames."""
        self.selection_frame.load()
        self.view_frame.load()


# TODO: Rename to FilterFrame, tbf -> tvf
# ? What does select_from do?
class SelectionFrame(ttk.Frame):
    """Create task filters.

    Attributes:
        parent: The :class:`StructureSelectionPanel` in which structures in
            the filter are selected.
        select_from: A `str` indicating from where the values within the frame
            are to be populated. If `"values"`, then the values are obtained
            from calculation parameter groups. If `"structure"`, then the
            values are obtained from the structures.
        tbf: A :class:`TreeviewFrame` containing the values if
            `SelectionFrame.select_from = "values"`, else `None`.
        lbf: A :class:`ListboxFrame` containing the values if
            `SelectionFrame.select_from = "structure"`, else `None`.
    """

    def __init__(
        self, parent: "StructureSelectionPanel", select_from: str
    ) -> None:
        """Initialize a `SelectionFrame`.

        Args:
            parent: The :class:`StructureSelectionPanel` in which structures in
            the filter are selected.
            select_from: A `str` indicating from where the values within the
                frame are to be populated. If `"values"`, then the values are
                obtained from calculation parameter groups. If `"structure"`, then
                the values are obtained from the structures.
        """
        super().__init__(parent)
        self.parent = parent

        self.select_from = select_from
        # self.tbf = self.lbf = None

        if self.select_from == "values":
            self.tbf = widgets.TreeviewFrame(self)
            self.tbf.treeview.configure(height=7)
        else:
            self.lbf = widgets.ListboxFrame(self, x_stretch=True)
            self.lbf.listbox.configure(height=7)

        self.organize()

    @property
    def items(self) -> list[str] | dict[str, list[str]]:
        """Displayed items (`SelectionFrame.lbf` or `SelectionFrame.lbf`).

        Raises:
            AttributeError: Invalid value of `SelectionFrame.select_from`.

        Returns:
            A list of strings representing structure paths
            (if `SelectionFrame.select_from == "structures") or a dictionary
            mapping parameter names to their values (if
            `SelectionFrame.select_from == "values")
        """
        if self.select_from == "structures":
            return self.structures

        if self.select_from == "values":
            return self.values

        msg = f'Invalid value of "select_from" attribute:{self.select_from}'
        raise AttributeError(msg)

    @property
    def structures(self) -> list[str]:
        """Returns the structures for which parameters have been specified.

        Returns:
            A list of `str` representing the structures for which parameters
            have been specified.
        """
        app: gui.GUI = self.parent.parent.app
        structure_groups: dict[str, list[str]] = (
            app.coordinator.structure_groups
        )
        structures: list[str] = []

        for group in iter(structure_groups.values()):
            for structure in group.structures:
                structures.append(structure)

        return [str(structure) for structure in dict.fromkeys(structures)]

    @property
    def values(self) -> dict[str, list[str]]:
        """A map from calculation parameter names to a list of their values."""
        values = []
        app: gui.GUI = self.parent.parent.app

        structures = [
            pathlib.Path(x)
            for x in self.parent.parent.panels[0].view_frame.lbf.items
        ]

        groups_with_structures = app.coordinator.structure_groups_with(
            structures
        )

        cdr: coordinator.Coordinator = self.parent.parent.app.coordinator

        calc_params: list[job.CalculationParameter] = []

        for calc_param in cdr.calc_params_for(structures):
            param = cdr.calc_param_from(calc_param, groups_with_structures)
            if param not in calc_params:
                calc_params.append(param)

        values = app.coordinator.calc_param_values_for(structures, calc_params)

        return values

    # TODO: change check to "is None"
    def load(self) -> None:
        """Reload displayed contents of `Listbox` or `Treeview`."""
        if hasattr(self, "lbf"):
            self.lbf.clear_listbox()

            # Add new items
            for item in self.items:
                self.lbf.listbox.insert(tk.END, item)
        elif hasattr(self, "tbf"):
            self.tbf.clear_treeview()

            # Add new items
            values = self.items
            for param in iter(values):
                iid = self.tbf.treeview.insert("", "end", text=param)
                for value in values[param]:
                    self.tbf.treeview.insert(iid, "end", text=str(value))

    def organize(self) -> None:
        """Pack `ListboxFrame` or `TreeviewFrame`."""
        # TODO: refer to ttk.TreeView if select_from == 'values'
        if hasattr(self, "lbf"):
            self.lbf.pack(expand=True, fill=tk.X, side=tk.TOP)
        elif hasattr(self, "tbf"):
            self.tbf.pack(expand=True, fill=tk.X, side=tk.TOP)


class SpecButton(ttk.Button):
    """`ttk.Button` that adds a spec.

    Args:
        parent: The parent :class:`~SelectionPanel`.
        src: The widget containing the source frame. This is either a
            :class:`.widgets.TreeviewFrame` (if :attr:`SpecButton.parent` is a
            :class:`ValueSelectionPanel`) or a
            :class:`.widgets.ListboxFrame` (if :attr:`SpecButton.parent` is a
            :class:`StructureSelectionPanel`).
        dest: The widget containing the destination frame. This is either a
            :class:`.widgets.TreeviewFrame` (if :attr:`SpecButton.parent` is a
            :class:`ValueSelectionPanel`) or a
            :class:`.widgets.ListboxFrame` (if :attr:`SpecButton.parent` is a
            :class:`StructureSelectionPanel`).
    """

    def __init__(self, parent: "SelectionPanel") -> None:
        """Initialize `SpecButton`.

        Args:
            parent: The parent :class:`~SelectionPanel`.
        """
        super().__init__(parent, text="Add spec")
        self.parent: SelectionPanel = parent

        if isinstance(self.parent, ValueSelectionPanel):
            self.src: widgets.TreeviewFrame | widgets.ListboxFrame = (
                self.parent.selection_frame.tbf
            )
            self.dest: widgets.TreeviewFrame | widgets.ListboxFrame = (
                self.parent.view_frame.tbf
            )
        else:
            self.src: widgets.TreeviewFrame | widgets.ListboxFrame = (
                self.parent.selection_frame.lbf
            )
            self.dest: widgets.TreeviewFrame | widgets.ListboxFrame = (
                self.parent.view_frame.lbf
            )

        self.configure(command=self.add_spec)

    def add_spec(self) -> None:
        """Add the current parameter specification to the group."""
        if isinstance(self.src, widgets.ListboxFrame):
            self.add_from_listbox()
        else:
            self.add_from_treeview()

        self.parent.parent.load()

    def add_from_listbox(self) -> None:
        """Add spec items from a `ttk.Listbox`."""
        indices_to_add = self.src.listbox.curselection()

        if indices_to_add:
            copy = self.src.listbox.get(0, self.src.listbox.size() - 1)
            items_to_add = [copy[i] for i in indices_to_add]
            end = self.dest.listbox.size() - 1
            items_in_dest = self.dest.listbox.get(0, end)

            for item in items_to_add:
                if item not in items_in_dest:
                    self.dest.listbox.insert(tk.END, item)

    def add_from_treeview(self) -> None:
        """Add spec items from a `ttk.Treeview`."""
        items_to_add = set(self.src.treeview.selection())

        for top_level_item in self.src.treeview.get_children():
            if top_level_item in items_to_add:
                children = list(self.src.treeview.get_children(top_level_item))
            else:
                children = list(
                    items_to_add.intersection(
                        self.src.treeview.get_children(top_level_item)
                    )
                )

            self.add_children(top_level_item, children)

    def add_children(self, top_level_item: str, children: list[str]) -> None:
        """Adds the contents of children items to a `ttk.Treeview` item.

        Args:
            top_level_item: The iid of the item under which the children will
                be added.
            children: A list of iids corresponding to items whose values are
                to be added under `top_level_item`.
        """
        parent_text = self.src.treeview.item(top_level_item, "text")

        values_to_add: list[str] = []

        for item in children:
            text = self.src.treeview.item(item, "text")
            try:
                if text not in self.dest.parent.tbf.items[parent_text]:
                    values_to_add.append(text)
            except KeyError:
                values_to_add.append(text)

        if values_to_add:
            values_to_add = validation.alphanum_sort(values_to_add)
            iid = self.get_iid_in_dest(parent_text)
            for text in values_to_add:
                self.dest.treeview.insert(iid, "end", text=text)

    def get_iid_in_dest(self, parent_text) -> str:
        """Get the iid of an item in the destination `ttk.Treeview`.

        Args:
            parent_text: A string representing the text of the item in the
                destination.

        Returns:
            The iid of the item in the destination `ttk.Treeview`.
        """
        for item in self.dest.treeview.get_children():
            text = self.dest.treeview.item(item, "text")
            if text == parent_text:
                return item

        return self.dest.treeview.insert("", "end", text=parent_text)


class ViewFrame(ttk.Frame):
    """A container `ttk.Frame` for viewing the values defining the spec.

    Attributes:
        parent: The :class:`SelectionPanel` in which the `ViewFrame` resides.
        tbf: The :class:`.widgets.TreeviewFrame` containing the values
            defining the spec. This is `None` if `parent` is a
            :class:`StructureSelectionPanel`.
        lbf: The :class:`.widgets.ListboxFrame` containing the values
            defining the spec. This is `None` if `parent` is a
            :class:`ValueSelectionPanel`.
    """

    def __init__(self, parent: Any) -> None:
        """Initialize a `ViewFrame`.

        Args:
            parent: The :class:`SelectionPanel` in which the `ViewFrame` resides.
        """
        super().__init__(parent)
        self.parent: SelectionPanel = parent

        if isinstance(self.parent, ValueSelectionPanel):
            self.tbf = widgets.TreeviewFrame(self)
            self.tbf.treeview.configure(height=7)
        else:
            self.lbf = widgets.ListboxFrame(self, x_stretch=True)
            self.lbf.listbox.configure(height=7)

        self.organize()

    def load(self) -> None:
        """Update the `ViewFrame` to reflect changes to the allowed values.

        This method updates the `ViewFrame`, removing those items that are
        no longer allowed due to updates to the items from which the spec
        was created.
        """
        if hasattr(self, "tbf"):
            old_items: dict[str, dict] = self.tbf.items
            self.tbf.clear_treeview()
            src: dict[str, dict] = self.parent.selection_frame.tbf.items

            for param, values in old_items.items():
                if param in src:
                    iid = self.tbf.treeview.insert("", "end", text=param)

                    for val in iter(values):
                        if val in src[param]:
                            self.tbf.treeview.insert(iid, "end", text=val)

                    # Remove item related to 'param' if all children related to
                    # 'param' have been removed by updating
                    if not self.tbf.treeview.get_children(iid) and values:
                        self.tbf.treeview.delete(iid)
        else:
            old_items: list[str] = self.lbf.items
            self.lbf.clear_listbox()

            for item in old_items:
                if item in self.parent.selection_frame.items:
                    self.lbf.listbox.insert(tk.END, item)

    def organize(self) -> None:
        """Pack frames."""
        if hasattr(self, "tbf"):
            self.tbf.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        else:
            self.lbf.pack(expand=True, fill=tk.BOTH, side=tk.TOP)


class ButtonFrame(ttk.Frame):
    """A `ttk.Frame` containing `ttk.Button`s for editing specs.

    Args:
        parent: The :class:`SelectionPanel` containing the `ButtonFrame`.
        listbox: The `tk.Listbox` containing the values for the spec. This
            is `None` if the parent :class:`SelectionFrame` has a
            :class:`.widgets.TreeviewFrame`.
        treeview: The `ttk.Treeview` containing the values for the spec. This
            is `None` if the parent :class:`SelectionFrame` has a
            :class:`.widgets.ListboxFrame`.
        buttons: A list of `ttk.Button`s. The first element is the "remove"
            button. The second element is the "clear" button.
    """

    def __init__(self, parent: "SelectionPanel") -> None:
        """Initialize a `ButtonFrame`.

        Args:
            parent: The :class:`SelectionPanel` containing the `ButtonFrame`.
        """
        super().__init__(parent)
        self.parent: SelectionPanel = parent
        if hasattr(self.parent.selection_frame, "lbf"):
            self.listbox = self.parent.view_frame.lbf.listbox
        else:
            self.treeview = self.parent.view_frame.tbf.treeview

        self.buttons: list[ttk.Button] = self.create_buttons()

    def create_buttons(self) -> list[ttk.Button]:
        """Create the "remove" and "clear" buttons.

        Returns:
            A list of `ttk.Button`s. The first element is the "remove"
            button. The second element is the "clear" button.
        """
        rm_button = ttk.Button(self, command=self.remove_items, text="remove")
        clr_button = ttk.Button(self, command=self.clear_items, text="clear")

        rm_button.grid(column=0, row=0)
        clr_button.grid(column=0, row=1)

        return [rm_button, clr_button]

    def remove_items(self) -> None:
        """Remove items from the `Listbox`/`Treeview`."""
        if hasattr(self.parent.selection_frame, "lbf"):
            indices_to_remove = self.listbox.curselection()
            end = self.listbox.size() - 1
            items = self.listbox.get(0, end)
            items_to_remove = [items[i] for i in indices_to_remove]
            self.listbox.delete(0, end)

            if items_to_remove:
                for item in items:
                    if item not in items_to_remove:
                        self.listbox.insert(tk.END, item)

            self.parent.parent.load()
        else:
            to_delete = self.treeview.selection()
            for item in to_delete:
                self.treeview.delete(item)

    def clear_items(self) -> None:
        """Remove all items from the `Listbox`/`Treeview`."""
        if hasattr(self.parent.selection_frame, "lbf"):
            self.listbox.selection_set(0, self.listbox.size() - 1)
        else:
            self.treeview.selection_set(self.treeview.get_children())

        self.remove_items()


class StructureSelectionPanel(SelectionPanel):
    """A :class:`SelectionPanel` for creating specs by selecting structures."""

    def __init__(self, parent: "SubmissionConfigurationTab") -> None:
        """Initialize a `StructureSelectionPanel`.

        Args:
            parent: The :class:`SubmissionConfigurationTab` to which the
            :class:`StructureSelectionPanel` belongs.
        """
        super().__init__(parent, text="structures")


class ValueSelectionPanel(SelectionPanel):
    """A :class:`SelectionPanel` for creating specs by selecting values."""

    def __init__(self, parent) -> None:
        """Initialize a `ValueSelectionPanel`.

        Args:
            parent: The :class:`SubmissionConfigurationTab` to which the
            :class:`ValueSelectionPanel` belongs.
        """
        super().__init__(parent, text="values")


class AddToGroupFrame(ttk.Frame):
    """A container `ttk.Frame` for adding the current spec to a SubmissionGroup.

    Attributes:
        parent: The :class:`SubmissionConfigurationTab`.
        combo_box: The `ttk.Combobox` for selecting the SubmissionGroup.
        button: The `ttk.Button` used to add the current spec to the group.
        var: A `tk.StringVar` referencing the  SubmissionGroup to which
            the spec will be added.
    """

    def __init__(self, parent: Any) -> None:
        """Initialize an `AddToGroupFrame`.

        Args:
            parent: The :class:`SubmissionConfigurationTab`.
        """
        super().__init__(parent)
        self.parent: SubmissionConfigurationTab = parent
        (
            self.combo_box,
            self.button,
            self.var,
        ) = self.create_add_group()
        self.organize()

    def create_add_group(
        self,
    ) -> tuple[ttk.Combobox, ttk.Button, tk.StringVar]:
        """Create the widgets for adding the current spec to a SubmissionGroup.

        Returns:
            A 3-tuple (`combo_box`, `button`, `var`). `combo_box` is a
            `ttk.Combobox` used to select the SubmissionGroup to which the
            spec will be added. `button` is the `ttk.Button` used to add the
            current spec to a `SubmissionGroup`. `var` is the `tk.StringVar`
            referencing the `SubmissionGroup` to which the current spec will
            be added.
        """
        var = tk.StringVar()
        combo_box = ttk.Combobox(
            self,
            state="readonly",
            textvariable=var,
            width=8,
        )
        button = ttk.Button(
            self,
            command=self.add_specs_to_group,
            text="Add all specs to group",
        )

        return combo_box, button, var

    def load(self) -> None:
        """Update `AddToGroupFrame.combo_box` values."""
        self.combo_box["values"] = validation.alphanum_sort(
            self.parent.button_frame.submission_parameter_groups
        )

        if self.parent.button_frame.submission_parameter_groups:
            if self.combo_box.current() == -1:
                self.combo_box.current(0)
        else:
            self.combo_box.set("")

    # TODO: Refactor:
    # TODO:     only add GroupFilter; do not update existing
    def add_specs_to_group(self) -> None:
        """Add current spec to SubmissionGroup or update existing group.

        This method uses the current spec to find all CalculatorParameterGroup
        instances that satisfy the spec (structure and values of calculator
        parameters) and add them to the SubmissionGroup.
        """
        if self.var.get() != "":
            group_name = self.var.get()
        else:
            return

        new_p_groups = {}

        # Collect all structures included in spec
        p_group_structures: list[str] = []
        for structure in self.parent.panels[0].view_frame.lbf.items:
            p_group_structures.append(pathlib.Path(structure))

        p_group_structures.sort()

        # Collect all values included in spec
        vals_panel: ValueSelectionPanel = self.parent.panels[1]

        # Flatten dictionaries (temporary until fixed in Treeview.items)
        # TODO: Replace with tbf.extract_values()?
        new_specs: dict[
            str, dict
        ] = {  # parameter names  # keys are parameter values
            key: validation.iter_to_native(value)
            for key, value in vals_panel.view_frame.tbf.items.items()
        }

        for structure in p_group_structures:
            # Collect all calculation parameters in "new_specs" applicable to
            # "structure"
            param_names = list(
                set(new_specs).intersection(
                    self.parent.app.coordinator.calc_params_for([structure])
                )
            )

            # Structure groups containing 'structure'
            s_groups: list[str] = (
                self.parent.app.coordinator.structure_groups_with([structure])
            )

            param_names = validation.alphanum_sort(param_names)
            params: list[job.CalculationParameter] = []

            # Convert calculation parameter strings to CalculationParameter
            # objects
            for param_name in param_names:
                params.append(
                    self.parent.app.coordinator.calc_param_from(
                        param_name, s_groups
                    )
                )

            # All valid parameter values for 'structure'
            values: dict[
                str, list[str]  # parameter names, parameter values
            ] = self.parent.app.coordinator.calc_param_values_for(
                [structure], params
            )

            param_values: dict[
                str, list[str]
            ] = {}  # parameter names, parameter values

            # Collect all values of "structure" that are specified in
            # "new_specs"
            for param_name, param in zip(param_names, params, strict=False):
                new_values = set(new_specs[param_name]).intersection(
                    values[param_name]
                )

                if len(new_values) == 0:
                    continue

                new_values = [str(x) for x in new_values]
                new_values = validation.alphanum_sort(new_values)
                new_values = validation.iter_to_native(new_values)
                param_values[param] = new_values

            # Adding new values to 'p_groups'
            if param_values:
                new_p_groups[pathlib.Path(structure)] = param_values

        self.parent.button_frame.update_groups(group_name, new_p_groups)

    def organize(self) -> None:
        """Pack `Combbox` and `Button`."""
        self.combo_box.pack(fill=tk.X, side=tk.TOP)
        self.button.pack(fill=tk.X, side=tk.TOP)


class SubmissionConfigurationTab(ttk.Frame):
    """A `ttk.Frame` for configuring SubmissionGroups.

    Attributes:
        parent: The `ttk.Notebook` to which the `SubmissionConfigurationTab`
            belongs.
        app: The :class:`.gui.GUI` controlling the GUI.
        button_frame: The :class:`GroupButtonFrame` used to create, delete,
            and view SubmissionGroups.
        panels: A list of :class:`SelectionPanel`s used to create
            `GroupFilter`s.
        add_to_group_frame: A :class:`AddToGroupFrame` used to add a
            `GroupFilter` to a SubmissionGroup.
    """

    def __init__(self, main_app: "gui.GUI") -> None:
        """Initialize a `SubmissionConfigurationTab`.

        Args:
            main_app: The :class:`.gui.GUI` controlling the GUI.
        """
        super().__init__(main_app.notebook)
        self.parent: ttk.Notebook = main_app.notebook
        self.app = main_app

        self.button_frame: GroupButtonFrame = GroupButtonFrame(self)
        self.panels: list[SelectionPanel] = self.create_panels()
        self.add_to_group_frame = AddToGroupFrame(self)

        self.organize()

    def create_panels(self) -> list[SelectionPanel]:
        """Returns a list containing structure and value selection panels."""
        panels: list[SelectionPanel] = []

        panels.append(StructureSelectionPanel(self))
        panels.append(ValueSelectionPanel(self))

        return panels

    def organize(self) -> None:
        """Pack frames."""
        self.button_frame.pack(side=tk.TOP)

        for panel in self.panels:
            panel.pack(fill=tk.X, padx=10, pady=5, side=tk.TOP)

        self.add_to_group_frame.pack(side=tk.TOP)

    def load(self) -> None:
        """Reload frames."""
        self.button_frame.load()

        for panel in self.panels:
            panel.load()

        self.add_to_group_frame.load()
