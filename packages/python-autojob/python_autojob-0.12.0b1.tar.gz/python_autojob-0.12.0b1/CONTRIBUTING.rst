===============
Contributing 🤝
===============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Bug reports
===========

When `reporting a bug <https://gitlab.com/ugognw/python-autojob/issues>`_ please include:

    * Your operating system name and version.
    * Any details about your local setup that might be helpful in troubleshooting.
    * Detailed steps to reproduce the bug.

Documentation improvements
==========================

``autojob`` could always use more documentation, whether as part of the
official autojob docs, in docstrings, or even on the web in blog posts,
articles, and such.

Feature requests and feedback
=============================

The best way to send feedback is to file an issue at https://gitlab.com/ugognw/python-autojob/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome :)

Development
===========

To set up `python-autojob` for local development:

1. Fork `python-autojob <https://gitlab.com/ugognw/python-autojob>`_
   (look for the "Fork" button).

2. Clone your fork locally::

    git clone git@gitlab.com:YOURGITLABNAME/python-autojob.git

3. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. A suitable development environment can be obtained by installing the
   ``test``, ``dev``, and ``docs`` extras::

    python3 -m pip install .'[test,dev,docs]'

5. When you're done making changes, run the unit tests with::

        pytest tests

    run the linting checks with ``pre-commit``::

        pre-commit run

    build the docs with::

        sphinx-build -b html docs/source docs/build/html

    and run link checks and doctests with::

        sphinx-build -b linkcheck docs/source docs/build/linkcheck
        sphinx-build -b doctest docs/source docs/build/doctest

6. Commit your changes and push your branch to GitLab::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitLab website.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make a pull request.

For merging, you should:

1. Ensure that tests pass locally (run ``pytest``).
2. Update documentation when there's new API, functionality etc.
3. Add a note to ``CHANGELOG.rst`` about the changes.
4. Add yourself to ``AUTHORS.rst``.



Tips
----

To run a subset of tests::

    tox -e envname -- pytest -k test_myfeature

To run all the test environments in *parallel*::

    tox -p auto
