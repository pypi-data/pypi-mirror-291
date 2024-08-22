
How ``autojob`` structures directories 💭
=========================================

This document summarizes the requirements for successfully using the CLI command ``autojob advance``

Workflow
--------

To use ``autojob advance`` navigate to a task directory of a directory tree with
either one of the supported directory structures.

.. _legacy-vs-normal:

Legacy vs. Normal Mode
----------------------

Legacy mode describes a set of differences in the data model, directory
structure, and metadata in ``autojob``. These differences derive from the first
use-case: a VASP relaxation calculation of an adsorbate complex followed by a
vibrational calculation to determine the Gibbs free energy.

Legacy Mode
~~~~~~~~~~~

In legacy mode, directory trees must adhere to the first structure outlined in
setup.

Task (Job) Metadata

- required keys:

  - Name

  - Notes

  - Study Group ID

  - Study ID

  - Calculation ID

  - Job ID

  - Study Type

  - Calculation Type

  - Calculator Type

Normal Mode
~~~~~~~~~~~

Task Metadata
- the result of ``json.dumps(Task.model_dump(by_alias=True, exclude_none=True), indent=4)``


Directory Structure
-------------------

You must be in the bottom-level directory (task or job directory) of a directory tree with either of the two supported directory structures (see setup)

Files
-----

The following files must be present in the study root directory:

- ``study.json``

- ``record.txt``

- ``parametrizations.json``

- ``workflow.json``

The following files must be present in the bottom-level directory:

- ``job.json`` (or ``task.json`` for non-legacy mode)

- ``run.py`` (or some python script whose generic name-this must be common
    to all jobs in a study-is stored as SETTINGS.PYTHON_SCRIPT. This can
    be passed as a CLI argument to ``autojob`` or set as an environment
    variable: ``AUTOJOB_PYTHON_SCRIPT``) # TODO
