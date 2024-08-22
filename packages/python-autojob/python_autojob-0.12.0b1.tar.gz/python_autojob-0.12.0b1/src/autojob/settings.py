"""Global settings and configuration for ``autojob``."""

import logging
from logging import handlers
import os
from pathlib import Path
from typing import Any
from typing import ClassVar

from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from pydantic_settings.sources import TomlConfigSettingsSource

logger = logging.getLogger(__name__)

AUTOJOB_HOME = (
    Path()
    .home()
    .resolve()
    .joinpath(
        ".config",
        "autojob",
    )
)
DEFAULT_CONFIG_FILE = AUTOJOB_HOME.joinpath("config.toml")


class AutojobSettings(BaseSettings):
    """Settings for ``autojob``."""

    TASK_FILE: str = Field(
        default="task.json",
        description="the default file name to use to store task metadata",
    )
    JOB_FILE: str = Field(
        default="job.json",
        description="the default file name to use to store job metadata",
    )
    CALCULATION_FILE: str = Field(
        default="calculation.json",
        description="the default file name to use to store calculation "
        "metadata",
    )
    RECORD_FILE: str = Field(
        default="record.txt",
        description="the default file name to use to store the study record",
    )
    STUDY_FILE: str = Field(
        default="study.json",
        description="the default file name to use to store study metadata",
    )
    STUDY_GROUP_FILE: str = Field(
        default="study_group.json",
        description="the default file name to use to store study group "
        "metadata",
    )
    WORKFLOW_FILE: str = Field(
        default="workflow.json",
        description="the default file name to use to store study workflow "
        "data",
    )
    PARAMETRIZATION_FILE: str = Field(
        default="parametrizations.json",
        description="the default file name to use to store study "
        "parametrization data",
    )
    PYTHON_SCRIPT: str = Field(
        default="run.py",
        description="the default file name to use for the python script",
    )
    SLURM_SCRIPT: str = Field(
        default="vasp.sh",
        description="the default file name to use for the SLURM script",
    )
    PYTHON_TEMPLATE: str = Field(
        default="run.py.j2",
        description="the default file name to use for the python script "
        "template",
    )
    SLURM_TEMPLATE: str = Field(
        default="run.sh.j2",
        description="the default file name to use for the SLURM script "
        "template",
    )
    JOB_STATS_FILE: str = Field(
        default="job_stats.txt",
        description="the default file name to use for the job stats file",
    )
    LOG_FILE: Path | None = Field(
        default=None,
        description="The filename for the log file. Note that this variable "
        "is mainly for storing state for application-like use. If you are "
        "using autojob as a library, you may be better served "
        "configuring handlers.",
    )
    LOG_LEVEL: int = Field(
        default=logging.DEBUG,
        description="The default log level.",
    )
    INPUT_ATOMS: str = Field(
        default="in.traj",
        description="the default file name to use for the input Atoms file",
    )
    OUTPUT_ATOMS: str = Field(
        default="final.traj",
        description="the default file name to use for the output Atoms file",
    )
    TEMPLATE_DIR: Path | None = Field(
        default=None,
        description="If not None, specifies the directory to use to load "
        "templates",
    )
    STRICT_MODE: bool = Field(
        default=True,
        description="Sets the default behaviour of data retrieval functions "
        "and methods. If True, such functions will raise errors when they "
        "fail. Otherwise, failure will pass with a log message only. This "
        "may be useful if you are harvesting the results of incomplete tasks.",
    )

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="AUTOJOB_", case_sensitive=True, env_ignore_empty=True
    )

    @field_validator("LOG_LEVEL", mode="plain")
    @classmethod
    def validate_log_level(cls, v: Any) -> int:
        """Validate the global log level."""
        if isinstance(v, int):
            return v

        try:
            return getattr(logging, v)
        except AttributeError as err:
            msg = f"{v} not a valid logging level"
            raise ValueError(msg) from err
        except TypeError as err:
            msg = f"Unable to convert {v} into a logging level"
            raise ValueError(msg) from err

    @model_validator(mode="after")
    def configure_logging(self) -> "AutojobSettings":
        """Configure logging based on user settings."""
        if self.LOG_FILE:
            fh = handlers.RotatingFileHandler(
                self.LOG_FILE, encoding="utf-8", maxBytes=1e6, backupCount=3
            )
            log_format = (
                "%(asctime)s - %(name)s::%(funcName)s::%(lineno)s - "
                "%(levelname)s - %(message)s "
            )
            formatter = logging.Formatter(log_format)
            fh.setFormatter(formatter)
            fh.setLevel(level=self.LOG_LEVEL)
            logger.addHandler(fh)

        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Add a TOML configuration file to the settings sources.

        Note that the name of the TOML file can be set via environment
        variables. Otherwise, the default filename is used.
        """
        toml_file = os.environ.get("AUTOJOB_CONFIG_FILE", DEFAULT_CONFIG_FILE)
        logger.info("Configuration file will be read from %s", toml_file)

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls, toml_file),
            file_secret_settings,
        )
