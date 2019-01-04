"""
Module with unit tests for the parser module.
"""
from unittest import mock

from regex4ocr.parser.parser import parse_ocr_result


@mock.patch("regex4ocr.parser.parser.extract_ocr_data")
@mock.patch("regex4ocr.parser.parser.pre_process_result")
@mock.patch("regex4ocr.parser.parser.get_all_drms_match")
def test_parse_ocr_result_with_drms(
    mocked_get_all_drms_match,
    mocked_pre_process_result,
    mocked_extract_ocr_data,
):
    """
    Unit: tests parsing function if DRM matches this document.
    """
    drm1 = {"test1": "value1"}

    drm2 = {"test2": "value2"}

    drms = [drm1, drm2]

    extracted_data = {"fields": {"field1": "value1"}}

    # mock returns
    mocked_get_all_drms_match.return_value = drms
    mocked_pre_process_result.return_value = "pre processed result"
    mocked_extract_ocr_data.return_value = extracted_data

    # method invocation
    assert parse_ocr_result("ocr result", drms) == extracted_data

    # mock assertions
    mocked_get_all_drms_match.assert_called_once_with("ocr result", drms)
    mocked_pre_process_result.assert_called_once_with(
        "ocr result", drm1
    )  # first drm
    mocked_extract_ocr_data.assert_called_once_with(
        "pre processed result", drm1
    )


@mock.patch("regex4ocr.parser.parser.extract_ocr_data")
@mock.patch("regex4ocr.parser.parser.pre_process_result")
@mock.patch("regex4ocr.parser.parser.get_all_drms_match")
def test_parse_ocr_result_no_drm_match(
    mocked_get_all_drms_match,
    mocked_pre_process_result,
    mocked_extract_ocr_data,
):
    """
    Unit: tests parsing function if no DRM identifiers match
          the document.
    """
    drm1 = {"test1": "value1"}

    drm2 = {"test2": "value2"}

    drms = [drm1, drm2]

    # mock returns
    mocked_get_all_drms_match.return_value = []  # no DRMs match

    # method invocation
    assert parse_ocr_result("ocr result", drms) == {}

    # mock assertions
    mocked_get_all_drms_match.assert_called_once_with("ocr result", drms)
    mocked_pre_process_result.assert_not_called()
    mocked_extract_ocr_data.assert_not_called()
