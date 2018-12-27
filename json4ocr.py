"""
Main module to parse OCR results.
"""
from parsers.doc_model import get_drms
from parsers.drm import parse_ocr_result


def json4ocr(ocr_result, drms_path="./docmodels"):
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
    drm_dicts = get_drms(drms_path)

    ocr_data = parse_ocr_result(ocr_result, drm_dicts)

    return ocr_data
