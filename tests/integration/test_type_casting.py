"""
Module with unit tests for the data type casting functions
"""
import copy
from unittest import mock

import pytest

from regex4ocr.parser.type_casting import cast_type
from regex4ocr.parser.type_casting import remove_wrong_types
from regex4ocr.parser.type_casting import validate_types
from regex4ocr.parser.yml_parser import parse_yml
from tests.data.aux import open_file


@pytest.fixture(scope="module")
def pre_processed_tax_coupon_2():
    """ OCR test data for tax coupon 3."""
    OCR_TEST_RESULT_FOLDER = "./tests/data/ocr_results/"

    ocr_result = open_file(
        OCR_TEST_RESULT_FOLDER + "tax_coupon_preprocessed_3.txt"
    )

    return ocr_result


@pytest.fixture(scope="module")
def drm_model_tax_coupon_with_inline_groups():
    """ DRM dict model for tax coupon. """
    DRM_TEST_YML_FOLDER = "./tests/data/drms/"

    drm = parse_yml(DRM_TEST_YML_FOLDER + "drm_inline_named_groups_1.yml")

    return drm


@pytest.fixture(scope="module")
def extracted_data_dict_1():
    return {
        "fields": {
            "cnpj": "10.549.937/000174",
            "date": "10/08/1991",
            "coo": "047621",
            "some_int": "1234",
        },
        "table": {
            "header": "iten codigo descricao qid1un vl1unit r$ ) st vl item(r$)",
            "all_rows": '\n17273 breit grossa 7mts" 3unx373 ft 288 026\n2 $17 pedra 1 (ht) 2unx84 694 f1\n169 38g\n003 515 cimento votoran todas as obras 50 kg\ncred)\n30un x 26.489 f1\n794,676\n',
            "footer": "total r$",
            "rows": [
                {
                    "row": '17273 breit grossa 7mts" 3unx373 ft 288 0262 $17 pedra 1 (ht) 2unx84 694 f1',
                    "data": {
                        "description": '17273 breit grossa 7mts" ',
                        "qty": "3",
                        "unit": "un",
                    },
                },
                {"row": "169 38g", "data": {}},
                {
                    "row": "003 515 cimento votoran todas as obras 50 kgcred)30un x 26.489 f1794,676",
                    "data": {
                        "description": "003 515 cimento votoran todas as obras 50 kgcred)",
                        "qty": "30",
                        "unit": "un",
                    },
                },
            ],
        },
    }


@pytest.fixture(scope="module")
def expected_extracted_data_dict_no_removal():
    return {
        "fields": {
            "cnpj": "10.549.937/000174",
            "coo": "047621",
            "date": "1991-08-10T00:00:00",  # cast to iso format
            "some_int": 1234,  # casting
        },
        "table": {
            "header": "iten codigo descricao qid1un vl1unit r$ ) st vl item(r$)",
            "all_rows": '\n17273 breit grossa 7mts" 3unx373 ft 288 026\n2 $17 pedra 1 (ht) 2unx84 694 f1\n169 38g\n003 515 cimento votoran todas as obras 50 kg\ncred)\n30un x 26.489 f1\n794,676\n',
            "footer": "total r$",
            "rows": [
                {
                    "row": '17273 breit grossa 7mts" 3unx373 ft 288 0262 $17 pedra 1 (ht) 2unx84 694 f1',
                    "data": {
                        "description": '17273 breit grossa 7mts" ',
                        "qty": 3,
                        "unit": "un",
                    },
                },
                {"row": "169 38g", "data": {}},
                {
                    "row": "003 515 cimento votoran todas as obras 50 kgcred)30un x 26.489 f1794,676",
                    "data": {
                        "description": "003 515 cimento votoran todas as obras 50 kgcred)",
                        "qty": 30,
                        "unit": "un",
                    },
                },
            ],
        },
    }


@pytest.fixture(scope="module")
def expected_extracted_data_dict_with_removal():
    return {
        "fields": {
            "cnpj": "10.549.937/000174",
            "coo": "047621",
            # "some_int": "1234",
            # "date": "10/08/1991",
        },
        "table": {
            "header": "iten codigo descricao qid1un vl1unit r$ ) st vl item(r$)",
            "all_rows": '\n17273 breit grossa 7mts" 3unx373 ft 288 026\n2 $17 pedra 1 (ht) 2unx84 694 f1\n169 38g\n003 515 cimento votoran todas as obras 50 kg\ncred)\n30un x 26.489 f1\n794,676\n',
            "footer": "total r$",
            "rows": [
                {
                    "row": '17273 breit grossa 7mts" 3unx373 ft 288 0262 $17 pedra 1 (ht) 2unx84 694 f1',
                    "data": {
                        "description": '17273 breit grossa 7mts" ',
                        "qty": 3,
                        "unit": "un",
                    },
                },
                {"row": "169 38g", "data": {}},
                {
                    "row": "003 515 cimento votoran todas as obras 50 kgcred)30un x 26.489 f1794,676",
                    "data": {
                        "description": "003 515 cimento votoran todas as obras 50 kgcred)",
                        "qty": 30,
                        "unit": "un",
                    },
                },
            ],
        },
    }


def test_cast_type_exception_unknown_drm_type():
    """
    Unit: tests cast_type when there's an unsupported or unknown type at the
          DRM yml file.
    """
    with pytest.raises(BaseException):
        cast_type("1234", "unknown_type")


def test_cast_type_int_type():
    """
    Unit: tests cast_type when there's a correct cast to an int type.
    """
    assert cast_type("1234", "int") == 1234


def test_cast_type_datetime_type_exception():
    """
    Unit: tests cast_type when there's an impossible cast to datetime.
    """
    assert cast_type("10/08/1991", ["datetime", "abc"]) is None


def test_cast_type_datetime_type_ok():
    """
    Unit: tests cast_type when there's a correct cast to a datetime type.
    """
    assert (
        cast_type("10/08/1991", ["datetime", "%d/%m/%Y"])
        == "1991-08-10T00:00:00"
    )


def test_cast_type_datetime_wrong_list_length():
    """
    Unit: tests cast_type when there's missing datetime metadata
          for the type cast.
    """
    with pytest.raises(BaseException):
        cast_type("10/08/1991", ["datetime"])


def test_cast_type_datetime_no_timestamp():
    """
    Unit: tests cast_type when the datetime metadata contains no
          timestamp info.
    """
    assert cast_type("10/08/1991", ["datetime", "%d/%m/%Y %H:%M:%S"]) is None


def test_cast_type_metadata_unknown():
    """
    Unit: tests cast_type when the desired type is a list with unknown type.
    """
    with pytest.raises(BaseException):
        cast_type("10/08/1991", ["unknown_type", "whatever"])


def test_cast_type_value_exception():
    """
    Unit: tests cast_type when there's raised ValueError.
    """
    assert cast_type("123.144-5566/12345-6", "int") is None


def test_remove_wrong_types_no_removal(
    extracted_data_dict_1, drm_model_tax_coupon_with_inline_groups
):
    """
    Unit: tests cast_type when all the type casts run smoothly.
    """
    # sends only the fields section
    extracted_data_section = {
        "cnpj": "10.549.937/000174",
        "coo": "047621",
        "date": "10/08/1991",
        "some_int": "1234",
    }

    # types > fields
    drm_types_section = {
        "cnpj": "str",
        # "coo": "047621", # not inserted
        "some_int": "int",
        "date": ["datetime", "%d/%m/%Y"],
    }

    expected_extracted_data_dict = {
        "cnpj": "10.549.937/000174",
        "coo": "047621",  # since there was no typing, remains as is
        "date": "1991-08-10T00:00:00",
        "some_int": 1234,
    }

    # function invocation which mutates extracted_data_section
    remove_wrong_types(extracted_data_section, drm_types_section)
    assert extracted_data_section == expected_extracted_data_dict


def test_remove_wrong_types_with_removal(
    drm_model_tax_coupon_with_inline_groups
):
    """
    Unit: tests cast_type when there's an unsupported or unknown type at the
          DRM yml file.
    """
    extracted_data_section = {
        "cnpj": "10.549.937/000174",
        "coo": "047621",
        "some_int": "1234xxnotanint",  # not an integer
        "date": "123/10/2018",  # broken date
    }

    drm_types_section = {
        "cnpj": "str",
        "coo": "str",
        "some_int": "int",
        "date": ["datetime", "%d/%m/%Y"],
    }

    expected_extracted_data_dict = {
        "cnpj": "10.549.937/000174",
        "coo": "047621",
        # "some_int": "1234",  # raises ValueError and must be removed
    }

    # function invocation
    remove_wrong_types(extracted_data_section, drm_types_section)

    assert extracted_data_section == expected_extracted_data_dict


def test_validate_types_no_removal(
    extracted_data_dict_1,
    expected_extracted_data_dict_no_removal,
    drm_model_tax_coupon_with_inline_groups,
):
    """
    Unit: tests validate_types when there are not type conflicts.
    """
    # function invocation
    extracted_data_dict_1 = copy.deepcopy(extracted_data_dict_1)
    validate_types(
        extracted_data_dict_1, drm_model_tax_coupon_with_inline_groups
    )

    assert extracted_data_dict_1 == expected_extracted_data_dict_no_removal


def test_validate_types_removal(
    extracted_data_dict_1,
    expected_extracted_data_dict_with_removal,
    drm_model_tax_coupon_with_inline_groups,
):
    """
    Unit: tests validate_types when there are type conflicts and
          some fields are removed.
    """
    # creates a deep copy of the fixture so mutations wont affect next tests
    extracted_data_dict = copy.deepcopy(extracted_data_dict_1)

    extracted_data_dict["fields"]["some_int"] = "abc123"  # messes int casting

    # function invocation
    validate_types(extracted_data_dict, drm_model_tax_coupon_with_inline_groups)

    assert extracted_data_dict == expected_extracted_data_dict_with_removal
