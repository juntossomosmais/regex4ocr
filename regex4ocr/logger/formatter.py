"""
Module which sets the logging configuration and format for the app.
"""

import logging
import os
import sys

# module variables to configure the logs
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")

LEVEL_MAPPING = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


class LogFormatter(logging.Formatter):
    """
    This class formats each log record before sending it to the
    output stream.
    """

    def format(self, record):
        return super(LogFormatter, self).format(record)


def format_logger(logger):
    """
    Sets a specific format for the logger.

    Args:
        logger (logging.Logger): The logger instance.

    Returns:
        (logging.Logger): The formatted logger instance.
    """
    # sets the stream output for the logger
    handler = logging.StreamHandler(sys.stdout)

    # sets the logger format handler
    handler.setFormatter(
        LogFormatter(
            "%(asctime)s - %(name)s - level=%(levelname)s - %(message)s"
        )
    )

    # sets the logger level based on the os variable
    logger.setLevel(LEVEL_MAPPING[LOGGING_LEVEL])

    # adds the format handler to the logger
    logger.addHandler(handler)

    return logger
