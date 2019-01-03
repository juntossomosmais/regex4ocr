"""
Module with unit tests for the pre processing functions.
"""
from unittest import mock

import pytest

from regex4ocr.parser.pre_process import (
    apply_options,
    pre_process_result,
    process_replaces,
)


@pytest.fixture(scope="module")
def pre_process_str():
    """
    Returns a pre processed str for testing.
    """
    pre_process_str = """
    Nota fiscal
    c00: 123
    codigo descricao qtd
    001--- prod A 3un
    002 prod B b0un
    """

    return pre_process_str


@pytest.fixture(scope="module")
def pre_process_str_non_ascii():
    """
    Returns a pre processed str for testing.
    """
    pre_process_str = """
    Nota fiscal
    c00: 123
    código descrição qtd
    001--- prod A 3un
    002 prod B b0un
    """

    return pre_process_str


def test_pre_process_replace(pre_process_str):
    """
    Unit: OCR string pre processing of the replaces.
    """
    expected_str = """
    Nota fiscal
    coo: 123
    codigo descricao qtd
    001 prod A 3un
    002 prod B 30un
    """

    replaces = [["c00", "coo"], ["b0un", "30un"], ["-+", ""]]

    assert process_replaces(pre_process_str, replaces) == expected_str


def test_apply_options_lowercase(pre_process_str):
    """
    Unit: tests lowercase option pre processing.
    """
    options = {
        "lowercase": True,
        "remove_whitespace": False,
        "force_ascii": False,
        "replaces": [["c00", "coo"]],
    }

    # replacing is the last option
    expected_str = """
    nota fiscal
    c00: 123
    codigo descricao qtd
    001--- prod a 3un
    002 prod b b0un
    """

    assert apply_options(pre_process_str, options) == expected_str


def test_apply_options_remove_lowercase_whitespace(pre_process_str):
    """
    Unit: tests remove whitespace option.
    """
    options = {
        "lowercase": True,
        "remove_whitespace": True,
        "force_ascii": False,
        "replaces": [["c00", "coo"]],
    }

    # replacing is the last option
    expected_str = (
        """notafiscalc00:123codigodescricaoqtd001---proda3un002prodbb0un"""
    )

    assert apply_options(pre_process_str, options) == expected_str


def test_apply_options_lowercase_force_ascii(pre_process_str_non_ascii):
    """
    Unit: tests force ascii with unidecode.
    """
    options = {
        "lowercase": True,
        "remove_whitespace": False,
        "force_ascii": True,
        "replaces": [["c00", "coo"]],
    }

    # replacing is the last option
    expected_str = """
    nota fiscal
    c00: 123
    codigo descricao qtd
    001--- prod a 3un
    002 prod b b0un
    """

    assert apply_options(pre_process_str_non_ascii, options) == expected_str


@mock.patch("regex4ocr.parser.pre_process.apply_options")
def test_pre_process_result(mocked_apply_options, pre_process_str):
    """
    Unit: pre process results overall.
    """
    mocked_apply_options.return_value = "pre_processed_str"
    mocked_options = mock.Mock()

    drm = {"options": mocked_options}

    # method invocation
    assert pre_process_result(pre_process_str, drm) == "pre_processed_str"
