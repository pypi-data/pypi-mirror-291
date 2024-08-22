
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on
`Keep a Changelog`_.

Starting with version 0.12.0, this project implements a version of
`Semantic Versioning`_ described
`here <https://iscinumpy.dev/post/bound-version-constraints/#semver>`_ called
"Realistic" Semantic Versioning.

`Unreleased`_
-------------

Added
~~~~~

* ``LORBIT`` Vasp INCAR tag to :mod:`autojob.coordinator.vasp`

* support for Gaussian-powered calculations

* support for custom Python script templates

* default template for infrared calculations

* New modules:

  * :mod:`autojob.utils`

  * :mod:`autojob.advance`: incremental job control

  * :mod:`autojob.harvest`: data assimilation convenience functions & CLI

    * :mod:`autojob.harvest.harvest`: utilities for harvesting task data

    * :mod:`autojob.harvest.patch`: utilities for patching task data

  * :mod:`autojob.cli.restart_relaxation`,
    :mod:`autojob.next.relaxation` and corresponding CLI command
    `restart-relaxation`

  * :mod:`autojob.cli.run_vibration`,
    :mod:`autojob.next.vibration` and corresponding CLI command
    `run-vibration`: create metadata preserving thermodynamic calculation
    directories

  * :mod:`autojob.cli.init`: enable shell completion for ``autojob``

  * :mod:`autojob.task`

  * :mod:`autojob.workflow`

  * :mod:`autojob.study`, :mod:`autojob.study_group`, :mod:`autojob.hpc`,
    :mod:`autojob.settings`, :mod:`autobjob.schemas`,
    :mod:`autobjob.parametrizations`

  * :mod:`autojob.calculation`: representations/manipulation of calculation
    data

  * :mod:`autojob.coordinator.gaussian`

* New dependencies:

  * `Pydantic`_ & `pydantic-settings`: for data validation/data model

  * `cclib`: for calculation output parsing

Changed
~~~~~~~

* Deprecated modules:

  * :mod:`autojob.coordinator.calculation`: use :mod:`autojob.calculation`

  * :mod:`autojob.coordinator.classification`: use :mod:`autojob.calculation`

  * :mod:`autojob.coordinator.job`: use :mod:`autojob.calculation`

  * :mod:`autojob.coordinator.study`: use :mod:`autojob.study`

  * :mod:`autojob.coordinator.validation`: use :mod:`autojob.utils`

  * :mod:`autojob.coordinator.vasp`: use :mod:`autojob.calculation.vasp`

* ``vasp.sh`` template no longer removes wildcard files upon cleaning up the
  scratch directory

* Switched to Hatch for build backend and testing (no more Poetry/tox)

* :mod:`autojob.cli.restart`: move to :mod:`autojob.next`

* Dropped support for Python <3.10

* Python and SLURM script templates

* Minimum ``ccu`` dependency is v0.0.5

Removed
~~~~~~~

* :mod:`autojob.accountant` and :mod:`autojob.auditor` have been removed in
  favour of using Pydantic for validation and deserialization

* :mod:`autojob.coordinator.arc` has been removed; use :mod:`autojob.hpc`
  instead

* :mod:`autojob.coordinator.calculation` has been removed; use
  :mod:`autojob.calculation` and :mod:`autojob.task` instead

* :mod:`autojob.coordinator.study` has been removed; use :mod:`autojob.study`
  instead

* :class:`autojob.coordinator.submission_configuration.ParameterSelectionCombobox`
  has been removed

* :mod:`autojob.utils.validate_id` has been removed

`0.11.1`_ (2022-12-02)
----------------------

Added
~~~~~

* :mod:`autojob.details`

Removed
~~~~~~~

* :func:`.findfile.find_details`

* :func:`.findfile.infer_details`

* :func:`.findfile.determine_entry_type`

* :func:`.findfile.find_studies`

`0.11.0`_ (2022-12-01)
----------------------

Added
~~~~~

* ``AMIX``, ``AMIX_MAG``, ``BMIX``, ``BMIX_MAG``, ``IMIX`` Vasp INCAR tags to
  :mod:`autojob.coordinator.vasp`

* :class:`~autojob.coordinator.vasp.VaspError`

* :func:`.findfile.get_slurm_job_id`

* :func:`.findfile.find_last_submitted_jobs`

Changed
~~~~~~~

* :class:`~xml.etree.ElementTree.ParseError`s are caught by
  :meth:`.Restarter.characterize_jobs`

* Default buffer time (i.e., time that a Vasp calculation is stopped prior to
  the actual end time) is increased from 5% to 10%

* :func:`.findfile.find_template_dir` renamed to
  :func:`.findfile._find_template_dir`
  (i.e., made private to module)

Fixed
~~~~~

* Parsing of structure name in
  :meth:`.Restarter.create_restart_jobs`

* New job names returned by
  :meth:`.Restarter.create_restart_jobs` instead of old job names

`0.10.6`_ (2022-11-28)
----------------------

Added
~~~~~

* docstrings for :mod:`autojob.accountant.parsing` functions

* Optional keyword argument parameter (``with_wavecar``) to
  :meth:`autojob.cli.restart.Restarter.create_restart_jobs`

* Optional inclusion of ``WAVECAR`` in restarted jobs from
  ``autojob restart``

* :meth:`autojob.cli.restart.Restarter.characterize_jobs`

Changed
~~~~~~~

* study group ID, study ID, calculation ID, and job ID included in
  :class:`.accountant.AccountingError` raised by
  :func:`.parsing.parse_job_results`

* ``gamma`` key added to first dictionary returned by
  :func:`.parsing.parse_job_results`

* Different printing of not added study groups in
  :meth:`.Accountant.create_study_group`, :meth:`.Accountant.create_study`,
  :meth:`.Accountant.create_calculation` depending on verbosity

* :meth:`.Accountant.create_study_group`, :meth:`.Accountant.create_study`,
  :meth:`.Accountant.create_calculation` print unknown errors to console

Fixed
~~~~~

* values argument to :class:`.job.CalculationParameter` for ``LDAUTYPE`` and
  ``NSW``

`0.10.5`_ (2022-11-22)
----------------------

Changed
~~~~~~~

* Memory limit specified per core instead of per node

Fixed
~~~~~

* rendering of k-pts in ``run.py``


`0.10.4`_ (2022-11-15)
----------------------

Added
~~~~~

* Option to format the ``vasp.sh`` for running on ComputeCanada clusters

Removed
~~~~~~~

* removed support for dictionaries in
  :func:`.validation.iter_to_native`

`0.10.3`_ (2022-11-14)
----------------------

Added
~~~~~

* :func:`.validation.iter_to_native` supports dictionaries

Changed
~~~~~~~

* :class:`autojob.coordinator.gui.groups.CalculationParameterGroup` stores
  values as native Python values instead of strings

Fixed
~~~~~

* Fixed issue with distinguishing calculation parameters in submission
  parameter tab


`0.10.2`_ (2022-11-12)
----------------------

Added
~~~~~

* Add docstrings for :func:`.findfile.find_study_group_dirs`,
  :func:`.findfile.find_study_dirs`,
  :func:`.findfile.find_calculation_dirs`, and
  :func:`.findfile.find_job_dirs`

* docstrings for :class:`~autojob.auditor.auditor.Auditor`

* :meth:`.Auditor.audit`

* :meth:`.Auditor.format`

* :meth:`.Auditor.prune`

* :meth:`.Auditor.prune_calculation_directories`

* ``autojob auditor`` CLI subcommands (`add`, `format`, `prune`)

* `Jinja2`_ dependency

Changed
~~~~~~~

* render `run.py` and `vasp.sh` using Jinja2 templates

`0.10.1`_ (2022-11-12)
----------------------

Changed
~~~~~~~

* The structure name for a restart job is determined from the `run.py` file

`0.10.0`_ (2022-11-06)
----------------------

Added
~~~~~

* outline of :mod:`autojob.auditor` subpackage

Changed
~~~~~~~

* :meth:`.JobStats.parse_max_rss` parses memory
  appropriately according to units

* `dest` variable not passed to
  :meth:`.Accountant.export`

Fixed
~~~~~

* :meth:`.Accountant.add` now correctly calls :meth:`.Accountant.create_study`
  instead of :meth:`.Accountant.create_study_group`

* :meth:`.Accountant.export` no longer passes `dest` as positional argument to
  :meth:`.Accountant._export_jobs`, :meth:`.Accountant._export_calculations`,
  :meth:`.Accountant._export_studies`, and
  :meth:`.Accountant._export_study_groups`

* :func:`.parsing.parse_job_results` handles :class:`IndexError` from
  parsing `vasprun.xml`

`0.9.7`_ (2022-10-18)
---------------------

Removed
~~~~~~~

* `pymongo` dependency

`0.9.6`_ (2022-10-18)
---------------------

Changed
~~~~~~~

* `--memory-scale` CLI option for `autojob restart` was renamed to
  `--memory-multiplier`

Fixed
~~~~~

* `autojob restart` now prints the new job ID instead of the old ID when
  listing newly created jobs

`0.9.5`_ (2022-10-17)
---------------------

Changed
~~~~~~~

* `autojob restart` prints all newly created jobs

* New memory requirements are printed with the 'GB' suffix

Fixed
~~~~~

* the correct directories were not found due to the regex used in
  :func:`.findfile.find_study_group_dirs`, :func:`.findfile.find_study_dirs`,
  :func:`.findfile.find_calculation_dirs`, and :func:`.findfile.find_job_dirs`

* the `vasp.sh` file is now correctly opened instead of attempting to open
  the old job directory

`0.9.4`_ (2022-10-17)
---------------------

Added
~~~~~

* docstring added for :meth:`.TreeviewFrame.clear_treeview`

* docstrings added for :mod:`autojob.coordinator.gui.submission_configuration`

Changed
~~~~~~~

* :meth:`.Coordinator.calc_params_for` and
  :meth:`.Coordinator.calc_param_values_for` accept a list of
  :class:`~pathlib.Path`s for the `structures` parameters instead of a list of
  strings

* :meth:`.Coordinator.structure_groups_with` accepts an iterable of
  :class:`pathlib.Path`s for the `structures` parameters instead of an
  iterable of strings

Removed
~~~~~~~

* :class:`~autojob.coordinator.gui.submission_configuration.ParameterSelectionPanel`

`0.9.3`_ (2022-10-17)
---------------------

Changed
~~~~~~~

* Restart jobs are printed as `calculationID/newjobID`

`0.9.2`_ (2022-10-17)
---------------------

Changed
~~~~~~~

* Logic of `autojob restart` moved into
  :class:`autojob.cli.restart.Restarter` class

`0.9.1`_ (2022-10-17)
---------------------

Added
~~~~~

* :func:`autojob.accountant.findfile.find_study_group_dirs`

* :func:`autojob.accountant.findfile.find_study_dirs`

* :func:`autojob.accountant.findfile.find_calculation_dirs`

* :func:`autojob.accountant.findfile.find_job_dirs`

* :func:`autojob.accountant.findfile.find_template_dir`

`0.9.0`_ (2022-10-16)
---------------------

Changed
~~~~~~~

* `autojob restart` (and related API functions) support scaling the memory
  limit in the restart job and changing the verbosity


`0.8.1`_ (2022-10-13)
---------------------

Added
~~~~~

* User can elect to update database entries instead of overwrite when using
  `autojob accountant add`, using the `-u`CLI option, or
  :meth:`autojob.accountant.accountant.Accountant.add` by setting the
  `update` attribute to `True`

Changed
~~~~~~~

* Formatting of file name returned by
  :func:`autojob.accountant.findfile.get_filename`

* `autojob accountant add` prints added entries by default

* Long CLI options for specifying export files with `autojob accountant add`
  have double hyphen prefixes

`0.8.0`_ (2022-10-13)
---------------------

Added
~~~~~

* :func:`autojob.accountant.findfile.get_filename`

* CLI option `--dest` for `autojob accountant export` subcommand

* User can specify filenames to output `.csv` files for jobs, calculations,
  studies, and study groups with `-jf`, `-cf`, `-sf`, and `-gf` CLI options,
  respectively

* verbose option (`-v`) added for `autojob accountant export` subcommand

Changed
~~~~~~~

* :func:`autojob.accountant.parsing.parse_job_results` raises
  :class:`~autojob.accountant.AccountingError` if no valid `vasprun.xml` found

* :func:`autojob.accountant.accountant.export` has new positional arguments
  `dest` and `filenames`

`0.7.5`_ (2022-10-13)
---------------------

Changed
~~~~~~~

* The job ID of the source job is recorded in the `job.json` file of the
  restart job by :mod:`autojob.cli.restart`

`0.7.4`_ (2022-10-13)
---------------------

Changed
~~~~~~~

* :meth:`.ParameterSelectionTab.calc_params` values are
  :class:`~autojob.coordinator.gui.groups.CalculationParameterGroup`'s

* values in dictionary return by
  :meth:`.ParameterSelectionTab.load_calc_params` are
  :class:`~autojob.coordinator.gui.groups.CalculationParameterGroup`'s

Fixed
~~~~~

* `bool` values are cast correctly in
  :class:`~autojob.coordinator.gui.parameter_selection.ParameterSelectionTab`


`0.7.3`_ (2022-10-12)
---------------------

Fixed
~~~~~

* :class:`AttributeError` due to calling `extend` method of values parameter
  passed to :meth:`.CalculationParameterGroup.add_values` by
  :meth:`.ParameterPanel.add_parameter_values`

`0.7.2`_ (2022-10-12)
---------------------

Changed
~~~~~~~

* Jobs that are not added to database by
  :func:`autojob.accountant.accountant.add` are printed out

* :class:`.accountant.AccountingError` raised if
  :func:`.parsing.parse_job_results` unable to parse `vasprun.xml`
  file twice


`0.7.1`_ (2022-10-12)
---------------------

Added
~~~~~

* DFT+U and magnetization :class:`CalculationParameter`s in
  :mod:`autojob.coordinator.vasp`

Changed
~~~~~~~

* :class:`FileNotFoundError` is handled by
  :func:`autojob.cli.restart.create_restart_calculation`

`0.7.0`_ (2022-10-11)
---------------------

Added
~~~~~

* :meth:`autojob.coordinator.groups.CalculationParameterGroup.defined_values`

* :meth:`.CalculationParameterGroup.defined_calculation_parameters`

* :class:`~autojob.coordinator.groups.SubmissionParameterGroup`

* :mod:`autojob.cli.restart` and correspondind CLI subcommand

Fixed
~~~~~

* Duplicate :class:`CalculationParameter`s in
  :class:`CalculationParameterGroup`

* Extra argument supplied to `load` methods of tabs

* Return value from :meth:`.SelectionFrame.structures`
  is now a list of strings instead of a list of :class:`pathlib.Path`'s

Removed
~~~~~~~

* :meth:`.Coordinator.next_calc_params`

`0.6.1`_ (2022-10-09)
---------------------

Added
~~~~~

* Version option for CLI

`0.6.0`_ (2022-10-09)
---------------------

Added
~~~~~

* :mod:`autojob.coordinator.gui.groups`

Changed
~~~~~~~

* :class:`~autojob.coordinator.gui.job_submission.JobSubmissionTab`,
  :class:`~autojob.coordinator.gui.parameter_selection.ParameterSelectionTab`,
  :class:`~autojob.coordinator.gui.structure_selection.StructureSelectionTab`,
  :class:`~autojob.coordinator.gui.study_configuration.StudyConfigurationTab`,
  :class:`~autojob.coordinator.gui.submission_configuration.SubmissionConfigurationTab`, and
  :class:`~autojob.coordinator.gui.summary.SummaryTab`
  constructors no longer require `notebook` parameter

* :class:`autojob.coordinator.job.InputParameter` renamed to
  :class:`~autojob.coordinator.job.CalculationParameter`


`0.5.1`_ (2022-09-30)
---------------------

Added
~~~~~

* docstrings for :meth:`.Accountant.add` call stack


`0.5.0`_ (2022-09-28)
---------------------

Added
~~~~~

* :func:`autojob.accountant.accountant.export` is implemented in API and CLI

Changed
~~~~~~~

* `as_dict`, `as_flat_dict`, and `from_dict` moved from must be
  implemented by subclasses (e.g., :class:`autojob.coordinator.vasp.VaspJob`)

* structure-related keys in `input_parameters` return value from
  `autojob.accountant.parsing`

* the dictionary return from :meth:`.Calculation.as_dict` includes the keys
  `@module` and `@class`

`0.4.1`_ (2022-09-28)
---------------------

Added
~~~~~

* `Inputs`, `Outputs`, `@module`, `@class` keys in return value dictionary in
  :meth:`.Job.as_dict`

Removed
~~~~~~~

* `k-pts`, and `Results` keys in return value dictionary in
  :class:`.Job.as_dict`

`0.4.0`_ (2022-09-26)
---------------------

Added
~~~~~

* CLI with `coordinator` and `accountant` subcommands

* :class:`~autojob.accountant.findfile.DetailEncoder`

* :class:`~autojob.coordinator.job.JobStats`

* :meth:`.Partition.from_name`

* :func:`.parsing.match_xml_tags`

* :func:`.parsing.parse_job_results`

* :meth:`.Job.as_dict`

* :meth:`.Calculation.as_dict`

* :meth:`Study.as_dict <autojob.coordinator.study.Study.as_dict>`

* :meth:`StudyGroup.as_dict <autojob.coordinator.study_group.StudyGroup.as_dict>`

* :meth:`.Accountant.create_study_group`

* :meth:`.Accountant.create_study`

* :meth:`.Accountant.create_calculation`

* :meth:`.Accountant.create_job`

* :meth:`.Accountant.load_db`

* :meth:`.Accountant.add_to_database`

* :class:`~autojob.coordinator.job.Job` accepts `None` for `results`
  and `job_stats` parameters

Changed
~~~~~~~

* :class:`~autojob.coordinator.main.MainApplication` renamed to
  :class:`~autojob.coordinator.gui.GUI`

* `strict` parameter renamed to `update` in
  :mod:`autojob.accountant.accountant`

* :mod:`autojob.accountant.accountant` CLI methods moved to
  :mod:`autojob.accountant.cli`

* :class:`~autojob.coordinator.calculation.Calculation` accepts a list of
  strings instead of a list of :class:`~autojob.coordinator.job.Job`'s

* :class:`~.autojob.coordinator.study.Study` accepts a list of strings instead
  of a list of :class:`~autojob.coordinator.calculation.Calculation`'s

* :class:`~autojob.coordinator.study.StudyGroup` accepts a list of strings
  instead of a list of :class:`~autojob.coordinator.study.Study`'s

* :class:`~autojob.coordinator.classification.CalculationType`,
  :class:`~autojob.coordinator.classification.CalculatorType`,
  :class:`~autojob.coordinator.classification.StudyType` do not capitalize
  `__str__` return value

* :class:`~autojob.accountant.accountant.Accountant` constructor requires three
  positional arguments (`exclusive`, `update`, `verbose`)

* `exclusive`, `update`, `verbose` are stored as instance attributes of
  :class:`~autojob.accountant.accountant.Accountant` objects and are no longer
  passed as arguments to :meth:`.Accountant.add`

* :func:`autojob.accountant.parsing.parse_job_stats_file` raises
  :class:`~autojob.accountant.AccountingError` is unable to parse job stats
  file

* :func:`.parsing.parse_job_stats_file` raises `ValueError` is headers missing
  in job stats file

* :class:`~autojob.coordinator.job.Job` properties changed to attributes

* :attr:`.Study.study_type` property changed to attribute

* :attr:`.StudyGroup.date_created` property changed to attribute

* :class:`~autojob.coordinator.calculation.Calculation` properties
  (except `job`) changed to attributes

`0.3.0`_ (2022-09-13)
---------------------

Added
~~~~~

* `isym` as a vasp parameter

Changed
~~~~~~~

* Properties of :class:`~autojob.coordinator.coordinator.Coordinator` are no
  longer cached


`0.2.0`_ (2022-09-12)
---------------------

Added
~~~~~

* :mod:`autojob.accountant`

* :mod:`autojob.coordinator.scripter`

* :class:`monty.json.MSONable` methods to
  :class:`~autojob.coordinator.calculation.Calculation`,
  :class:`~autojob.coordinator.job.Job`,
  :class:`~autojob.coordinator.study.Study`, and
  :class:`~autojob.coordinator.study.StudyGroup`

Changed
~~~~~~~

* Refactored tests

* Moved package to `src/` directory

* scripting capabilities located in :mod:`autojob.coordinator.scripter`

`0.1.2`_ (2022-09-08)
---------------------

Removed
~~~~~~~

* `pymatgen-db`, `acat`, `wulffpack`, `scipy`, `pandas`
  dependencies

Changed
~~~~~~~

* The list containing GUI pages has been re-implemented as a dictionary

`0.1.1`_ (2022-09-07)
---------------------

Added
~~~~~

* The Job Submission tab allows for different submission parameters
  for each :class:`~autobjob.coordinator.gui.groups.ParameterGroup`

* :class:`~autojob.coordinator.gui.job_submission.JobSubmissionTab`

* :mod:`autojob.coordinator.gui.submission_configuration`

* Structure groups

* :class:`~autojob.coordinator.gui.widgets.TreeviewFrame`

* :func:`.validation.val_to_native`

* :func:`.validation.iter_to_native`

* Summary Tab in GUI

* :mod:`autojob.coordinator.coordinator`

Changed
~~~~~~~

* Refactor :mod:`autojob.coordinator.gui.parameter_selection`

`0.1.0`_ (2022-09-02)
---------------------

* First version.

.. _Unreleased: https://gitlab.com/ugognw/python-autojob/-/compare/v0.11.1...development?from_project_id=39386367&straight=true
.. _0.11.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.11.0...v0.11.1?from_project_id=39386367&straight=true
.. _0.11.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.10.6...v0.11.0?from_project_id=39386367&straight=true
.. _0.10.6: https://gitlab.com/ugognw/python-autojob/-/compare/v0.10.5...v0.10.6?from_project_id=39386367&straight=true
.. _0.10.5: https://gitlab.com/ugognw/python-autojob/-/compare/v0.10.4...v0.10.5?from_project_id=39386367&straight=true
.. _0.10.4: https://gitlab.com/ugognw/python-autojob/-/compare/v0.10.3...v0.10.4?from_project_id=39386367&straight=true
.. _0.10.3: https://gitlab.com/ugognw/python-autojob/-/compare/v0.10.2...v0.10.3?from_project_id=39386367&straight=true
.. _0.10.2: https://gitlab.com/ugognw/python-autojob/-/compare/v0.10.1...v0.10.2?from_project_id=39386367&straight=true
.. _0.10.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.10.0...v0.10.1?from_project_id=39386367&straight=true
.. _0.10.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.9.7...v0.10.0?from_project_id=39386367&straight=true
.. _0.9.7: https://gitlab.com/ugognw/python-autojob/-/compare/v0.9.6...v0.9.7?from_project_id=39386367&straight=true
.. _0.9.6: https://gitlab.com/ugognw/python-autojob/-/compare/v0.9.5...v0.9.6?from_project_id=39386367&straight=true
.. _0.9.5: https://gitlab.com/ugognw/python-autojob/-/compare/v0.9.4...v0.9.5?from_project_id=39386367&straight=true
.. _0.9.4: https://gitlab.com/ugognw/python-autojob/-/compare/v0.9.3...v0.9.4?from_project_id=39386367&straight=true
.. _0.9.3: https://gitlab.com/ugognw/python-autojob/-/compare/v0.9.2...v0.9.3?from_project_id=39386367&straight=true
.. _0.9.2: https://gitlab.com/ugognw/python-autojob/-/compare/v0.9.1...v0.9.2?from_project_id=39386367&straight=true
.. _0.9.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.9.0...v0.9.1?from_project_id=39386367&straight=true
.. _0.9.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.8.1...v0.9.0?from_project_id=39386367&straight=true
.. _0.8.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.8.0...v0.8.1?from_project_id=39386367&straight=true
.. _0.8.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.7.5...v0.8.0?from_project_id=39386367&straight=true
.. _0.7.5: https://gitlab.com/ugognw/python-autojob/-/compare/v0.7.4...v0.7.5?from_project_id=39386367&straight=true
.. _0.7.4: https://gitlab.com/ugognw/python-autojob/-/compare/v0.7.3...v0.7.4?from_project_id=39386367&straight=true
.. _0.7.3: https://gitlab.com/ugognw/python-autojob/-/compare/v0.7.2...v0.7.3?from_project_id=39386367&straight=true
.. _0.7.2: https://gitlab.com/ugognw/python-autojob/-/compare/v0.7.1...v0.7.2?from_project_id=39386367&straight=true
.. _0.7.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.7.0...v0.7.1?from_project_id=39386367&straight=true
.. _0.7.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.6.1...v0.7.0?from_project_id=39386367&straight=true
.. _0.6.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.6.0...v0.6.1?from_project_id=39386367&straight=true
.. _0.6.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.5.1...v0.6.0?from_project_id=39386367&straight=true
.. _0.5.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.5.0...v0.5.1?from_project_id=39386367&straight=true
.. _0.5.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.4.1...v0.5.0?from_project_id=39386367&straight=true
.. _0.4.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.4.0...v0.4.1?from_project_id=39386367&straight=true
.. _0.4.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.3.0...v0.4.0?from_project_id=39386367&straight=true
.. _0.3.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.2.0...v0.3.0?from_project_id=39386367&straight=true
.. _0.2.0: https://gitlab.com/ugognw/python-autojob/-/compare/v0.1.2...v0.2.0?from_project_id=39386367&straight=true
.. _0.1.2: https://gitlab.com/ugognw/python-autojob/-/compare/v0.1.1...v0.1.2?from_project_id=39386367&straight=true
.. _0.1.1: https://gitlab.com/ugognw/python-autojob/-/compare/v0.1.0...v0.1.1?from_project_id=39386367&straight=true
.. _0.1.0: https://gitlab.com/ugognw/python-autojob/-/tree/v0.1.0?ref_type=tags

.. _Pydantic: https://docs.pydantic.dev/latest/
.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html
.. _Jinja2: http://jinja.palletsprojects.com
