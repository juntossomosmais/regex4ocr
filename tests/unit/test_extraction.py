"""
Module with unit tests for the data extraction functions.
"""
import re
from unittest import mock

import pytest

from regex4ocr.parser.extraction import (
    extract_fields,
    extract_ocr_data,
    extract_table_data,
    get_table_rows,
)
from regex4ocr.parser.yml_parser import parse_yml
from tests.data.aux import open_file


@pytest.fixture(scope="module")
def pre_processed_tax_coupon_1():
    """ OCR test data for tax coupon 1."""
    OCR_TEST_RESULT_FOLDER = "./tests/data/ocr_results/"

    ocr_result = open_file(
        OCR_TEST_RESULT_FOLDER + "tax_coupon_preprocessed_1.txt"
    )

    return ocr_result


@pytest.fixture(scope="module")
def pre_processed_tax_coupon_2():
    """ OCR test data for tax coupon 1."""
    OCR_TEST_RESULT_FOLDER = "./tests/data/ocr_results/"

    ocr_result = open_file(
        OCR_TEST_RESULT_FOLDER + "tax_coupon_preprocessed_2.txt"
    )

    return ocr_result


@pytest.fixture(scope="module")
def drm_model_tax_coupon_1():
    """ DRM dict model for tax coupon. """
    DRM_TEST_YML_FOLDER = "./tests/data/drms/"

    drm = parse_yml(DRM_TEST_YML_FOLDER + "drm_tax_coupon_1.yml")

    return drm


@pytest.fixture(scope="module")
def table_data():
    all_rows = """
    17273 breit grossa 7mts" bunx373 ft 288 026
    2 $17 pedra 1 (ht) 2unx84 694 f1
    169 38g
    003 515 cimento votoran todas as obras 50 kg
    cred)
    boun x 26.489 f1
    794,676
    """

    headers = """iten codigo descricao qid un vl unit r$ ) st vl item(r$)"""
    footer = """total r$"""
    all_rows = re.sub("    ", "", all_rows)

    table_data = {"header": headers, "all_rows": all_rows, "footer": footer}

    return table_data


def test_extract_fields_with_match_group(
    pre_processed_tax_coupon_1, drm_model_tax_coupon_1
):
    """
    Unit: tests field extraction of the OCR result string.
    """
    expected_data = {
        "cnpj": "12.345.678/1234-12",
        "coo": "047621",
        "date": "10/08/2018 17:55:55",
    }

    assert (
        extract_fields(pre_processed_tax_coupon_1, drm_model_tax_coupon_1)
        == expected_data
    )


def test_extract_fields_without_matches(
    pre_processed_tax_coupon_2, drm_model_tax_coupon_1
):
    """
    Unit: tests field extraction of the OCR result string without matches.
    """
    expected_data = {}

    assert (
        extract_fields(pre_processed_tax_coupon_2, drm_model_tax_coupon_1)
        == expected_data
    )


def test_extract_table_data(pre_processed_tax_coupon_1, drm_model_tax_coupon_1):
    """
    Unit: tests table data extraction.
    """
    # expected_table_data
    all_rows = """
    17273 breit grossa 7mts" bunx373 ft 288 026
    2 $17 pedra 1 (ht) 2unx84 694 f1
    169 38g
    003 515 cimento votoran todas as obras 50 kg
    cred)
    boun x 26.489 f1
    794,676
    """

    headers = """iten codigo descricao qid un vl unit r$ ) st vl item(r$)"""
    footer = """total r$"""
    all_rows = re.sub("    ", "", all_rows)

    expected_table_data = {
        "header": headers,
        "all_rows": all_rows,
        "footer": footer,
    }

    assert (
        extract_table_data(pre_processed_tax_coupon_1, drm_model_tax_coupon_1)
        == expected_table_data
    )


def test_get_table_rows_without_match(table_data):
    """
    Unit: tests table row extraction when there's no line_start regexp match.
    """
    drm_no_match = {"table": {"line_start": "no_regex_match"}}
    all_rows = table_data["all_rows"]

    # method invocation
    assert get_table_rows(all_rows, drm_no_match) == []


def test_get_table_rows_with_match(table_data):
    """
    Unit: tests table row extraction when there are line_start regexp match.
    """
    drm = {"table": {"line_start": r"\n\d+\s+(\d+)?"}}
    all_rows = table_data["all_rows"]

    expected_rows = [
        '17273 breit grossa 7mts" bunx373 ft 288 026',
        "2 $17 pedra 1 (ht) 2unx84 694 f1",
        "169 38g",
        # last row matches until the end of the all_rows string
        "003 515 cimento votoran todas as obras 50 kgcred)boun x 26.489 f1794,676",
    ]

    # method invocation
    assert get_table_rows(all_rows, drm) == expected_rows


@mock.patch("regex4ocr.parser.extraction.get_table_rows")
@mock.patch("regex4ocr.parser.extraction.extract_table_data")
@mock.patch("regex4ocr.parser.extraction.extract_fields")
def test_extract_ocr_data_table_match_rows_match(
    mocked_extract_fields, mocked_extract_table_data, mocked_get_table_rows
):
    """
    Unit: tests the overall ocr data extraction function where there is
          a table_data match and rows matches.
    """
    # mock results
    mocked_fields = {"field1": "result1", "field2": "result2"}

    mocked_table_data = {
        "header": "test",
        "all_rows": "row1 row2 row3",
        "footer": "footer",
    }

    mocked_table_rows = ["row1", "row2", "row3"]

    mocked_extract_fields.return_value = mocked_fields
    mocked_extract_table_data.return_value = mocked_table_data
    mocked_get_table_rows.return_value = mocked_table_rows

    expected_extracted_data = {
        "fields": mocked_fields,
        "table": mocked_table_data,
    }

    expected_extracted_data["table"]["rows"] = mocked_table_rows

    # method invocation
    assert (
        extract_ocr_data("ocr result", {"test": "test"})
        == expected_extracted_data
    )

    # mock assertions
    mocked_extract_fields.assert_called_once_with(
        "ocr result", {"test": "test"}
    )

    mocked_extract_table_data.return_assert_called_once_with(
        "ocr result", {"test": "test"}
    )

    mocked_get_table_rows.assert_called_once_with(
        mocked_table_data["all_rows"], {"test": "test"}
    )


@mock.patch("regex4ocr.parser.extraction.get_table_rows")
@mock.patch("regex4ocr.parser.extraction.extract_table_data")
@mock.patch("regex4ocr.parser.extraction.extract_fields")
def test_extract_ocr_data_table_match_rows_no_match(
    mocked_extract_fields, mocked_extract_table_data, mocked_get_table_rows
):
    """
    Unit: tests the overall ocr data extraction function where there is
          a table_data match but no row regexp matches.
    """
    # mock results
    mocked_fields = {"field1": "result1", "field2": "result2"}

    mocked_table_data = {
        "header": "test",
        "all_rows": "row1 row2 row3",
        "footer": "footer",
    }

    mocked_table_rows = []  # no row matches

    mocked_extract_fields.return_value = mocked_fields
    mocked_extract_table_data.return_value = mocked_table_data
    mocked_get_table_rows.return_value = mocked_table_rows

    expected_extracted_data = {
        "fields": mocked_fields,
        "table": mocked_table_data,
    }

    expected_extracted_data["table"]["rows"] = mocked_table_rows  # [] now

    # method invocation
    assert (
        extract_ocr_data("ocr result", {"test": "test"})
        == expected_extracted_data
    )

    # mock assertions
    mocked_extract_fields.assert_called_once_with(
        "ocr result", {"test": "test"}
    )

    mocked_extract_table_data.return_assert_called_once_with(
        "ocr result", {"test": "test"}
    )

    mocked_get_table_rows.assert_called_once_with(
        mocked_table_data["all_rows"], {"test": "test"}
    )


@mock.patch("regex4ocr.parser.extraction.get_table_rows")
@mock.patch("regex4ocr.parser.extraction.extract_table_data")
@mock.patch("regex4ocr.parser.extraction.extract_fields")
def test_extract_ocr_data_no_table_match(
    mocked_extract_fields, mocked_extract_table_data, mocked_get_table_rows
):
    """
    Unit: tests the overall ocr data extraction function where there is
          no table_data match.
    """
    # mock results
    mocked_fields = {"field1": "result1", "field2": "result2"}

    mocked_table_data = {}

    mocked_extract_fields.return_value = mocked_fields
    mocked_extract_table_data.return_value = mocked_table_data

    expected_extracted_data = {
        "fields": mocked_fields,
        "table": mocked_table_data,
    }

    # method invocation
    assert (
        extract_ocr_data("ocr result", {"test": "test"})
        == expected_extracted_data
    )

    # mock assertions
    mocked_extract_fields.assert_called_once_with(
        "ocr result", {"test": "test"}
    )

    mocked_extract_table_data.return_assert_called_once_with(
        "ocr result", {"test": "test"}
    )

    # no row extraction if there is no table
    mocked_get_table_rows.assert_not_called()
