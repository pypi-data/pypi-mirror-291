Using ``autojob advance``
=========================

Assumptions About Workflow Structure
------------------------------------

- Only the first step can fail and be restarted (see
  :func:`autojob.advance.advance.get_next_steps`)

- Tasks without a workflow step ID are assumed to be the first of a
  single-predecessor, 2-step workflow

- Only independently connected workflows with single-source
  :class:`~.workflow.VariableReference`'s are supported at the moment

- In legacy mode, it is assumed that if the task metadata file does not
  contain the workflow step ID, the corresponding task is the first step in
  the workflow

- Due to the current implementation the first step in the workflow must have
  exactly one parametrization in order for restarting to work

Utility Functions
-----------------

For convenience, more granular, step-wise control and customization of workflows can be achieved using ``autojob step`` subcommands (e.g.,
``relaxation``, ``vibration``) which correspond to :class:`Calculation <autojob.calculation.calculation.Calculation>` subclasses.

If one desires to control workflow progression by oneself, these subcommands
can be used to create arbitrary calculations from a completed calculation
directory. For example, ``autojob advance`` will exit with a non-zero exit code
and not advance if an ``autojob.stop`` file is found in the directory in which
it is run. Thus, if a change must be made to parameters prior to a successive
run or if the trajectory of a workflow must be changed, one can place such a
file, then make modifications as desired.

Each CLI command accepts the following CLI options:

- ``--calc-mods``

- ``--slurm-mods``

- ``--verbose``

- ``--log-file``

Note that the aforementioned CLI commands also serve the use-case where one wantes to manually manage an entire workflow.
