Configuration
==============

Directory Structure
-------------------

``autojob`` supports two directory structures. The first structure exists for
backwards-compatibility and will be phased out and is as follows:

- Study Group

  - ``study_group.json``

  - Study

    - ``parameterizations.json``

    - ``record.txt``

    - ``study.json``

    - ``workflow.json``

    - Calculation

      - ``calculation.json``

      - Job

        - ``job.json``

Here, a "Job" is the atomic unit and corresponds roughly to a job submission in a job scheduler. A "Calculation" is then the ultimate goal of the initial submission (e.g., structure relaxation, adsorption calculation, etc.). The motivation for this structure stems from the early use of autojob as solely a way of parametrizing VASP calculations. As such, since calculations would frequently require restarting-whether due to time limit constraints, VASP errors, or parametrization optimization-grouping each "Job"
under a "Calculation" made it easy to navigate to previous iterations of the "Calculation", restart jobs, and retrace one's steps. The ``calculation.json`` file served as a record of all jobs.

For other computational chemistry tasks, however, (e.g., slab generation, adsorbate placement, etc.), the additional nested structure adds unnecessary complexity. Furthermore, the linking of jobs can be achieved by simply retaining a unique identifier analogous to the calculation ID that links jobs. These factors led to the conception of the second supported directory structure.

The second supported directory structure takes the form:

- Study Group

  - ``study_group.json``

  - Study

    - ``parameterizations.json``

    - ``record.txt``

    - ``study.json``

    - ``workflow.json``

    - Task

      - ``task.json``

In the future, the top-level directory may be foregone such that the final supported directory structure may take the form:

- Study

  - ``parameterizations.json``

  - ``record.txt``

  - ``study.json``

  - ``workflow.json``

  - Task

    - ``task.json``

Data Files
----------

Study Files
^^^^^^^^^^^

``parameterizations.json``

- a dictionary mapping a workflow step ID to a :class:`~autojob.workflow.Step`

``record.txt``

- a text file in which each line lists a task ID of a completed task

``study.json``

- contains metadata about the study (e.g., Study Group ID, Study ID, Study
  Type, Date Created) and a list of calculation IDs (or task IDs) of
  calculations (or tasks) belonging to the Study

``workflow.json``

- a dictionary mapping a workflow step ID to a list of workflow step IDs

- a directed acyclic graph representing the study's workflow

Task Files
^^^^^^^^^^

``run.py``

- a python script containing the logic for executing the task

- can be set with the ``--python-script`` CLI argument for ``autojob`` or the
  ``AUTOJOB_PYTHON_SCRIPT`` environment variable

- Requirements:

  - The structure of the script must match that of the template file

  - Minimal, notable features of the template file:

    - ASE calculator imported

    - structure file read using ase.io.read

    - the ASE calculator configuration format

``vasp.sh``

- a Bash script containing the logic from running the computing job

- can be set with the ``--slurm-script`` CLI argument for ``autojob`` or the
    ``AUTOJOB_SLURM_SCRIPT`` environment variable

- Requirements:

  - The structure of the script must match that of the template file

  - Minimal, notable features of the template file:

    - SLURM configuration directives

    - files to delete

    - files to copy

``job.json``

- a JSON-serialized dictionary of task metadata

- can be set with the ``--job-file`` CLI argument for ``autojob`` or the
  ``AUTOJOB_JOB_FILE`` environment variable

- Generally, this should not be directly edited but should be modified
  indirectly when a new job is created by any one of the utility functions
  (e.g., :func:`~.advance.advance`, :func:`~.relaxationrestart_relaxation`,
  :func:`~.vibration.create_vibration`)

``task.json``

- a JSON-serialized dictionary summarizing a completed task

Legacy Files
^^^^^^^^^^^^

``calculation.json``

- a JSON-serialized dictionary of calculation metadata

- can be set with the ``--calculation-file`` CLI argument for ``autojob`` or
  the ``AUTOJOB_CALCULATION_FILE`` environment variable

- Generally, this should not be directly edited but should be modified
  indirectly when a new job is created by any one of the utility functions
  (e.g., :func:`~.advance.advance`, :func:`~.relaxationrestart_relaxation`,
  :func:`~.vibration.create_vibration`)
