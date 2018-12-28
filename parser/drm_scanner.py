"""
Module to analyze the Document Regexp Model (DRM) directory in order
to load the available DRMs for the document parser.
"""
import logging
import os
from parser.validation import is_valid_drm
from parser.yml_parser import parse_yml

from logger.formatter import format_logger

logger = format_logger(logging.getLogger(__name__))


def scan_drms_folder(drms_path):
    """
    Scans the DRM directory in order to load a list of available
    DRMs to parse the ocr result string.

    Args:
        drms_path (str): file system folder path of the drms

    Returns:
        (list): list of DRMs to parse the ocr result string.
    """
    base_path = os.path.join(drms_path, "")  # adds final flash of the directory
    all_files = os.listdir(drms_path)
    drms = []

    for file in all_files:
        logger.debug("Reading file %s...", base_path + file)

        drm_dict = parse_yml(base_path + file)

        if drm_dict and is_valid_drm(drm_dict):
            logger.debug("Appending valid DRM...")
            drms.append(drm_dict)

    logger.debug("Returning scanned DRMs...")

    return drms
