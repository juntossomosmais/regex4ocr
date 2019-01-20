"""
Module with unit tests for the data extraction functions.
"""
import re
from unittest import mock

import pytest

from regex4ocr.parser.extraction import extract_fields
from regex4ocr.parser.extraction import extract_ocr_data
from regex4ocr.parser.extraction import extract_row_named_groups
from regex4ocr.parser.extraction import extract_table_data
from regex4ocr.parser.extraction import get_table_rows
from regex4ocr.parser.extraction import get_uniqueness_fields
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
def drm_model_tax_coupon_with_inline_named_groups_1():
    """ DRM dict model for tax coupon. """
    DRM_TEST_YML_FOLDER = "./tests/data/drms/"

    drm = parse_yml(DRM_TEST_YML_FOLDER + "drm_inline_named_groups_1.yml")

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


@mock.patch("regex4ocr.parser.extraction.extract_row_named_groups")
@mock.patch("regex4ocr.parser.extraction.get_table_rows")
@mock.patch("regex4ocr.parser.extraction.extract_table_data")
@mock.patch("regex4ocr.parser.extraction.extract_fields")
def test_extract_ocr_data_table_match_rows_match(
    mocked_extract_fields,
    mocked_extract_table_data,
    mocked_get_table_rows,
    mocked_extract_row_named_groups,
):
    """
    Unit: tests the overall ocr data extraction function where there is
          a table_data match and rows matches.
    """
    drm = {"test": "test"}

    # mock results
    mocked_fields = {"field1": "result1", "field2": "result2"}

    mocked_table_data = {
        "header": "test",
        "all_rows": "row1 row2 row3",
        "footer": "footer",
    }

    mocked_table_rows = ["row1", "row2", "row3"]
    mocked_row_named_groups = [
        {"row": "row1", "data": {"group_1": "value_1"}},
        {"row": "row2", "data": {"group_1": "value_1"}},
        {"row": "row3", "data": {"group_1": "value_1"}},
    ]

    mocked_extract_fields.return_value = mocked_fields
    mocked_extract_table_data.return_value = mocked_table_data
    mocked_get_table_rows.return_value = mocked_table_rows
    mocked_extract_row_named_groups.side_effect = mocked_row_named_groups

    expected_extracted_data = {
        "fields": mocked_fields,
        "table": mocked_table_data,
    }

    expected_extracted_data["table"]["rows"] = mocked_row_named_groups

    # method invocation
    assert extract_ocr_data("ocr result", drm) == expected_extracted_data

    # mock assertions
    mocked_extract_fields.assert_called_once_with("ocr result", drm)

    mocked_extract_table_data.return_assert_called_once_with("ocr result", drm)

    mocked_get_table_rows.assert_called_once_with(
        mocked_table_data["all_rows"], drm
    )

    mocked_extract_row_named_groups.return_value.assert_has_calls = [
        mock.call("row1", drm),
        mock.call("row2", drm),
        mock.call("row3", drm),
    ]


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


def test_extract_row_named_groups_no_group_names(drm_model_tax_coupon_1):
    """
    Unit: tests extract_row_named_groups when there are no regexp groups in the DRM.
    """
    row_1 = "17273 breit grossa 7mts bunx373 ft 288 026"
    row_2 = "2 $17 pedra 1 (ht) 2unx84 694 f1"

    expected_row_1 = {
        "row": "17273 breit grossa 7mts bunx373 ft 288 026",
        "data": {},  # no named groups
    }

    expected_row_2 = {
        "row": "2 $17 pedra 1 (ht) 2unx84 694 f1",
        "data": {},  # no named groups
    }

    # method invocation
    assert (
        extract_row_named_groups(row_1, drm_model_tax_coupon_1)
        == expected_row_1
    )
    assert (
        extract_row_named_groups(row_2, drm_model_tax_coupon_1)
        == expected_row_2
    )


def test_extract_row_named_groups_with_inline_regexp(
    drm_model_tax_coupon_with_inline_named_groups_1
):
    """
    Unit: tests extract_row_named_groups when there are in regexp groups in the DRM.
    """
    row_1 = "17273 breit grossa 7mts bunx373 ft 288 026"
    row_2 = "2 $17 pedra 1 (ht) 2unx84 694 f1"

    expected_row_1 = {
        "row": "17273 breit grossa 7mts bunx373 ft 288 026",
        "data": {},
    }

    expected_row_2 = {
        "row": "2 $17 pedra 1 (ht) 2unx84 694 f1",
        "data": {
            "description": "2 $17 pedra 1 (ht) ",
            "qty": "2",
            "unit": "un",
        },
    }

    # method invocation
    assert (
        extract_row_named_groups(
            row_1, drm_model_tax_coupon_with_inline_named_groups_1
        )
        == expected_row_1
    )
    assert (
        extract_row_named_groups(
            row_2, drm_model_tax_coupon_with_inline_named_groups_1
        )
        == expected_row_2
    )


@mock.patch("regex4ocr.parser.extraction.extract_row_named_groups")
@mock.patch("regex4ocr.parser.extraction.get_table_rows")
@mock.patch("regex4ocr.parser.extraction.extract_table_data")
@mock.patch("regex4ocr.parser.extraction.extract_fields")
def test_extract_ocr_data_table_match_rows_match_uniqueness(
    mocked_extract_fields,
    mocked_extract_table_data,
    mocked_get_table_rows,
    mocked_extract_row_named_groups,
):
    """
    Unit: tests the overall ocr data extraction function where there is
          a table_data match and rows matches and there are uniqueness fields.
    """
    drm = {"test": "test", "uniqueness_fields": ["field1"]}

    # mock results (field1 is a uniquess field)
    mocked_fields = {"field1": "result1", "field2": "result2"}

    mocked_table_data = {
        "header": "test",
        "all_rows": "row1 row2 row3",
        "footer": "footer",
    }

    mocked_table_rows = ["row1", "row2", "row3"]
    mocked_row_named_groups = [
        {"row": "row1", "data": {"group_1": "value_1"}},
        {"row": "row2", "data": {"group_1": "value_1"}},
        {"row": "row3", "data": {"group_1": "value_1"}},
    ]

    mocked_extract_fields.return_value = mocked_fields
    mocked_extract_table_data.return_value = mocked_table_data
    mocked_get_table_rows.return_value = mocked_table_rows
    mocked_extract_row_named_groups.side_effect = mocked_row_named_groups

    expected_extracted_data = {
        "fields": mocked_fields,
        "table": mocked_table_data,
        "uniqueness_fields": {"field1": "result1"},
    }

    expected_extracted_data["table"]["rows"] = mocked_row_named_groups

    # method invocation
    assert extract_ocr_data("ocr result", drm) == expected_extracted_data

    # mock assertions
    mocked_extract_fields.assert_called_once_with("ocr result", drm)

    mocked_extract_table_data.return_assert_called_once_with("ocr result", drm)

    mocked_get_table_rows.assert_called_once_with(
        mocked_table_data["all_rows"], drm
    )

    mocked_extract_row_named_groups.return_value.assert_has_calls = [
        mock.call("row1", drm),
        mock.call("row2", drm),
        mock.call("row3", drm),
    ]

@mock.patch("regex4ocr.parser.extraction.extract_row_named_groups")
@mock.patch("regex4ocr.parser.extraction.get_table_rows")
@mock.patch("regex4ocr.parser.extraction.extract_table_data")
@mock.patch("regex4ocr.parser.extraction.extract_fields")
def test_extract_ocr_data_uniqueness_not_found(
    mocked_extract_fields,
    mocked_extract_table_data,
    mocked_get_table_rows,
    mocked_extract_row_named_groups,
):
    """
    Unit: tests the overall ocr data extraction function where there is
          a table_data match and rows matches and there are uniqueness fields.
    """
    drm = {"test": "test", "uniqueness_fields": ["field99"]}

    # mock results (field1 is a uniquess field)
    mocked_fields = {"field1": "result1", "field2": "result2"}

    mocked_table_data = {
        "header": "test",
        "all_rows": "row1 row2 row3",
        "footer": "footer",
    }

    mocked_table_rows = ["row1", "row2", "row3"]
    mocked_row_named_groups = [
        {"row": "row1", "data": {"group_1": "value_1"}},
        {"row": "row2", "data": {"group_1": "value_1"}},
        {"row": "row3", "data": {"group_1": "value_1"}},
    ]

    mocked_extract_fields.return_value = mocked_fields
    mocked_extract_table_data.return_value = mocked_table_data
    mocked_get_table_rows.return_value = mocked_table_rows
    mocked_extract_row_named_groups.side_effect = mocked_row_named_groups

    expected_extracted_data = {
        "fields": mocked_fields,
        "table": mocked_table_data,
        "uniqueness_fields": {"field1": "result1"},
    }

    expected_extracted_data["table"]["rows"] = mocked_row_named_groups

    # method invocation
    assert extract_ocr_data("ocr result", drm) == {}  # uniqueness fields fail

    # mock assertions
    mocked_extract_fields.assert_called_once_with("ocr result", drm)

    mocked_extract_table_data.return_assert_called_once_with("ocr result", drm)

    mocked_get_table_rows.assert_called_once_with(
        mocked_table_data["all_rows"], drm
    )

    mocked_extract_row_named_groups.return_value.assert_has_calls = [
        mock.call("row1", drm),
        mock.call("row2", drm),
        mock.call("row3", drm),
    ]


def test_get_uniqueness_fields_ok():
    """
    Unit: asserts that all unique fields are returned when found.
    """
    fields_section = {"k1": 1, "k2": 2, "k3": 3}

    uniqueness_fields = ["k1", "k3"]

    expected_data = {"k1": 1, "k3": 3}

    assert (
        get_uniqueness_fields(fields_section, uniqueness_fields)
        == expected_data
    )


def test_get_uniqueness_fields_not_found():
    """
    Unit: asserts an empty dict is returned when a unique field is not found.
    """
    fields_section = {"k1": 1, "k2": 2, "k3": 3}

    uniqueness_fields = ["k1", "k3", "k7"]

    assert get_uniqueness_fields(fields_section, uniqueness_fields) == {}


def test_get_uniqueness_fields_excepion():
    """
    Unit: asserts an exception is raised when uniqueness fields is NOT a list.
    """
    fields_section = {"k1": 1, "k2": 2, "k3": 3}

    uniqueness_fields = "whatever"

    with pytest.raises(BaseException):
        get_uniqueness_fields(fields_section, uniqueness_fields)
