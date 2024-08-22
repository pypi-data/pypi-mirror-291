Building the Documentation
--------------------------

``autojob`` uses Sphinx to build its documentation.

If you are using hatch to manage environments, you can install the
"docs" environment and build the documentation using:

.. code-block:: shell

    hatch env run build-html:docs

This is effectively equivalent to running:

.. code-block:: shell

    pip install -e .'[docs]'
    sphinx-build -b html docs/source docs/build/html/

The above commands will run ``sphinx-apidoc`` on the codebase and build the HTML files
from the existing ``.rst`` files. To run a local server to view changes to the
documentation, you can run:

.. code-block:: shell

    hatch env run serve:docs

or explicitly run ``sphinx-autobuild``:

.. code-block:: shell

    sphinx-autobuild --port 0 docs/source docs/build/
