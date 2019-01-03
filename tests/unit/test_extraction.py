"""
Module with unit tests for the data extraction functions.
"""
import re
from unittest import mock

import pytest

from regex4ocr.parser.extraction import extract_fields, extract_table_data
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
