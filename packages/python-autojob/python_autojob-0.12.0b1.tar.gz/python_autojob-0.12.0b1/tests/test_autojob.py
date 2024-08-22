import logging

from click.testing import CliRunner

from autojob.cli.main import main

logger = logging.getLogger(__name__)


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    logger.debug(f"CLI result:\n{result.output}")
    assert "Usage: autojob" in result.output
    assert result.exit_code == 0
