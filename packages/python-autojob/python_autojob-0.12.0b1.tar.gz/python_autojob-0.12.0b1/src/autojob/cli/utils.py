"""Utilities for CLI commands."""

import logging
from logging import handlers

import click

from autojob import SETTINGS

LEVEL_TO_COLOR: dict[int, str] = {
    logging.DEBUG: "green",
    logging.INFO: "blue",
    logging.WARNING: "yellow",
    logging.ERROR: "magenta",
    logging.CRITICAL: "red",
}


logger = logging.getLogger(__package__.split(".")[0])


class FancyConsoleHandler(logging.StreamHandler):
    """A handler that prints colourful output to stderr."""

    def emit(self, record: logging.LogRecord):
        """Emit a record using ``click.secho``.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline in
        ANSI colours depending on the log level.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            color = LEVEL_TO_COLOR[record.levelno]
            click.secho(msg, color=True, fg=color)
        except RecursionError:  # See issue 36272 in CPython
            raise
        # This is how Python catches the exception
        except Exception:  # noqa: BLE001
            self.handleError(record)


def configure_logging(console_log_level: int = logging.WARNING) -> None:
    """Configure logging and printing for command-line functions.

    The log file an dare read from the SETTINGS values. In particular,


    Args:
        console_log_level: The log level for messages printed to the console.
            Defaults to logging.WARNING.
    """
    logger.setLevel(logging.DEBUG)
    log_format = (
        "%(asctime)s - %(name)s::%(funcName)s::%(lineno)s - "
        "%(levelname)s - %(message)s "
    )
    formatter = logging.Formatter(log_format)

    # ! we don't remove existing stream handlers, so be sure
    # ! not to set it twice if that's not intended
    if SETTINGS.LOG_FILE is not None:
        fh = handlers.RotatingFileHandler(
            SETTINGS.LOG_FILE, encoding="utf-8", maxBytes=1e8, backupCount=5
        )
        fh.setLevel(level=SETTINGS.LOG_LEVEL)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = FancyConsoleHandler()
    stderr_formatter = logging.Formatter("%(message)s")
    ch.setFormatter(stderr_formatter)
    ch.setLevel(level=console_log_level)
    logger.addHandler(ch)
