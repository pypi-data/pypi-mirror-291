"""Select structures for structure groups."""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import TYPE_CHECKING

from autojob.coordinator import validation
from autojob.coordinator.gui import groups
from autojob.coordinator.gui import widgets

if TYPE_CHECKING:
    from autojob.coordinator.gui import gui


class StructureSelectionFrame(ttk.Frame):
    """Select structures to use.

    Attributes:
        parent: The :class:`StructureSelectionPanel` in which the
            `StructureSelectionFrame` resides.
        lbf: The :class:`.widgets.ListboxFrame` listing structure
            filenames.
        button_frame: A :class:`tkinter.ttk.Frame` containing "add", "remove",
            and "clear" buttons.
    """

    def __init__(self, parent: "StructureSelectionPanel") -> None:
        """Initialize a `StructureSelectionFrame`.

        Args:
            parent: The :class:`StructureSelectionPanel` in which the
            `StructureSelectionFrame` resides.
        """
        super().__init__(parent)
        self.parent: StructureSelectionPanel = parent

        self._structures: list[str] = []

        self.lbf: widgets.ListboxFrame = widgets.ListboxFrame(
            self, x_stretch=True
        )

        self.button_frame: ttk.Frame = self.create_button_frame()

        self.organize()

    @property
    def structures(self) -> list[str]:
        """The list of structure filenames."""
        return self._structures.copy()

    @structures.setter
    def structures(self, new_structures: list[str]) -> None:
        self._structures = new_structures

        self.parent.parent.load()

    def load(self) -> None:
        """Reload the structures displayed in the Listbox."""
        # Clear list
        end = self.lbf.listbox.size() - 1
        self.lbf.listbox.delete(0, end)

        # Add new structures
        for structure in self._structures:
            self.lbf.listbox.insert(tk.END, structure)

    def create_button_frame(self) -> ttk.Frame:
        """Create "add", "remove", and "clear" buttons."""
        subframe: ttk.Frame = ttk.Frame(self)
        # Configure "add" button
        add_button = ttk.Button(
            subframe, text="add", command=self.add_structures
        )

        # Configure "remove" button
        rm_button = ttk.Button(
            subframe, text="remove", command=self.remove_structures
        )

        # Configure "clear" button
        clr_button = ttk.Button(
            subframe, text="clear", command=self.clear_structures
        )

        add_button.grid(column=0, row=0)
        rm_button.grid(column=1, row=0)
        clr_button.grid(column=2, row=0)

        return subframe

    def add_structures(self) -> None:
        """Add structure filenames from a file dialog."""
        filetypes = (
            ("ase trajectories", "*.traj"),
            ("CONTCARs", "CONTCAR"),
            ("POSCARs", "POSCAR"),
            ("VASP output files", "*.xml"),
            ("WAVECARs", "WAVECAR"),
            ("All files", "*.*"),
        )

        filenames = filedialog.askopenfilenames(
            title="Select structures",
            # TODO: set to "./" for distribution
            initialdir="./tests/test_structure_files",
            filetypes=filetypes,
        )

        # Add new structures and remove duplicates
        structures = self.structures
        structures.extend(filenames)
        structures = list(dict.fromkeys(structures))
        self.structures = structures

    def remove_structures(self) -> None:
        """Remove selected structures from the Listbox."""
        indices_to_remove = self.lbf.listbox.curselection()
        end = self.lbf.listbox.size() - 1
        copy = self.lbf.listbox.get(0, end)
        structures_to_remove = [copy[i] for i in indices_to_remove]
        new_structures: list[str] = []

        if structures_to_remove:
            for structure in self._structures:
                if structure not in structures_to_remove:
                    new_structures.append(structure)

        # Defer to structures 'property' to handle updating
        self.structures = new_structures

    def clear_structures(self) -> None:
        """Remove all structures from the Listbox."""
        self.lbf.listbox.selection_set(0, self.lbf.listbox.size() - 1)

        self.remove_structures()

    def organize(self) -> None:
        """Pack frames."""
        self.lbf.pack(expand=True, fill=tk.X, side=tk.TOP)
        self.button_frame.pack(fill=tk.X, side=tk.TOP)


class GroupButtonFrame(ttk.Frame):
    """Define StructureGroups.

    Attributes:
        parent: The :class:`StructureSelectionPanel` in which the
            `GroupButtonFrame` resides.
        create_group_entry: The :class:`tkinter.ttk.Entry` for entering
            structure group names.
        create_group_button: The :class:`tkinter.ttk.Entry` for creating
            structure groups.
        entry_var: The :class:`tkinter.StringVar` storing the name of the
            structure group to create.
        del_group_cb: The :class:`tkinter.Combobox` for selecting which
            structure group to delete.
        del_group_button: The :class:`tkinter.ttk.Entry` for deleting
            structure groups.
        cb_var1: The :class:`tkinter.StringVar` storing the name of the
            structure group to delete.
        groups_cb: The :class:`tkinter.Combobox` for selecting which
            structure group structures are to be added to.
        add_to_group_button: The :class:`tkinter.ttk.Button` for adding
            selected structures to structure groups.
        cb_var2: The :class:`tkinter.StringVar` storing the name of the
            structure group to which selected structures will be added.
    """

    def __init__(self, parent: "StructureSelectionPanel") -> None:
        """Initialize a `StructureSelectionFrame`.

        Args:
            parent: The :class:`StructureSelectionPanel` in which the
            `GroupButtonFrame` resides.
        """
        super().__init__(parent)
        self.parent: StructureSelectionPanel = parent

        self._structure_groups: dict[str, groups.StructureGroup] = {}

        (
            self.create_group_entry,
            self.create_group_button,
            self.entry_var,
        ) = self.create_create_group()

        (
            self.del_group_cb,
            self.del_group_button,
            self.cb_var1,
        ) = self.create_del_group()

        (
            self.groups_cb,
            self.add_to_group_button,
            self.cb_var2,
        ) = self.create_add_to_group()

        self.organize()

    @property
    def structure_groups(self) -> dict[str, list[str]]:
        """A mapping from structure group names to structure filenames."""
        return self._structure_groups.copy()

    @structure_groups.setter
    def structure_groups(self, new_groups: dict[str, list[str]]) -> None:
        self._structure_groups = new_groups

        self.parent.parent.load()

    def create_create_group(
        self,
    ) -> tuple[ttk.Entry, ttk.Button, tk.StringVar]:
        """Create the GUI elements for creating structure groups."""
        var: tk.StringVar = tk.StringVar()
        entry = ttk.Entry(self, textvariable=var, width=8)
        button = ttk.Button(
            self, command=self.create_group, text="Create group"
        )

        return entry, button, var

    def create_group(self) -> None:
        """Create a structure group."""
        new_group_name = self.entry_var.get()

        if new_group_name == "":
            return

        if new_group_name not in self._structure_groups:
            structure_groups = self.structure_groups
            structure_groups[new_group_name] = groups.StructureGroup()
            self.structure_groups = structure_groups
            colour = ttk.Style().lookup("TEntry", "foreground")
        else:
            colour = "red"

        style = ttk.Style()
        style.configure("group.TEntry", foreground=colour)
        self.create_group_entry.configure(style="group.TEntry")

    def create_del_group(
        self,
    ) -> tuple[ttk.Combobox, ttk.Button, tk.StringVar]:
        """Create the GUI elements for deleting structure groups."""
        var = tk.StringVar()
        combo_box = ttk.Combobox(
            self, state="readonly", textvariable=var, width=8
        )
        button = ttk.Button(self, command=self.del_group, text="Delete group")

        return combo_box, button, var

    def del_group(self) -> None:
        """Delete a structure group."""
        del self._structure_groups[self.cb_var1.get()]
        self.parent.parent.load()

    def create_add_to_group(
        self,
    ) -> tuple[ttk.Combobox, ttk.Button, tk.StringVar]:
        """Create the GUI elements for updating structure groups."""
        button = ttk.Button(
            self, command=self.add_structures_to_group, text="Add to group"
        )

        var = tk.StringVar()

        def reset_listbox(reason: str) -> bool:
            if reason != "forced":
                self.parent.group_view_frame.load()

            return True

        cmd = self.register(reset_listbox)

        combo_box = ttk.Combobox(
            self,
            state="readonly",
            textvariable=var,
            validate="focus",
            validatecommand=(cmd, "%V"),
            width=8,
        )

        return combo_box, button, var

    def add_structures_to_group(self) -> None:
        """Add selected structures to the selected structure group."""
        listbox = self.parent.structure_selection_frame.lbf.listbox
        indices_to_add = listbox.curselection()

        if indices_to_add:
            end = listbox.size() - 1
            copy = listbox.get(0, end)
            structures_to_add = [copy[i] for i in indices_to_add]

            try:
                active_group = self._structure_groups[self.cb_var2.get()]
                active_group.add_structures(structures_to_add)
                self.parent.parent.load()
            except KeyError:
                pass

    def load(self) -> None:
        """Update the structures in each structure group."""
        structures = self.parent.structure_selection_frame.structures

        # Update groups if structures have changed
        for group in self._structure_groups.values():
            indices_to_remove: list[int] = []
            for i, structure in enumerate(group.structures):
                if str(structure) not in structures:
                    indices_to_remove.append(i)

            group.remove_structures(indices_to_remove)

        self.reset_cbs()

    def reset_cbs(self) -> None:
        """Reset the values displayed by the `Combobox`es."""
        self.del_group_cb["values"] = validation.alphanum_sort(
            list(self._structure_groups)
        )
        self.groups_cb["values"] = validation.alphanum_sort(
            list(self._structure_groups)
        )

        if self._structure_groups:
            if self.del_group_cb.current() == -1:
                self.del_group_cb.current(0)

            if self.groups_cb.current() == -1:
                self.groups_cb.current(0)
        else:
            self.del_group_cb.set("")
            self.groups_cb.set("")

    def organize(self) -> None:
        """Grid widgets."""
        self.create_group_entry.grid(column=0, row=0, sticky=tk.W + tk.E)
        self.create_group_button.grid(column=1, row=0, sticky=tk.W + tk.E)

        self.del_group_cb.grid(column=0, row=1, sticky=tk.W + tk.E)
        self.del_group_button.grid(column=1, row=1, sticky=tk.W + tk.E)

        self.groups_cb.grid(column=0, row=2, sticky=tk.W + tk.E)
        self.add_to_group_button.grid(column=1, row=2, sticky=tk.W + tk.E)

        (_, rows) = self.grid_size()

        for i in range(rows):
            self.rowconfigure(i, weight=1)


class GroupViewFrame(ttk.Frame):
    """View the structures in each structure group.

    Attributes:
        parent: The :class:`StructureSelectionPanel` in which the
            `GroupViewFrame` resides.
        lbf: The :class:`.widgets.ListboxFrame` listing structure
            filenames.
        button_frame: A :class:`tkinter.ttk.Frame` containing "remove"
            and "clear" buttons.
    """

    def __init__(self, parent) -> None:
        """Initialize a `GroupViewFrame`.

        Args:
            parent: The :class:`StructureSelectionPanel` in which the
            `GroupViewFrame` resides.
        """
        super().__init__(parent)
        self.parent: StructureSelectionPanel = parent

        self.lbf: widgets.ListboxFrame = widgets.ListboxFrame(
            self, x_stretch=True
        )

        self.button_frame: ttk.Frame = self.create_button_frame()

        self.organize()

    def create_button_frame(self) -> ttk.Frame:
        """Create "remove" and "clear" buttons."""
        subframe: ttk.Frame = ttk.Frame(self)

        cmd1 = self.remove_structures_from_group
        rm_button = ttk.Button(subframe, command=cmd1, text="remove")

        cmd2 = self.clear_structures_from_group
        clr_button = ttk.Button(subframe, command=cmd2, text="clear")

        placeholder = ttk.Label(subframe, width=10)

        placeholder.grid(column=0, row=0)
        rm_button.grid(column=1, row=0)
        clr_button.grid(column=2, row=0)

        return subframe

    def remove_structures_from_group(self) -> None:
        """Remove selected structures from the selected structure group."""
        indices_to_remove = self.lbf.listbox.curselection()
        group = self.parent.group_button_frame.cb_var2.get()
        self.parent.group_button_frame.structure_groups[
            group
        ].remove_structures(indices_to_remove)
        self.load()

    def clear_structures_from_group(self) -> None:
        """Remove all structures from the selected structure group."""
        self.lbf.listbox.selection_set(0, self.lbf.listbox.size() - 1)
        self.remove_structures_from_group()

    def load(self) -> None:
        """Reload the displayed structures in the selected structure group."""
        displayed_group = self.parent.group_button_frame.cb_var2.get()
        self.lbf.clear_listbox()

        if displayed_group:
            structures = self.parent.group_button_frame.structure_groups[
                displayed_group
            ].structures

            for structure in structures:
                self.lbf.listbox.insert(tk.END, structure)

    def organize(self) -> None:
        """Pack frames."""
        self.lbf.pack(expand=True, fill=tk.X, side=tk.TOP)
        self.button_frame.pack(fill=tk.X, side=tk.TOP)


class StructureSelectionPanel(ttk.LabelFrame):
    """A `LabelFrame` for selecting structures and creating structure groups.

    Attributes:
        parent: The :class:`StructureSelectionTab` in which the
            `StructureSelectionPanel` resides.
        structure_selection_frame: The frame for selecting structures.
        group_button_frame: The frame for creating and deleting structure groups.
        group_view_frame: The frame for displaying the structures of the
            selected group.
    """

    def __init__(self, parent: "StructureSelectionTab") -> None:
        """Initialize a `StructureSelectionPanel`.

        Args:
            parent: The :class:`StructureSelectionTab` in which the
            `StructureSelectionPanel` resides.
        """
        super().__init__(parent, text="Create structure groups")
        self.parent: StructureSelectionTab = parent

        self.structure_selection_frame = StructureSelectionFrame(self)
        self.group_button_frame = GroupButtonFrame(self)
        self.group_view_frame = GroupViewFrame(self)

        self.organize()

    def organize(self) -> None:
        """Pack frames."""
        self.structure_selection_frame.pack(
            expand=True, fill=tk.Y, side=tk.LEFT
        )
        self.group_button_frame.pack(fill=tk.Y, side=tk.LEFT)
        self.group_view_frame.pack(expand=True, fill=tk.Y, side=tk.LEFT)

    def load(self) -> None:
        """Load frames."""
        self.structure_selection_frame.load()
        self.group_button_frame.load()
        self.group_view_frame.load()


class StructureSelectionTab(ttk.Frame):
    """A tab for selecting structures and creating structure groups.

    Attributes:
        parent: The :class:`tkinter.ttk.Notebook` in which the
            `StructureSelectionTab` resides.
        app: The running :class:`.gui.GUI` instance.
        panel: The contained :class:`StructureSelectionPanel`.
    """

    def __init__(self, main_app: "gui.GUI") -> None:
        """Initialize a `StructureSelectionTab`.

        Args:
            main_app: The running :class:`.gui.GUI` instance.
        """
        super().__init__(main_app.notebook)

        self.parent: ttk.Notebook = main_app.notebook
        self.app: gui.GUI = main_app

        self.panel = StructureSelectionPanel(self)

        self.organize()

    def organize(self) -> None:
        """Pack panel."""
        self.panel.pack(fill=tk.X, ipadx=10, ipady=10, side=tk.TOP)

    def load(self) -> None:
        """Load panel."""
        self.panel.load()
