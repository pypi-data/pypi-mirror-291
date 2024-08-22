"""The Configuration Module.

The module contains Model for Gunicorn Configuration.
"""
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import field_validator


class GunicornConfigModel(BaseSettings):
    """Base setting of the Gunicorn Deployment.

    Class creates the deployment config. Also contains default values
    """

    gunicorn_host: str = "0.0.0.0"
    gunicorn_port: str = "5000"
    gunicorn_workers: int = 3
    gunicorn_worker_class: str = "uvicorn.workers.UvicornWorker"
    gunicorn_loglevel: str = "info"
    gunicorn_logconfig: Optional[str] = None
    gunicorn_timeout: int = 1200
    gunicorn_max_requests: int = 200
    gunicorn_max_requests_jitter: int = 20
    gunicorn_preload_app: bool = False

    @field_validator("gunicorn_logconfig", mode="before")
    def set_gunicorn_logconfig(cls, value, values):
        """Setter of gunicorn logging config.

        Sets the gunicorn logging configuration.
        :params value: value for `gunicorn_logconfig` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: gunicorn logging configuration file path
        """
        gunicorn_loglevel = values.data.get("gunicorn_loglevel")
        package_dir = Path(__file__).resolve().parent
        if gunicorn_loglevel.lower() == "debug":
            return str(package_dir / "gunicorn_logging_debug.cfg")
        else:
            return str(package_dir / "gunicorn_logging.cfg")
