"""
Init module to expose the regex4ocr function.
"""
from regex4ocr.logger.formatter import config_log

from .main import parse

# configures the application logger
config_log()
