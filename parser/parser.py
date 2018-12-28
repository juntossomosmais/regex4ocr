"""
Module with the drm parser.
"""
import logging
from parser.extraction import extract_ocr_data
from parser.drm_scanner import get_all_drms_match
from parser.pre_process import pre_process_result

from logger.formatter import format_logger

logger = format_logger(logging.getLogger(__name__))


def parse_ocr_result(ocr_result, drms):
    """
    Parses and extract data from the OCR document result string by
    using a DRM (Document Regexp Model) that matches this OCR string.

    Args:
        ocr_result (str): OCR result string;
        drms (dict): list of all DRMs dicts found in the DRM directory folder.

    Returns:
        (list): List of all DRM dicts that matches the OCR document string.
    """
    logger.info("Verifying DRMs that match with this OCR document string...")
    drms = get_all_drms_match(ocr_result, drms)

    if not drms:
        raise RuntimeError("No DRM Match!")

    drm = drms[0]
    logger.info("Using the following DRM: %s", drm)

    logger.info("Pre processing the OCR result according to DRM...")
    pre_processed_result = pre_process_result(ocr_result, drm)
    logger.debug(
        "Showing pre processed OCR result...\n%s", pre_processed_result
    )

    logger.info("Extracting json data from the OCR pre processed result...")
    data = extract_ocr_data(pre_processed_result, drm)

    return data
