"""This module defines various specialized `ttk.Frame`s for convenience.

The :class:`~RadiobuttonPanel` class defines a `ttk.LabelFrame` containing
`ttk.Radiobutton`s.

The :class:`ListboxFrame` class defines a `ttk.Frame` containing a
`tk.Listbox`.

The :class:`TreeviewFrame` class defines a `ttk.Frame` containing a
`ttk.Treeview`.
"""

import math
import tkinter as tk
from tkinter import ttk

from autojob.coordinator import validation
from autojob.coordinator.classification import ImplementableEnum


class RadiobuttonPanel(ttk.LabelFrame):
    """A :class:`~ttk.LabelFrame` containing :class:`~ttk.Radiobutton`s.

    This GUI element is designed to allow for the selection of a `Radiobutton`
    corresponding to an `ImplementableEnum`.

    Attributes:
        parent: The :class:`~ttk.Frame` in which the `RadiobuttonPanel`
            resides.
        frame: The :class:`~ttk.Frame` in which the `ttk.Radiobutton`s will
            reside.
        implementable_enum: An :class:`~ImplementableEnum`.
        columns: The number of columns used to display to selection options.
        rb_var: A `tk.IntVar` recording the selected `Radiobutton`.
        rbs: A dictionary mappping `ImplementableEnum`s to their
            representative `Radiobutton`s.
    """

    def __init__(
        self,
        parent: ttk.Frame,
        title: str,
        implementable_enum: ImplementableEnum,
        columns: int,
    ) -> None:
        """Initialize a `RadiobuttonPanel`.

        Args:
            parent: The :class:`~ttk.Frame` in which the `RadiobuttonPanel`
                resides.
            title: The title for the `RadiobuttonPanel`.
            implementable_enum: The :class:`.classification.ImplementableEnum`
                that will be enumerated by the `Radiobutton`s.
            columns: The number of columns to be used to display the
                `Radiobutton`s.
        """
        super().__init__(parent, text=title)

        self.parent: ttk.Frame = parent
        self.frame = ttk.Frame(self)
        self.frame.pack()
        self.implementable_enum = implementable_enum
        self.columns = columns

        self.rb_var = tk.IntVar()
        self.rbs: dict[ImplementableEnum, ttk.Radiobutton] = self.creation()

        self.placement()
        self.set_states()

    def creation(
        self,
    ) -> dict[ImplementableEnum, ttk.Radiobutton]:
        """Create `ttk.Radiobutton`s for each `ImplementableEnum`.

        Returns:
            A dictionary mappping `ImplementableEnum`s to their representative
            `Radiobutton`s.
        """
        rbs: dict[ImplementableEnum, ttk.Radiobutton] = {}

        for i, member in enumerate(self.implementable_enum):
            rb = ttk.Radiobutton(
                self.frame,
                text=member.value.title(),
                variable=self.rb_var,
                value=i,
            )

            rbs[member] = rb

        return rbs

    def placement(self) -> None:
        """Organize `RadiobuttonPanel` `ttk.Radiobutton`s."""
        for i, key in enumerate(self.rbs):
            self.rbs[key].grid(
                column=i % self.columns,
                padx=10,
                pady=10,
                row=math.floor(i / self.columns),
                sticky=tk.W,
            )

    def set_states(self) -> None:
        """Set states of `ttk.Radiobutton`s based on implementation."""
        for key in self.rbs:
            if key.is_implemented():
                self.rbs[key].configure(state=tk.NORMAL)
                if key.is_default():
                    self.rbs[key].invoke()
            else:
                self.rbs[key].configure(state=tk.DISABLED)


class ListboxFrame(ttk.Frame):
    """A `ttk.Frame` preconfigured with a `tk.Listbox`.

    Attributes:
        parent: The `ttk.Frame` in which the `ListboxFrame` will reside.
        x_stretch: Whether or not the `ListboxFrame` will expand horizontally
            to fill the frame.
        listbox: The :class:`tkinter.Listbox` within the `ListboxFrame`.
        yscroll: The :class:`tkinter.ttk.Scrollbar` controlling y-scrolling.
        xscroll: The :class:`tkinter.ttk.Scrollbar` controlling x-scrolling.
    """

    def __init__(self, parent: ttk.Frame, *, x_stretch: bool = False) -> None:
        """Initialize a ``ListboxFrame``.

        Args:
            parent: The ``ttk.Frame`` in which the ``ListboxFrame`` will reside.
            x_stretch: Whether or not the ``ListboxFrame`` will expand horizontally
                to fill the frame.. Defaults to False.
        """
        super().__init__(parent)
        self.parent = parent
        self.x_stretch = x_stretch
        self.listbox: tk.Listbox = self.create_listbox()
        self.yscroll: ttk.Scrollbar = self.create_yscrollbar()
        self.xscroll: ttk.Scrollbar = self.create_xscrollbar()
        self.organize()

    def create_listbox(self) -> tk.Listbox:
        """Creates a ``Listbox``."""
        return tk.Listbox(self, height=10, selectmode=tk.EXTENDED)

    def create_yscrollbar(self) -> ttk.Scrollbar:
        """Creates a y-``Scrollbar``."""
        return ttk.Scrollbar(self, command=self.listbox.yview)

    def create_xscrollbar(self) -> ttk.Scrollbar:
        """Creates an x-``Scrollbar``."""
        return ttk.Scrollbar(
            self, command=self.listbox.xview, orient=tk.HORIZONTAL
        )

    def organize(self) -> None:
        """Organize the `ListboxFrame` elements."""
        if self.x_stretch:
            self.xscroll.pack(fill=tk.X, side=tk.BOTTOM)
            self.listbox.configure(xscrollcommand=self.xscroll.set)

            self.yscroll.pack(fill=tk.Y, side=tk.RIGHT)
            self.listbox.configure(height=15, yscrollcommand=self.yscroll.set)

            self.listbox.pack(expand=True, side=tk.LEFT, fill=tk.X)
        else:
            self.listbox.grid(column=0, row=0)

            self.yscroll.grid(column=1, row=0, sticky=tk.N + tk.S)
            self.listbox.configure(yscrollcommand=self.yscroll.set)

    def clear_listbox(self) -> None:
        """Clear the ``Listbox``."""
        self.listbox.delete(0, self.listbox.size() - 1)

    @property
    def items(self) -> tuple[float | int | str | None]:
        """Return the elements of the ``Listbox`` as a list."""
        return validation.iter_to_native(
            self.listbox.get(0, self.listbox.size() - 1)
        )


class TreeviewFrame(ttk.Frame):
    """A `ttk.Frame` preconfigured with a `ttk.Treeview`.

    Attributes:
        parent: The `ttk.Frame` in which the `TreeviewFrame` will reside.
        treeview: The :class:`tkinter.ttk.Treeview` within the `TreeviewFrame`.
        yscroll: The :class:`tkinter.ttk.Scrollbar` controlling y-scrolling.
        xscroll: The :class:`tkinter.ttk.Scrollbar` controlling x-scrolling.
    """

    def __init__(self, parent: ttk.Frame) -> None:
        """Initialize a ``ListboxFrame``.

        Args:
            parent: The ``ttk.Frame`` in which the ``ListboxFrame`` will reside.
        """
        super().__init__(parent)
        self.parent: ttk.Frame = parent
        self.treeview: ttk.Treeview = self.create_treeview()
        self.yscroll: ttk.Scrollbar = self.create_yscrollbar()
        self.xscroll: tk.Scrollbar = self.create_xscrollbar()
        self.organize()

    def create_treeview(self) -> ttk.Treeview:
        """Creates a ``Treeview``."""
        return ttk.Treeview(
            self, height=10, selectmode=tk.EXTENDED, show="tree"
        )

    def create_yscrollbar(self) -> ttk.Scrollbar:
        """Creates a y-``Scrollbar``."""
        return ttk.Scrollbar(self, command=self.treeview.yview)

    def create_xscrollbar(self) -> ttk.Scrollbar:
        """Creates an x-``Scrollbar``."""
        return ttk.Scrollbar(
            self, command=self.treeview.xview, orient=tk.HORIZONTAL
        )

    def organize(self) -> None:
        """Organize the `TreeviewFrame` elements."""
        self.xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.treeview.configure(xscrollcommand=self.xscroll.set)

        self.yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.configure(height=15, yscrollcommand=self.yscroll.set)

        self.treeview.pack(expand=True, side=tk.LEFT, fill=tk.X)

    def clear_treeview(self) -> None:
        """Deletes all items in the treeview."""
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    @property
    def items(self) -> dict[str, dict]:
        """Return the elements of the ``Treeview`` as a nested dictionary."""
        items = {}

        def get_descendants(iid: str) -> dict:
            descendants = {}
            children = self.treeview.get_children(iid)

            for child in children:
                key = self.treeview.item(child, "text")

                if key in items:
                    msg = f"Duplicate items in treeview: {key}."
                    raise ValueError(msg)

                descendants[key] = get_descendants(child)

            return descendants

        for top_level_item in self.treeview.get_children():
            key = self.treeview.item(top_level_item, "text")

            if key in items:
                msg = f"Duplicate items in treeview: {key}."
                raise ValueError(msg)

            items[key] = get_descendants(top_level_item)

        return items
