"""
Module to analyze the Document Regexp Model (DRM) directory in order
to load the available DRMs for the document parser.
"""
import logging
import os
import re

from regex4ocr.logger.formatter import format_logger
from regex4ocr.parser.validation import is_valid_drm
from regex4ocr.parser.yml_parser import parse_yml

logger = format_logger(logging.getLogger(__name__))


def has_drm_match(ocr_result, drm):
    """
    Checks if a drm matches the ocr_result format.

    Args:
        ocr_result (str): OCR result string;
        drm (dict): DRM dict object for parsing the OCR string.

    Returns:
        (bool): Returns True if the DRM identifier matches with
                OCR result string.
    """
    id_regexps = drm["identifiers"]

    for id_regexp in id_regexps:
        regexp = re.compile(id_regexp, re.IGNORECASE)

        if not re.search(regexp, ocr_result):
            return False

    return True


def get_all_drms_match(ocr_result, drms):
    """
    Returns all DRM dicts that matches the OCR string document model.

    Args:
        ocr_result (str): OCR result string;
        drms (dict): list of all DRMs dicts found in the DRM directory folder.

    Returns:
        (list): List of all DRM dicts that matches the OCR document string or
                an empty list if there are no DRM matches.
    """
    drm_matches = [drm for drm in drms if has_drm_match(ocr_result, drm)]

    return drm_matches


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
