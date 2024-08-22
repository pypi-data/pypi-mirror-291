========
Overview
========

.. start elevator-pitch

``autojob`` is a (semi-)automatic framework for DFT job automation on massively parallel
computing resources. With ``autojob``, you can manage complex, automated workflows while
still retaining the flexibility to stop, make job-level changes, and resume the workflow.

.. end elevator-pitch

.. image:: docs/source/_static/autojob_light.png
   :align: center

.. start quickstart

Requirements
============

``autojob`` requires the following dependencies:

* Python 3.11+
* ase
* numpy
* scipy
* ccu
* emmet
* monty
* shortuuid
* pymatgen
* click
* Jinja2
* pydantic
* pydantic-settings
* cclib

Installation 🛠️
===============

(WIP)

``autojob`` can be installed via ``pip``:

.. code-block:: shell

    pip install python-autojob

You can also install the in-development version with ssh:

.. code-block:: shell

    pip install git+ssh://git@gitlab.com/ugognw/python-autojob.git@development"

or https

.. code-block:: shell

    pip install git+https://gitlab.com/ugognw/python-autojob.git

.. end quickstart

Documentation
=============

https://python-autojob.readthedocs.io/
