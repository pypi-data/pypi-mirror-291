Using ``autojob coordinator``
=============================

Example: Build a Mechanistic Study (WIP)
----------------------------------------

This document summarizes the requirements for successfully using the CLI command ``autojob coordinator``. This tutorial will demonstrate how to
design, parametrize, and execute a mechanistic study workflow.

1. Name and describe our study on the "Study Design" page.

   (animated screen grab of typing study group name and description)

2. Select "Mechanistic Study" from "Study Templates"

3. Click "Next"

4. Parametrize the mechanistic study. The following parameters can be modified:

   **structures**
     specify structures - the mechanistic study will be performed
     for each structure

   **adsorbates**
     specify each adsorbate that will be placed on each structure
     or select from a list of presets which correspond to common mechanisms
     (e.g., nitrate reduction reaction, oxygen reduction reaction, etc.);
     learn how to extend this list here

   **finder**
     specify how to identify adsorption sites (by tag, by file metadata, by
     Python function)

   Specifying multiple values of a parameter instructs ``autojob`` to create a
   task for each combination of that value and the other parameters.

5. Parametrize the constituent tasks within the mechanistic study.

   * calculator: the ASE calculator to use to run the calculation

   * other parameters: calculator-specific parameters such as kpts and encut
     for VASP or scf and chk for Gaussian

6. Specify submission parameters for tasks.

   * group tasks by parameter

   * parametrize tasks with respect to submission parameters

7. View "Study Summary" page to see total number of steps, list of all tasks,
   and study metadata.

8. Execute workflow.
