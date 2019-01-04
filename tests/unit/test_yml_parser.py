"""
Module with unit tests for the yml parser function.
"""
import pytest

from regex4ocr.parser.yml_parser import parse_yml
import yaml


def test_yml_parser():
    """
    Unit: tests YML parsing.
    """
    BASE_YML_TEST_FOLDER = "./tests/data/drms/"

    expected_yml_dict = {
        "identifiers": ["id1", "id2"],
        "fields": {"test1": "key1", "test2": "key2"},
    }

    assert (
        parse_yml(BASE_YML_TEST_FOLDER + "drm_yml_parser.yml")
        == expected_yml_dict
    )


def test_yml_parser_raises_exception():
    """
    Unit: tests YML parsing.
    """
    BASE_YML_TEST_FOLDER = "./tests/data/drms/"

    print(parse_yml(BASE_YML_TEST_FOLDER + "drm_yml_parser_broken.yml"))

    assert parse_yml(BASE_YML_TEST_FOLDER + "drm_yml_parser_broken.yml") is None
