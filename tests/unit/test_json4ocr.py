"""
Unit tests for the json4ocr module.
"""
import unittest
from unittest import mock

from json4ocr import json4ocr
from tests.data.aux import open_file


class TestJson4OcrModule(unittest.TestCase):
    """
    Unit tests for the json4ocr module.
    """

    OCR_RESULTS_FILE_PATH = "./tests/data/ocr_results/"

    @mock.patch("json4ocr.parse_ocr_result")
    @mock.patch("json4ocr.scan_drms_folder")
    def test_json4ocr(self, mocked_scan_drms_folder, mocked_parse_ocr_result):
        """
        Unit: Tests json4ocr function logic.
        """
        ocr_result = open_file(self.OCR_RESULTS_FILE_PATH + "ocr_1.txt")
        drms_path = "./drms"

        mocked_drms_1 = {"test": 1}
        mocked_drms_2 = {"test": 2}

        mocked_scan_drms_folder.return_value = [mocked_drms_1, mocked_drms_2]
        mocked_parse_ocr_result.return_value = "test_parsed_ocr_result"

        self.assertEqual(
            json4ocr(ocr_result, drms_path), "test_parsed_ocr_result"
        )

        mocked_scan_drms_folder.assert_called_once_with(drms_path)
        mocked_parse_ocr_result.assert_called_once_with(
            ocr_result, [mocked_drms_1, mocked_drms_2]
        )
