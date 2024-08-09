import json
import os
from logging import config


def configure_logging() -> None:
    """Configure logging for Flask App"""
    config_path = os.environ.get(
        "FLASK_LOGGING",
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "logging.json")
    )

    with open(config_path, encoding="utf-8") as config_file:
        logging_config = json.load(config_file)
        config.dictConfig(logging_config)
