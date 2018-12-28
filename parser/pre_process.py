"""
Module with all the functions used throughout the pre process
stage of the OCR result string.
"""
import logging
import re

from unidecode import unidecode

from logger.formatter import format_logger

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
        (list): List of all DRM dicts that matches the OCR document string.
    """
    drm_matches = [drm for drm in drms if has_drm_match(ocr_result, drm)]

    return drm_matches


def process_replaces(pre_process_str, replaces):
    """
    Performs string replaces in the original ocr_result in the pre processing
    stage of the OCR result.

    Args:
        pre_process_str (str): OCR document str in the pre process stage;
        replaces (list): List of tuples in the following format:
                         [(regexp, replace_str), (regexp, replace_str), ...]

    Returns:
        (str): The pre processed OCR result string after the DRM option
               replaces.
    """
    for regexp, replacement in replaces:
        pre_process_str = re.sub(regexp, replacement, pre_process_str)

    return pre_process_str


def pre_process_result(ocr_result, drm):
    """
    Pre processes OCR document result string based on a DRM match and its
    OPTIONS fields.

    Args:
        ocr_result (str): OCR result string;
        drm (dict): DRM dict that matches the OCR document string format.

    Returns:
        (str): The pre processed OCR result string according to the DRM.
    """
    pre_process_str = ocr_result

    options = drm.get("options")

    if options:

        if options.get("lowercase"):
            pre_process_str = pre_process_str.lower()

        if options.get("remove_whitespace"):
            pre_process_str = re.sub(r"\s", "", pre_process_str)

        if options.get("force_ascii"):
            pre_process_str = unidecode(pre_process_str)

        if options.get("replace"):
            pre_process_str = process_replaces(
                pre_process_str, options["replace"]
            )

    return pre_process_str
