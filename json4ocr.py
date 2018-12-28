"""
Main module to parse OCR results.
"""
import logging
from parser.analyzer import scan_drms_folder
from parser.drm import parse_ocr_result

from logger.formatter import format_logger

logger = format_logger(logging.getLogger(__name__))


def json4ocr(ocr_result, drms_path="./drms"):
    """
    Applies regexp rules to the ocr result string in order to extract required
    data to JSON format.

    Args:
        ocr_result (str): OCR result string;
        drms_path (str): filesys path to the folder with the
                         document regexp models (drms).

    Returns:
        (dict): Python dict with the results.
    """
    logger.info("Scanning DRMs directory...")
    drm_dicts = scan_drms_folder(drms_path)

    logger.info("Parsing the OCR string result...")
    ocr_data = parse_ocr_result(ocr_result, drm_dicts)

    logger.info("Returning the parsed OCR data...")

    return ocr_data