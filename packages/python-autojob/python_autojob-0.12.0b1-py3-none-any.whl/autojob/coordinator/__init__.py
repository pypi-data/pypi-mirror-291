"""Coordinate the creation of study groups.

This subpackage provides utilities for the creation of study groups.
The :mod:`autojob.coordinator` module is especially useful for parametrizing
calculations en masse. The ``Coordinator`` GUI can be launched
programmatically with the :func:`.gui.run` function

.. code-block:: python

    from autojob.coordinator.gui import gui

    gui.run()

or from the command line with the ``autojob coordinator`` CLI command

.. code-block:: console

    autojob coordinator
"""
