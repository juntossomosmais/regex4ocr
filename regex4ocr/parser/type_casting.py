"""
Module with type-casting related functions.
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_types(extracted_data, drm):
    """
    Performs data validation of the extracted_data according to the
    types informed at the drm for this document.
    """
    logger.info("Beginning types validation...")

    fields_types_section = drm.get("types", {}).get("fields", {})
    inline_groups_types_section = (
        drm.get("types", {}).get("table", {}).get("inline_named_group_captures")
    )
    rows = extracted_data.get("table", {}).get("rows")

    logger.info("Performing inline captured groups type casting...")

    if rows and inline_groups_types_section:
        # removes named groups if type casting fails
        for row_dict in rows:
            logger.debug(
                "Validating row data: %s, with the types: %s",
                row_dict["data"],
                inline_groups_types_section,
            )

            remove_wrong_types(row_dict["data"], inline_groups_types_section)

    # fields is always required
    if fields_types_section:
        logger.debug(
            "Validating fields: %s, with the types: %s",
            extracted_data["fields"],
            fields_types_section,
        )

        remove_wrong_types(extracted_data["fields"], fields_types_section)


def remove_wrong_types(extracted_data_section, drm_types_section):
    """
    Receives a portion (dict) of the parsed image receipt and a dict whose keys
    are the extracted_data_section keys and values are the are desired types for
    the extracted_data_section keys.

    If the cast of the extracted_data_section to the desired type fails, that
    key is POPPED from the original dictionary. Hence, this method MUTATES the
    original extracted_data_section.

    Args:
        extracted_data_section (dict): portion of the parsed data;
        drm_types_section (dict): dict whose keys are the fields of the
            extracted_data_section and values are the desired types.
    """
    for desired_field, desired_type in drm_types_section.items():
        # gets the target field from the data section, if exists
        extracted_field = extracted_data_section.get(desired_field)

        # the type has a matching desired_field
        if extracted_field:
            logger.debug(
                "Found cast: %s, to %s...", extracted_field, desired_type
            )
            cast_rslt = cast_type(extracted_field, desired_type)

            if cast_rslt:
                # updates with the appropriate cast value
                extracted_data_section[desired_field] = cast_rslt
            else:
                # removes field from the original section
                extracted_data_section.pop(desired_field)


def cast_type(extracted_field, desired_type):
    """
    Attempts to cast the extracted data from the regular expressions
    to a desired type given by the DRM.

    Args:
        extracted_field (str): the extract field from the OCR string;
        desired_type (str): the type

    Returns:
        (desired_type): the extracted_field coerced to the desired_type or None.
                        if there was a coercion error.

    Raises:
        ValueError: if the extracted_field cannot be cast to the desired type.
        BaseException: if the DRM contains unknown types.
    """
    logger.debug("Casting: %s, to %s...", extracted_field, desired_type)

    if isinstance(desired_type, list):
        return _cast_type_list(extracted_field, desired_type)

    types_mapping = {"int": int, "float": float, "str": str}

    if desired_type not in types_mapping.keys():
        raise BaseException(
            "Unknown specified type at the DRM: %s", desired_type
        )

    type_function = types_mapping[desired_type]

    try:
        return type_function(extracted_field)
    except ValueError:

        logger.info(
            "Removed wrong type data: %s, desired_type: %s",
            extracted_field,
            desired_type,
        )
        return None


def _cast_type_list(extracted_field, desired_type):
    """
    Performs data casting when the desired_type is list that contains the
    type and associated information about it.

    Supported types with metadata:
        - ['datetime', <datetime_format_string>] --> returns ISO datetime

    Args:
        extracted_field (str): extract field from the ocr
        desired_type: (list): type info in the format: [<type>, <type_metadata>]

    Returns:
        (desired_type): the extracted_field coerced to the desired_type or None.
                        if there was a coercion error.

    Raises:
        ValueError: if the extracted_field cannot be cast to the desired type.
        BaseException: if the DRM contains unknown types.
    """
    logger.debug(
        "Casting type with metadata: %s, to %s...",
        extracted_field,
        desired_type,
    )

    supported_types = ("datetime",)

    if len(desired_type) < 2 or desired_type[0] not in supported_types:
        raise BaseException(
            "Unknown specified type at the DRM: %s", desired_type
        )

    if desired_type[0] == "datetime":
        try:

            return datetime.strptime(
                extracted_field, desired_type[1]
            ).isoformat()

        except ValueError:
            logger.info(
                "Removed wrong type data: %s, desired_type: %s",
                extracted_field,
                desired_type,
            )
            return None
