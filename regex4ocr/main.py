"""
Main module to parse OCR results.
"""
import logging

from regex4ocr.logger.formatter import format_logger
from regex4ocr.parser.drm_scanner import scan_drms_folder
from regex4ocr.parser.parser import parse_ocr_result

logger = format_logger(logging.getLogger(__name__))


def parse(ocr_result, drms_path="./drms"):
    """
    Applies regexp rules to the ocr result string in order to extract the
    desired data and convert it to a final JSON (Python dict) format.

    Args:
        ocr_result (str): OCR result string;
        drms_path (str): filesys path to the folder with the
                         document regexp models (drms).

    Returns:
        (dict): Python dict with the results or None if no DRM
                matches the ocr_result string.
    """
    logger.info("Scanning DRMs directory...")
    drm_dicts = scan_drms_folder(drms_path)

    logger.info("Parsing the OCR string result...")
    ocr_data = parse_ocr_result(ocr_result, drm_dicts)

    logger.info("Returning the parsed OCR data...\n%s", ocr_data)

    return ocr_data
