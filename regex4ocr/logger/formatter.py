"""
Module which sets the logging configuration and format for the app.
"""
import logging
import logging.config
import os

# module variables to configure the logs
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")

LEVEL_MAPPING = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


def config_log():
    """
    Configures the root logger of the application.
    """
    my_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - level=%(levelname)s - %(message)s"
    )

    my_handler = logging.StreamHandler()
    my_handler.setFormatter(my_formatter)

    logging.getLogger().addHandler(my_handler)
    logging.getLogger().setLevel(LEVEL_MAPPING[LOGGING_LEVEL])
