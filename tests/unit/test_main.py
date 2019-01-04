"""
Unit tests for the main regex4ocr function.
"""
from unittest import mock

import pytest

from regex4ocr.main import parse
from tests.data.aux import open_file


@pytest.fixture(scope="module")
def ocr_test_rslt_folder():
    """ OCR test data fixture. """
    OCR_TEST_RESULT_FOLDER = "./tests/data/ocr_results/"

    return OCR_TEST_RESULT_FOLDER


@mock.patch("regex4ocr.main.parse_ocr_result")
@mock.patch("regex4ocr.main.scan_drms_folder")
def test_regex4ocr_function(
    mocked_scan_drms_folder, mocked_parse_ocr_result, ocr_test_rslt_folder
):
    """
    Unit: Tests regex4ocr function logic.
    """
    ocr_result = open_file(ocr_test_rslt_folder + "tax_coupon_1.txt")
    drms_path = "./drms"

    mocked_drms_1 = {"test": 1}
    mocked_drms_2 = {"test": 2}

    mocked_scan_drms_folder.return_value = [mocked_drms_1, mocked_drms_2]
    mocked_parse_ocr_result.return_value = "test_parsed_ocr_result"

    assert parse(ocr_result, drms_path) == "test_parsed_ocr_result"

    mocked_scan_drms_folder.assert_called_once_with(drms_path)
    mocked_parse_ocr_result.assert_called_once_with(
        ocr_result, [mocked_drms_1, mocked_drms_2]
    )
