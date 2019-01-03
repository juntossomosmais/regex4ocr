"""
Unit tests for the DRM (Doc regex model) scanner module.
"""
from unittest import mock

import pytest

from regex4ocr.parser.drm_scanner import (
    get_all_drms_match,
    has_drm_match,
    scan_drms_folder,
)
from regex4ocr.parser.yml_parser import parse_yml
from tests.data.aux import open_file


@pytest.fixture(scope="module")
def ocr_result_tax_coupon_1():
    """ OCR test data for tax coupon 1."""
    OCR_TEST_RESULT_FOLDER = "./tests/data/ocr_results/"

    ocr_result = open_file(OCR_TEST_RESULT_FOLDER + "tax_coupon_1.txt")

    return ocr_result


@pytest.fixture(scope="module")
def ocr_result_no_match_1():
    """ OCR test data for unknown receipt structure."""
    OCR_TEST_RESULT_FOLDER = "./tests/data/ocr_results/"

    ocr_result = open_file(OCR_TEST_RESULT_FOLDER + "no_match_1.txt")

    return ocr_result


@pytest.fixture(scope="module")
def ocr_result_sat_coupon_1():
    """ OCR test data for a sat coupon 1. """
    OCR_TEST_RESULT_FOLDER = "./tests/data/ocr_results/"

    ocr_result = open_file(OCR_TEST_RESULT_FOLDER + "sat_coupon_1.txt")

    return ocr_result


@pytest.fixture(scope="module")
def drm_model_tax_coupon_1():
    """ DRM dict model for tax coupon. """
    DRM_TEST_YML_FOLDER = "./tests/data/drms/"

    drm = parse_yml(DRM_TEST_YML_FOLDER + "drm_tax_coupon_1.yml")

    return drm


@pytest.fixture(scope="module")
def drm_model_no_match_1():
    """ DRM dict model for an unknown coupon. """
    DRM_TEST_YML_FOLDER = "./tests/data/drms/"

    drm = parse_yml(DRM_TEST_YML_FOLDER + "drm_no_match_1.yml")

    return drm


@pytest.fixture(scope="module")
def drm_model_sat_coupon_1():
    """ DRM dict model for sat coupon. """
    DRM_TEST_YML_FOLDER = "./tests/data/drms/"

    drm = parse_yml(DRM_TEST_YML_FOLDER + "drm_sat_coupon_1.yml")

    return drm


def test_has_drm_match_with_matching_regexp_identifier(
    ocr_result_tax_coupon_1, drm_model_tax_coupon_1
):
    """
    Unit: tests if a tax coupon ocr result gets matched with a tax coupon DRM.
    """
    # method invocation
    assert has_drm_match(ocr_result_tax_coupon_1, drm_model_tax_coupon_1)


def test_has_drm_match_with_no_matching_regexp_identifier(
    ocr_result_tax_coupon_1, drm_model_no_match_1
):
    """
    Unit: tests if a tax coupon ocr result does not get matched
        with an unknown DRM.
    """
    # method invocation
    assert not has_drm_match(ocr_result_tax_coupon_1, drm_model_no_match_1)


def test_sat_coupon_has_sat_drm_match(
    ocr_result_tax_coupon_1,
    ocr_result_sat_coupon_1,
    drm_model_tax_coupon_1,
    drm_model_sat_coupon_1,
):
    """
    Unit: tests if a tax coupon does not get matched by an sat DRM due to many
    identifiers.
    """
    # tax coupon does not match the SAT DRM due to two identifiers
    assert not has_drm_match(ocr_result_tax_coupon_1, drm_model_sat_coupon_1)

    # sat coupon gets matched by the SAT DRM due to the presence
    # of the two matching identifiers
    assert has_drm_match(ocr_result_sat_coupon_1, drm_model_sat_coupon_1)


def test_get_all_drms_match(
    ocr_result_tax_coupon_1,
    drm_model_tax_coupon_1,
    drm_model_sat_coupon_1,
    drm_model_no_match_1,
):
    """
    Unit: tests that only the tax coupon DRM remains as a match for the ocr tax
          coupon result.
    """
    drms = [
        drm_model_tax_coupon_1,
        drm_model_sat_coupon_1,
        drm_model_no_match_1,
    ]

    assert get_all_drms_match(ocr_result_tax_coupon_1, drms) == [
        drm_model_tax_coupon_1
    ]


def test_scan_drms_folder(
    drm_model_tax_coupon_1, drm_model_sat_coupon_1, drm_model_no_match_1
):
    """
    Unit: tests that all the drms on the given folder get properly scanned and
          translated from yml to dictionary (valid ones only).
    """
    DRM_SCANNER_TEST_YML_FOLDER = "./tests/data/drms_scanner/"

    # method invocation
    all_drms = scan_drms_folder(DRM_SCANNER_TEST_YML_FOLDER)

    expected_drm_1 = parse_yml(DRM_SCANNER_TEST_YML_FOLDER + "drm_1.yml")
    expected_drm_2 = parse_yml(DRM_SCANNER_TEST_YML_FOLDER + "drm_2.yml")

    expected_drms = [expected_drm_1, expected_drm_2]

    assert all_drms == expected_drms
