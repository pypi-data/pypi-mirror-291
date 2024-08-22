"""Configure scheduler parameters for SubmissionGroups."""

from collections.abc import Callable
import math
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from typing import TypedDict

from autojob import hpc
from autojob.coordinator import validation

if TYPE_CHECKING:
    from autojob.coordinator.gui import gui


class GroupSelectionCombobox(ttk.Combobox):
    """Select a SubmissionGroup.

    Attributes:
        parent: The `JobSubmissionTab` in which the `GroupSelectionCombobox` is embedded.
        var: A :class:`tkinter.StringVar` storing the name of the active SubmissionGroup.

    Note:
        The `.load()` function of the parent frame is called during the validation
        function for the combobox.
    """

    def __init__(self, parent: "JobSubmissionTab") -> None:
        """Initialize a `GroupSelectionCombobox`.

        Args:
            parent: The `JobSubmissionTab` in which the `GroupSelectionCombobox` is embedded.
        """
        text_var = tk.StringVar()

        super().__init__(
            parent,
            state="readonly",
            textvariable=text_var,
            validate="all",
            width=10,
        )

        self.parent: JobSubmissionTab = parent
        self.var = text_var

        def update_frame() -> bool:
            self.parent.load()
            return True

        cmd = self.register(update_frame)
        self.configure(validatecommand=cmd)

    def load(self) -> None:
        """Reload the displayed values of submission parameters."""
        values = list(self.parent.app.coordinator.submission_parameter_groups)
        self.configure(values=validation.alphanum_sort(values))

        if values:
            if self.current() == -1:
                self.current(0)
        else:
            self.set("")


class RunTimePanel(ttk.LabelFrame):
    """Specify a time limit for jobs of the SubmissionGroup.

    Attributes:
        parent: The `JobSubmissionTab` in which the `RunTimePanel` is embedded.
        max_time_limit: The maximum time that can be specified. This will be used as a limit
            for the combo box.
        frames: A list of :class:`tkinter.ttk.Frame`s, containing GUI elements for day, hour, and minute specifications.
        sbs: A list of :class:`tkinter.Spinbox`es, for specifying days, hours, and minutes.
        vars: A list of :class:`tkinter.StringVar`s, storing day, hour, and minute specifications.
    """

    def __init__(
        self, parent: "JobSubmissionTab", time_limit: int = 10080
    ) -> None:
        """Initialize the `RunTimePanel`.

        Args:
            parent: The `JobSubmissionTab` in which the `GroupSelectionCombobox` is embedded.
            time_limit: The maximum time that can be specified. This will be used as a limit
                for the combo box.
        """
        super().__init__(
            parent, text="Set a limit on the total run time of each job."
        )
        self.parent: JobSubmissionTab = parent
        self.max_time_limit = time_limit
        self.frames, self.sbs, self.vars = self.create()

        self.organize()

    def create(
        self,
    ) -> tuple[list[ttk.Frame], list[tk.Spinbox], list[tk.StringVar]]:
        """Create `Frame`, `Spinbox`, and `IntVar` lists."""
        texts = ["days:", "hours:", "minutes:"]
        upper_limits = [
            self.max_time_limit / (60 * 24),
            self.max_time_limit / 60,
            self.max_time_limit,
        ]

        frames: list[ttk.Frame] = []
        sbs: list[tk.Spinbox] = []
        sb_vars: list[tk.StringVar] = []

        for i, text in enumerate(texts):
            frame = ttk.Frame(self)
            label = ttk.Label(frame, text=text, width=5)
            var = tk.StringVar()
            sb = tk.Spinbox(
                frame,
                from_=0,
                state="readonly",
                to=upper_limits[i],
                textvariable=var,
                width=5,
            )
            label.pack(expand=True, fill=tk.X, side=tk.LEFT)
            sb.pack(expand=True, fill=tk.X, side=tk.LEFT)

            sbs.append(sb)
            frames.append(frame)
            sb_vars.append(var)

        return frames, sbs, sb_vars

    def enforce_time_limit(self) -> None:
        """Validate run time specification subject to time limit."""
        group = self.parent.group_cb.var.get()
        days = int(self.vars[0].get())
        hours = int(self.vars[1].get())
        mins = int(self.vars[2].get())
        run_time = {"days": days, "hours": hours, "minutes": mins}
        self.parent.submission_parameters[group]["run time"] = run_time

        time_surplus = self.max_time_limit - (
            days * 24 * 60 + hours * 60 + mins
        )

        self.sbs[0].configure(to=days + math.floor(time_surplus / (24 * 60)))
        self.sbs[1].configure(to=hours + math.floor(time_surplus / (60)))
        self.sbs[2].configure(to=mins + math.floor(time_surplus))

        self.parent.panels["part_panel"].enforce_partition_limits()

    def organize(self) -> None:
        """Pack frames."""
        for frame in self.frames:
            frame.pack(expand=True, fill=tk.X, padx=10, pady=10, side=tk.LEFT)

    def load(self) -> None:
        """Reload displayed day, hour, and minute specificiations."""
        group = self.parent.group_cb.var.get()
        days = int(
            self.parent.submission_parameters[group]["run time"]["days"]
        )
        self.vars[0].set(days)

        hours = int(
            self.parent.submission_parameters[group]["run time"]["hours"]
        )
        self.vars[1].set(hours)

        mins = int(
            self.parent.submission_parameters[group]["run time"]["minutes"]
        )
        self.vars[2].set(mins)


class MemoryPanel(ttk.LabelFrame):
    """Specify a memory limit for jobs of the SubmissionGroup.

    Attributes:
        parent: The `JobSubmissionTab` in which the `MemoryPanel` is embedded.
        entry: The :class:`tkinter.Entry` for specifying memory.
        entry_var: The :class:`tkinter.StringVar` storing the value of the specified memory.
        units_rb_frame: The :class:`tkinter.ttk.Frame` containing the units radiobuttons.
        rbs: A list of :class:`tkinter.Radiobutton`s, for selecting a memory units.
        rb_var: A :class:`tkinter.IntVar` storing the value of the selected memory unit.
        shadow_var: A :class:`tkinter.IntVar` storing the previous value of the selected memory unit.
    """

    def __init__(self, parent) -> None:
        """Initialize a `GroupSelectionCombobox`.

        Args:
            parent: The `JobSubmissionTab` in which the `GroupSelectionCombobox` is embedded.
        """
        super().__init__(
            parent,
            text="Specify the real memory required per cpu (core). Value will be rounded to the nearest integer.",
        )
        self.parent: JobSubmissionTab = parent
        self.entry, self.entry_var = self.create()
        self.units_rb_frame, self.rbs, self.rb_var = self.create_rbs()
        self.shadow_var = self.rb_var.get()

        self.rbs[0].invoke()

        self.organize()

    def create(self) -> tuple[ttk.Entry, tk.StringVar]:
        """Create a `Entry`and `StringVar` for the memory specifying entry."""
        entry_var = tk.StringVar(value=0)
        entry: ttk.Entry = tk.Entry(
            self, textvariable=entry_var, validate="focusout", width=5
        )

        return entry, entry_var

    def validate_memory(self) -> Callable[[str], bool]:
        """Create a validator for the specified memory."""

        def func(val: str) -> bool:
            try:
                val = validation.val_to_native(val)
                if val >= 0:
                    self.parent.panels["part_panel"].enforce_partition_limits()
                    group = self.parent.group_cb.var.get()
                    txt = self.rbs[self.rb_var.get()]["text"]
                    self.parent.submission_parameters[group]["memory"] = (
                        val,
                        txt,
                    )
                    return True

                return False
            except ValueError:
                return False

        return func

    def create_rbs(self) -> tuple[ttk.Frame, list[ttk.Radiobutton], tk.IntVar]:
        """Create the memory unit selection GUI elements."""
        units_rb_frame: ttk.Frame = ttk.Frame(self)
        rb_var: tk.IntVar = tk.IntVar(value=-1)

        label = ttk.Label(units_rb_frame, text="UNITS:")

        gb_rb = ttk.Radiobutton(
            units_rb_frame,
            command=self.convert_mem,
            text="GB",
            value=0,
            variable=rb_var,
        )
        mb_rb = ttk.Radiobutton(
            units_rb_frame,
            command=self.convert_mem,
            text="MB",
            value=1,
            variable=rb_var,
        )
        kb_rb = ttk.Radiobutton(
            units_rb_frame,
            command=self.convert_mem,
            text="KB",
            value=2,
            variable=rb_var,
        )
        label.pack(expand=True, side=tk.LEFT)
        gb_rb.pack(expand=True, fill=tk.X, side=tk.LEFT)
        mb_rb.pack(expand=True, fill=tk.X, side=tk.LEFT)
        kb_rb.pack(expand=True, fill=tk.X, side=tk.LEFT)

        return units_rb_frame, [gb_rb, mb_rb, kb_rb], rb_var

    def convert_mem(self) -> None:
        """Convert displayed units when unit changed."""
        conversion_factors = [1e6, 1e3, 1]
        mem = float(self.entry_var.get()) * conversion_factors[self.shadow_var]
        converted_mem = mem / conversion_factors[self.rb_var.get()]
        self.shadow_var = self.rb_var.get()
        self.entry_var.set(converted_mem)

    def organize(self) -> None:
        """Pack GUI elements."""
        self.entry.pack(expand=True, fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        self.units_rb_frame.pack(
            expand=True, fill=tk.X, padx=10, pady=10, side=tk.LEFT
        )

    def load(self) -> None:
        """Reload displayed memory and unit."""
        group = self.parent.group_cb.var.get()
        memory = self.parent.submission_parameters[group]["memory"]
        for rb in self.rbs:
            if rb["text"] == memory[1]:
                rb.invoke()
                break

        self.entry_var.set(memory[0])


class ParallelizationPanel(ttk.LabelFrame):
    """Specify parallelization parameters for jobs of the SubmissionGroup.

    Attributes:
        parent: The `JobSubmissionTab` in which the `ParallelizationPanel` is embedded.
        frames: A list of :class:`tkinter.ttk.Frame`s, containing GUI elements for node and core specificiations.
        sbs: A list of :class:`tkinter.Spinbox`es, for specifying nodes and cores.
        vars: A list of :class:`tkinter.IntVar`s, storing node and core specifications.
    """

    def __init__(self, parent: "JobSubmissionTab") -> None:
        """Initialize a `ParallelizatioPanel`.

        Args:
            parent: The `JobSubmissionTab` in which the `ParallelizationPanel` is embedded.
        """
        super().__init__(parent, text="Enter the parallelization parameters.")
        self.parent: JobSubmissionTab = parent
        self.frames, self.sbs, self.vars = self.create()

        self.organize()

    def create(
        self,
    ) -> tuple[list[ttk.Frame], list[tk.Spinbox], list[tk.IntVar]]:
        """Create `Frame`, `Spinbox`, and `IntVar` lists."""
        labels = ["nodes", "cores"]
        upper_limits = [100, 600]
        frames: list[ttk.Frame] = []
        sb_vars: list[tk.StringVar] = []
        sbs: list[tk.Spinbox] = []
        group = self.parent.group_cb.var.get()

        for i, key_text in enumerate(labels):
            frame = ttk.Frame(self)
            label_text = (
                key_text if key_text == "nodes" else key_text + " per node"
            )
            label = ttk.Label(frame, text=f"number of {label_text}")
            var = tk.IntVar(
                value=self.parent.submission_parameters[group][key_text]
            )
            sb = tk.Spinbox(
                frame,
                command=self.update_parallelization,
                from_=1,
                state="readonly",
                textvariable=var,
                to=upper_limits[i],
            )

            label.pack(side=tk.LEFT)
            sb.pack(side=tk.LEFT)

            frames.append(frame)
            sb_vars.append(var)
            sbs.append(sb)

        return frames, sbs, sb_vars

    def update_parallelization(self) -> None:
        """Update the parallelization parameters with the displayed values."""
        group = self.parent.group_cb.var.get()

        nodes = int(self.vars[0].get())
        self.parent.submission_parameters[group]["nodes"] = nodes

        cores = int(self.vars[1].get())
        self.parent.submission_parameters[group]["cores"] = cores

        self.parent.panels["part_panel"].enforce_partition_limits()

    def organize(self) -> None:
        """Pack frames."""
        for frame in self.frames:
            frame.pack(expand=True, fill=tk.Y, side=tk.LEFT)

    def load(self) -> None:
        """Load displayed parameters from stored values."""
        group = self.parent.group_cb.var.get()

        nodes = self.parent.submission_parameters[group]["nodes"]
        self.vars[0].set(nodes)

        cores = self.parent.submission_parameters[group]["cores"]
        self.vars[1].set(cores)


class PartitionPanel(ttk.LabelFrame):
    """Specify partitions for jobs of the SubmissionGroup.

    Attributes:
        parent: The `JobSubmissionTab` in which the `PartitionPanel` is embedded.
        partitions: The list of the selected partitions.
        partition_cb: The :class:`tkinter.Combobox` for selecting partitions to add.
        button_frame: The :class:`tkinter.ttk.Frame` containing buttons to add, clear
            and remove partitions.
        listbox: The :class:`tkinter.Listbox` for displaying the selected
        yscroll: The :class:`tkinter.ttk.Scrollbar` for manipulating the `Listbox`.
        list_var: The :class:`tkinter.StringVar` storing the contents of the `Listbox`.
    """

    def __init__(self, parent: "JobSubmissionTab"):
        """Initialize a `PartitionPanel`.

        Args:
            parent: The `JobSubmissionTab` in which the `PartitionPanel` is embedded.
        """
        super().__init__(parent, text="Specify the partitions for the job.")
        self.parent: JobSubmissionTab = parent

        self.partitions: list[hpc.Partition] = self.load_partitions()
        self.partition_cb, self.cb_var = self.create_combobox()
        self.button_frame: ttk.Frame = self.create_button_frame()
        self.listbox, self.yscroll, self.list_var = self.create_listbox()

        self.organize()

    def load_partitions(self) -> list[hpc.Partition]:
        """Returns the list of partitions from which to select."""
        partitions = []
        for partition in hpc.ARC_PARTITIONS:
            partitions.append(partition)

        return partitions

    def create_combobox(self) -> tuple[ttk.Combobox, tk.StringVar]:
        """Returns the selection `Combobox` and `StringVar` as a 2-tuple."""
        partitions = [p.cluster_name for p in self.partitions]

        text_var = tk.StringVar()
        partition_cb: ttk.Combobox = ttk.Combobox(
            self, state="readonly", textvariable=text_var, values=partitions
        )

        return partition_cb, text_var

    def create_button_frame(self) -> ttk.Frame:
        """Creates and returns the button frame."""
        background = ttk.Style().lookup("TFrame", "background")
        style: ttk.Style = ttk.Style()
        style.configure("button.TFrame", background=background)
        subframe = ttk.Frame(self, style="button.TFrame")

        add_cmd = self.add_partitions
        add_button = ttk.Button(subframe, text="add", command=add_cmd, width=5)

        rm_cmd = self.remove_partitions

        rm_button = ttk.Button(
            subframe, text="remove", command=rm_cmd, width=5
        )

        clr_cmd = self.clear_partitions

        clr_button = ttk.Button(
            subframe, text="clear", command=clr_cmd, width=5
        )

        add_button.grid(column=0, padx=5, pady=10, row=0)
        rm_button.grid(column=0, padx=5, pady=10, row=1)
        clr_button.grid(column=0, padx=5, pady=10, row=2)

        subframe.rowconfigure(0, weight=1)
        subframe.rowconfigure(1, weight=1)
        subframe.rowconfigure(2, weight=1)

        return subframe

    def create_listbox(self) -> tuple[tk.Listbox, tk.StringVar]:
        """Returns the `Listbox` and `StringVar` as a 2-tuple."""
        list_var = tk.StringVar()
        yscroll = ttk.Scrollbar(self)
        listbox: tk.Listbox = tk.Listbox(
            self,
            height=5,
            listvariable=list_var,
            selectmode=tk.EXTENDED,
            yscrollcommand=yscroll.set,
        )

        return listbox, yscroll, list_var

    def add_partitions(self) -> None:
        """Validates parameter values and adds new values.

        Duplicates are removed and the entries in the tk.Listbox are
        sorted.
        """
        group = self.parent.group_cb.var.get()
        partitions = set(
            self.parent.submission_parameters[group]["partitions"]
        )
        partitions.add(self.cb_var.get())
        partitions = validation.alphanum_sort(list(partitions))

        self.parent.submission_parameters[group]["partitions"] = partitions
        self.load()

    def remove_partitions(self) -> None:
        """Removes selected partitions."""
        selected = self.listbox.curselection()

        copy = self.listbox.get(0, self.listbox.size() - 1)

        new_values = []

        for i, partition in enumerate(copy):
            if i not in selected:
                new_values.append(partition)

        self.listbox.delete(0, self.listbox.size() - 1)

        for value in new_values:
            self.listbox.insert(tk.END, value)

    def clear_partitions(self) -> None:
        """Remove all partitions from the `Listbox`."""
        self.listbox.delete(0, self.listbox.size() - 1)

    def organize(self) -> None:
        """Pack frames."""
        self.partition_cb.pack(fill=tk.X, side=tk.LEFT)
        self.button_frame.pack(fill=tk.Y, side=tk.LEFT)
        self.listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        self.yscroll.pack(expand=True, fill=tk.Y)

    def enforce_partition_limits(self) -> None:
        """Update partitions available for selection.

        This method populates the list of partitions available for selection
        using the values of the submission parameters and the properties
        of the available partitions.
        """
        days = int(self.parent.panels["rt_panel"].vars[0].get())
        hours = int(self.parent.panels["rt_panel"].vars[1].get())
        mins = int(self.parent.panels["rt_panel"].vars[2].get())
        time_req = days * 24 * 60 + hours * 60 + mins

        mem_req = validation.val_to_native(
            self.parent.panels["mem_panel"].entry_var.get()
        )
        nodes_req = int(self.parent.panels["para_panel"].vars[0].get())
        cores_req = int(self.parent.panels["para_panel"].vars[1].get())

        # Convert memory to KB
        if self.parent.panels["mem_panel"].rb_var.get() == 0:
            mem_req *= 1e6
        elif self.parent.panels["mem_panel"].rb_var.get() == 1:
            mem_req *= 1e3

        # Filter partitions according to resource request
        suitable_partitions: list[str] = []

        for partition in self.partitions:
            time_limit = partition.time_limit
            max_mem_per_node = partition.max_mem_per_node
            nodes = partition.nodes
            cpus_per_node = partition.cpus_per_node

            if (
                time_req <= time_limit
                and mem_req <= max_mem_per_node
                and nodes_req <= nodes
                and cores_req <= cpus_per_node
            ):
                suitable_partitions.append(partition.cluster_name)

        self.partition_cb.configure(values=suitable_partitions)

        self.format_partitions(suitable_partitions)

    def format_partitions(self, suitable_partitions: list[str]) -> None:
        """Format the selected partitions based on request suitability.

        Suitable partitions are formatted in white text. Unsuitable
        partitions are formatted in red text.

        Args:
            suitable_partitions: The list of partitions that are suitable
                given the present resource request.
        """
        for i in range(self.listbox.size()):
            if self.listbox.get(i) not in suitable_partitions:
                self.listbox.itemconfig(
                    i, foreground="red", selectforeground="red"
                )
            else:
                self.listbox.itemconfig(
                    i, foreground="white", selectforeground="white"
                )

    def load(self) -> None:
        """Load the displayed partitions based on the SubmissionGroup."""
        group = self.parent.group_cb.var.get()
        lb_vals = self.parent.submission_parameters[group]["partitions"]

        self.listbox.delete(0, self.listbox.size() - 1)

        for val in lb_vals:
            self.listbox.insert(tk.END, val)


class AutoRestartPanel(ttk.LabelFrame):
    """Specify auto-restart options.

    Attributes:
        parent: The `JobSubmissionTab` in which the `AutoRestartPanel` resides.
        frame1: The :class:`tkinter.ttk.Frame` containing the unlimited
            auto-restart prompt.
        label1: The :class:`tkinter.ttk.Label` containing the prompt for
            unlimited auto-restart.
        rbs: A list of `Radiobutton`s indicating the choice for unlimited
            auto-restart.
        rb_var: An :class:`tkinter.IntVar` indicating which selection the user
            has made. 0 if user has selected unlimited auto-restart, 1
                otherwise.
        frame2: The :class:`tkinter.ttk.Frame` for specifying the auto-restart
            limit.
        label2: The :class:`tkinter.ttk.Label` containing the prompt for
            setting the auto-restart limit.
        sb: A :class:`tkinter.Spinbox` for specifying the auto-restart limit.
        sb_var: An :class:`tkinter.IntVar` storing the value of the
            auto-restart limit.
    """

    def __init__(self, parent: "JobSubmissionTab") -> None:
        """Initialize an `AutoRestartPanel`.

        Args:
            parent: The `JobSubmissionTab` in which the `AutoRestartPanel` resides.
        """
        super().__init__(parent, text="Specify the auto-restart options.")
        self.parent: JobSubmissionTab = parent

        (
            self.frame1,
            self.label1,
            self.rbs,
            self.rb_var,
        ) = self.create_unlimited_restart_prompt()

        (
            self.frame2,
            self.label2,
            self.sb,
            self.sb_var,
        ) = self.create_auto_restart_limit()

        self.organize()

    def create_unlimited_restart_prompt(
        self,
    ) -> tuple[ttk.Frame, ttk.Label, list[ttk.Radiobutton], tk.IntVar]:
        """Create the panel for selecting unlimited auto-restart.

        Returns:
            A tuple (`frame`, `label`, `rbs`, `rb_var`) where `frame` is the
            Frame containing the radio buttons, `label` contains the
            auto-restart text prompt, `rbs` is a list of `Radiobutton`s which
            set unlimited auto-restart, and `rb_var` is the `IntVar`
            indicating which radiobutton is selected.
        """
        frame = ttk.Frame(self)
        label = ttk.Label(frame, text="Unlimited auto-restart?")

        rb_var = tk.IntVar(value=0)
        yes_rb = ttk.Radiobutton(
            frame,
            command=self.display_autorestart_options,
            text="Yes",
            value=0,
            variable=rb_var,
        )
        no_rb = ttk.Radiobutton(
            frame,
            command=self.display_autorestart_options,
            text="No",
            value=1,
            variable=rb_var,
        )
        label.pack(padx=10, pady=10, side=tk.LEFT)
        yes_rb.pack(expand=True, padx=10, pady=10, side=tk.LEFT)
        no_rb.pack(expand=True, padx=10, pady=10, side=tk.LEFT)

        return frame, label, [yes_rb, no_rb], rb_var

    def display_autorestart_options(self) -> None:
        """Toggle display of restart limit selection."""
        group = self.parent.group_cb.var.get()
        if self.rb_var.get() == 0:
            self.label2.pack_forget()
            self.sb.pack_forget()
            self.parent.submission_parameters[group]["restart limit"] = None
        else:
            self.label2.pack(padx=10, pady=10, side=tk.LEFT)
            self.sb.pack(padx=10, pady=10, side=tk.LEFT)
            limit = self.sb_var.get()
            self.parent.submission_parameters[group]["restart limit"] = limit

    def create_auto_restart_limit(
        self,
    ) -> tuple[ttk.Frame, ttk.Label, tk.IntVar]:
        """Create restart limit elements."""
        frame = ttk.Frame(self)
        label = ttk.Label(frame, text="Select auto-restart limit:")
        sb_var = tk.IntVar()
        sb = tk.Spinbox(
            frame,
            command=self.update_limit,
            from_=0,
            state="readonly",
            textvariable=sb_var,
            to=50,
        )

        label.pack(padx=10, pady=10, side=tk.LEFT)
        sb.pack(padx=10, pady=10, side=tk.LEFT)

        return frame, label, sb, sb_var

    def update_limit(self) -> bool:
        """Update the stored restart limit. Returns True."""
        group = self.parent.group_cb.var.get()
        limit = int(self.sb_var.get())
        self.parent.submission_parameters[group]["restart limit"] = limit

        return True

    def organize(self) -> None:
        """Pack frames."""
        self.frame1.pack(
            expand=True, fill=tk.X, padx=10, pady=10, side=tk.LEFT
        )
        self.frame2.pack(
            expand=True, fill=tk.X, padx=10, pady=10, side=tk.LEFT
        )

    def load(self) -> None:
        """Display the stored auto-restart specification."""
        group = self.parent.group_cb.var.get()
        limit = self.parent.submission_parameters[group]["restart limit"]
        if limit is None:
            self.rbs[0].invoke()
        else:
            self.sb_var.set(limit)
            self.rbs[1].invoke()


class ExtrasPanel(ttk.LabelFrame):
    """Specify additonal SLURM options.

    Atributes:
        parent: The `JobSubmissionTab` in which the `ExtrasPanel` resides.
        account: The :class:`tkinter.StringVar` storing the value of the
            `--account` option.
        mail_type: The :class:`tkinter.StringVar` storing the value of the
            `--mail-type` option.
        mail_user: The :class:`tkinter.StringVar` storing the value of the
            `--mail-user` option.
    """

    def __init__(self, parent: "JobSubmissionTab") -> None:
        """Initialize a `ExtrasPanel`.

        Args:
            parent: The `JobSubmissionTab` in which the `ExtrasPanel` resides.
        """
        self.parent = parent
        super().__init__(parent, text="Specify additional SLURM options")

        # Add labels and entries for mail type and mail user with validation
        def _update_account(value: str) -> bool:
            group = self.parent.group_cb.var.get()
            self.parent.submission_parameters[group]["account"] = value
            return True

        self.account = tk.StringVar()
        account_label = ttk.LabelFrame(self, text="account")
        account_cmd = self.register(_update_account)
        account_entry = ttk.Entry(
            account_label,
            textvariable=self.account,
            validate="focusout",
            validatecommand=(account_cmd, "%P"),
        )
        account_entry.pack(expand=True, fill="both", side="left")
        account_label.grid(column=0, row=0)

        def _update_mail_type(value: str) -> bool:
            group = self.parent.group_cb.var.get()
            self.parent.submission_parameters[group]["mail-type"] = value
            return True

        self.mail_type = tk.StringVar()
        mail_type_label = ttk.LabelFrame(self, text="mail-type")
        mail_type_cmd = self.register(_update_mail_type)
        mail_type_entry = ttk.Entry(
            mail_type_label,
            textvariable=self.mail_type,
            validate="focusout",
            validatecommand=(mail_type_cmd, "%P"),
        )
        mail_type_entry.pack(expand=True, fill="both", side="left")
        mail_type_label.grid(column=1, row=0)

        def _update_mail_user(value: str) -> bool:
            group = self.parent.group_cb.var.get()
            self.parent.submission_parameters[group]["mail-user"] = value
            return True

        self.mail_user = tk.StringVar()
        mail_user_label = ttk.LabelFrame(self, text="mail-user")
        mail_user_cmd = self.register(_update_mail_user)
        mail_user_entry = ttk.Entry(
            mail_user_label,
            textvariable=self.mail_user,
            validate="focusout",
            validatecommand=(mail_user_cmd, "%P"),
        )
        mail_user_entry.pack(expand=True, fill="both", side="left")
        mail_user_label.grid(column=2, row=0)

    def load(self) -> None:
        "Load the values of the displayed mail notification options."
        group = self.parent.group_cb.var.get()
        mail_type = self.parent.submission_parameters[group]["mail-type"]
        mail_user = self.parent.submission_parameters[group]["mail-user"]
        self.mail_type.set(mail_type)
        self.mail_user.set(mail_user)


class JobSubmissionPanels(TypedDict):
    """The `JobSubmissionTab` panels."""

    rt_panel: RunTimePanel
    mem_panel: MemoryPanel
    para_panel: ParallelizationPanel
    part_panel: PartitionPanel
    ar_panel: AutoRestartPanel
    mail_panel: ExtrasPanel


class JobSubmissionTab(ttk.Frame):
    """Specify submission parameters for a SubmissionGroup.

    Attributes:
        parent: The :class:`tkinter.ttkNotebook` in which the `JobSubmissionTab` resides.
        app: The root :class:`.coordinator.gui.GUI`.
        groub_cb: The `GroupSelectionCombobox` for selecting a group.
        panels: A dictionary mapping panel names to the various frames
            used to set submission parameters.
    """

    def __init__(self, main_app: ttk.Notebook) -> None:
        """Initialize the job submission tab.

        Args:
            main_app: The :class:`tkinter.ttkNotebook` in which the `JobSubmissionTab` resides.
        """
        super().__init__(main_app.notebook)

        self.parent: ttk.Notebook = main_app.notebook
        self.app: gui.GUI = main_app

        self._submission_parameters = self.initialize_submission_parameters()

        self.group_cb = GroupSelectionCombobox(self)

        self.panels: JobSubmissionPanels = {}

        self.group_cb.grid(column=0, pady=10, row=0)
        self.columnconfigure(0, weight=1)

    def initialize_submission_parameters(self) -> dict[str, dict]:
        """Create the submission group dictionary.

        Returns:
            A dictionary mapping submission parameter group names to
            dictionaries of submissionn parameters.
        """
        groups = list(self.app.coordinator.submission_parameter_groups)

        params: dict[str, dict | int | list | None | tuple] = {}

        for group in validation.alphanum_sort(groups):
            params[group] = self.new_submission_parameters()

        return params

    def new_submission_parameters(
        self,
    ) -> dict[str, dict | int | list | None]:
        """Create a default set of submission parameters."""
        parameters: dict[str, dict | int | list | None] = {}

        parameters["run time"] = {"days": 0, "hours": 0, "minutes": 0}
        parameters["memory"] = (0, "GB")
        parameters["nodes"] = 1
        parameters["cores"] = 1
        parameters["partitions"] = []
        parameters["restart limit"] = None
        parameters["account"] = None
        parameters["mail-type"] = "BEGIN,END,FAIL,TIME_LIMIT,TIME_LIMIT_90"
        parameters["mail-user"] = None

        return parameters

    def update_panels(self) -> None:
        """Load each of the panels in the `JobSubmissionTab`."""
        if self.panels:
            for panel in self.panels.values():
                panel.load()
        else:
            self.create_panels()
            self.update_panels()
            self.pack_panels()

    def create_panels(self) -> None:
        """Create all panels."""
        self.panels["rt_panel"] = RunTimePanel(self)
        self.panels["mem_panel"] = MemoryPanel(self)
        self.panels["para_panel"] = ParallelizationPanel(self)
        self.panels["part_panel"] = PartitionPanel(self)
        self.panels["ar_panel"] = AutoRestartPanel(self)
        self.panels["mail_panel"] = ExtrasPanel(self)

    def remove_panels(self) -> None:
        """Remove all panels."""
        if self.panels:
            for panel in self.panels.values():
                panel.destroy()

        self.panels = {}

    def pack_panels(self) -> None:
        """Pack frames."""
        i = 1
        for key in iter(self.panels):
            self.panels[key].grid(column=0, pady=10, row=i, sticky=tk.W + tk.E)
            i += 1

    def partition_enforcement(self) -> None:
        """Enforce partition capabilities."""
        for sb in self.panels["rt_panel"].sbs:
            sb.configure(command=self.panels["rt_panel"].enforce_time_limit)

        mem_panel = self.panels["mem_panel"]
        cmd = mem_panel.register(mem_panel.validate_memory())
        mem_panel.entry.configure(validatecommand=(cmd, "%P"))

        para_panel = self.panels["para_panel"]

        for sb in para_panel.sbs:
            sb.configure(command=para_panel.update_parallelization)

    @property
    def submission_parameters(
        self,
    ) -> dict[str, dict[str, dict | float | int | str | tuple]]:
        """The submission parameters of each submission parameter group."""
        return self._submission_parameters.copy()

    @submission_parameters.setter
    def submission_parameters(
        self,
        new_submission_parameters: dict[
            str, dict[str, dict | float | int | str | tuple]
        ],
    ):
        """Set the submission parameter group and reload."""
        self._submission_parameters = new_submission_parameters
        self.load()

    def update_parameters(self) -> None:
        """Update the stored submission parameters from the selected values."""
        old_groups = self.submission_parameters
        new_groups = list(self.app.coordinator.submission_parameter_groups)

        for group in iter(old_groups):
            if group not in new_groups:
                del self._submission_parameters[group]

        for group in new_groups:
            if group not in old_groups:
                self._submission_parameters[group] = (
                    self.new_submission_parameters()
                )

    def load(self) -> None:
        """Reload the displayed parameters based on the stored values."""
        self.update_parameters()

        self.group_cb.load()

        if self.group_cb.var.get() != "":
            self.update_panels()
            self.partition_enforcement()
        else:
            self.remove_panels()
