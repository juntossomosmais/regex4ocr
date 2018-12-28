"""
Module with all the functions used throughout the pre process
stage of the OCR result string.
"""
import logging
import re

from unidecode import unidecode

from regex4ocr.logger.formatter import format_logger

logger = format_logger(logging.getLogger(__name__))


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


def apply_options(ocr_result, options):
    """
    Applies the options configus of the matching DRM.

    Args:
        ocr_result (str): OCR result string;
        options (dict): options configuration from the DRM dict.

    Returns:
        (str): The pre processed OCR result string according to the DRM.
    """
    pre_processed_str = ocr_result

    if options.get("lowercase"):
        pre_processed_str = pre_processed_str.lower()

    if options.get("remove_whitespace"):
        pre_processed_str = re.sub(r"\s", "", pre_processed_str)

    if options.get("force_ascii"):
        pre_processed_str = unidecode(pre_processed_str)

    if options.get("replace"):
        pre_processed_str = process_replaces(
            pre_processed_str, options["replace"]
        )

    return pre_processed_str


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
    options = drm.get("options")

    # applies options if any
    if options:
        pre_processed_str = apply_options(ocr_result, options)

        return pre_processed_str

    # no pre processing
    return ocr_result
