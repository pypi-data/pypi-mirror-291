Basic Usage
==============

``autojob`` has two main functions

1. coordinator - GUI-based calculation and workflow design

2. advance/step - Semi-automatic workflow management framework

``coordinator``
---------------

``coordinator`` is a codeless interface for computational chemistry study design,
management, and parallelization.

Study Design
^^^^^^^^^^^^

Study design begins on the "Study Design" page where you optionally name and
describe your study.

(code screenshot of "Study Design" page)

Useful definitions:

**Study**
  A study is a collection of workflows.

**Workflow**
  A workflow is a directed acyclic graph of actions and tasks.

**Action**
  An action is a locally run step in a workflow such as
  determining all non-equivalent adsorption sites on a metal surface or
  permuting a defect within a structure.

**Task**
  A task is an atomic compute job that may be submitted to a
  scheduler. Tasks often require parallelization and submission to a workload
  manager such as Slurm. Examples of tasks include single-point calculations,
  relaxation calculations, and ab-initio molecular dynamics calculations.

Next, you build a study by either selecting from a list of presets (learn how
to extend this list here) or stitching together tasks, workflows, and actions.

Task Configuration
^^^^^^^^^^^^^^^^^^

A "task" represents an atomic compute job that may be submitted to a scheduler. Tasks often
require parallelization and submission to a workload manager such as Slurm.

The following tasks are pre-defined in autojob:

* relaxation
* vibrational calculation
* infrared frequency calculation

On the "Task Configuration" page, you can change the parameters used to
execute a given task. If the parameter can be defined via a file, you will have the
option of specifying a value, selecting a file, or specifying a file
that must be present at runtime by path.

(screen grab of Task Configuration panel)
