"""
Module with type-casting related functions.
"""
import logging

logger = logging.getLogger(__name__)


def validate_types(extracted_data, drm):
    """
    Performs data validation of the extracted_data according to the
    types informed at the drm for this document.
    """
    fields_types_section = drm.get("types", {}).get("fields", {})
    inline_groups_types_section = (
        drm.get("types", {}).get("table", {}).get("inline_named_group_captures")
    )
    rows = extracted_data.get("table", {}).get("rows")

    if rows and inline_groups_types_section:
        # removes named groups if type casting fails
        for row_dict in rows:
            remove_wrong_types(row_dict["data"], inline_groups_types_section)

    # fields is always required
    if fields_types_section:
        remove_wrong_types(extracted_data["fields"], fields_types_section)


def remove_wrong_types(extracted_data_section, drm_types_section):
    """
    Receives a portion (dict) of the parsed image receipt and a dict whose keys
    are the extracted_data_section keys and values are the are desired types for
    the extracted_data_section keys.

    If the cast of the extracted_data_section to the desired type fails, that key
    is POPPED from the original dictionary. Hence, this method MUTATES the
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
    """
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
