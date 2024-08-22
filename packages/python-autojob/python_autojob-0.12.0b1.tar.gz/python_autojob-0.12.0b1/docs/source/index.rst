.. autojob documentation master file, created by
   sphinx-quickstart on Tue Jan 23 10:25:50 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/autojob_dark.png
   :align: center

Welcome to autojob's documentation!
===================================

.. include:: ../../README.rst
    :start-after: .. start elevator-pitch
    :end-before: .. end elevator-pitch

* |Getting Started|_: what you need and how to install ``autojob``
* |Introduction|_: an overview of ``autojob``'s features
* |API Documentation|_: API for all of ``autojob``'s packages, modules, and
  CLI functions

.. |Getting Started| replace:: **Getting Started**
.. _Getting Started: :doc:`quickstart`
.. |Introduction| replace:: **Introduction**
.. _Introduction: :doc:`usage/basicusage`
.. |API Documentation| replace:: **API Documentation**
.. _API Documentation: :doc:`reference/modules`

.. toctree::
   :caption: Quickstart 🚀
   :maxdepth: 1
   :hidden:

   quickstart

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:

   usage/basicusage
   Configuration 🎨 <usage/configuration>
   usage/directory
   usage/task
   usage/coordinator
   usage/advance
   usage/harvest

.. toctree::
   :maxdepth: 2
   :caption: API Documentation
   :glob:
   :hidden:

   reference/modules
   Command-Line Interface <reference/commandline>

.. toctree::
   :maxdepth: 2
   :caption: Task Library
   :glob:
   :hidden:

   library/actions
   library/tasks
   library/workflows

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide
   :hidden:

   devguide/contributing
   devguide/docs
   devguide/extending

.. toctree::
   :maxdepth: 2
   :caption: About
   :hidden:

   Changelog 🔮 <about/changelog>
   License <about/license>
