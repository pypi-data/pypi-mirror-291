Extending autojob
-----------------

autojob is designed to facilitate extension to fit your niche needs. This page outlines what is needed in order to ensure that your extension fits nicely into
the autojob ecosystem. In particular, this document covers how to extend the following constructs:

- Task

- Calculation

Task
====

Writing your own ``Task`` requires implementation of

``from_directory``

If you intend to override :meth:`Task.from_directory` in your subclass,
be careful calling :meth:`Task.from_directory` with ``magic_mode = True``. Since this
parameter may result in an infinite loop. If you are going to support calling
``from_directory`` with ``magic_mode = True`` considering starting your
function with the following if block:

.. code-block:: python

    def func():
        builder = TaskMetadata.from_directory(dir_name)._build_class
        if magic_mode:
            return cls.load_magic(dir_name, builder)

This ensures that the loading is deferred to the appropriate subclass and avoids the
temptation of passing ``magic_mode``. Note that if you were to construct your override
in this way:

.. code-block:: python

    ...
    task = Task.from_directory(dir_name, strict_mode, magic_mode)
    # do patching here
    ...

Then, if ``_build_class`` is set in the metadata file, you will effectively call your
code twice!

Calculation
===========

Useful points for customization:

- ``Calculation.write_python_script``: Define a new template file

- ``Calculation.prepare_input_atoms``: Define preparation steps in addition to
  copying magnetic moments or freeze non-adsorbate atoms.

- ``Calculation.get_output_atoms``: This function should return an
  :class:`~ase.Atoms` object :class:`Path` that represents the directory of the
  calculation

- ``Calculation.load_calculation_outputs``: This function should return a
  dictionary that maps outputs (string keys) to their values when passed a
  :class:`Path` that represents the directory of the calculation

- ``FILES_TO_CARRYOVER``: This should be a module-level
    constant which defines the files from a previous
    calculation to carry-over to a new job. Usually, this
    is the checkpoint-type file employed by the calculation
    software.
