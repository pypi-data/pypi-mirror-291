Usage
=====

Enable Shell Completion
-----------------------

Shell completion is supported for the bash, zsh, and fish shells. Shell
completion can be enabled by running  :prog:`autojob init` and then restarting
your shell.

CLI Commands
------------

.. click:: autojob.cli.main:main
    :prog: autojob
    :nested: full

.. click:: autojob.cli.restart_relaxation:main
    :prog: restart-relaxation
    :nested: full

.. click:: autojob.cli.run_vibration:main
    :prog: run-vibration
    :nested: full
