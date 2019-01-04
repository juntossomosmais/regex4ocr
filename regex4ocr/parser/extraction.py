"""
Module with all the data extraction functions used after the OCR result
string pre processing stage.
"""
import logging
import re

from regex4ocr.logger.formatter import format_logger

logger = format_logger(logging.getLogger(__name__))


def extract_fields(ocr_result, drm):
    """
    Performs field extraction of the pre processed OCR result. This function
    uses the key 'fields' of DRM and its regexps to extract the data.

    Args:
        ocr_result (str): OCR result string;
        drm (dict): DRM dict object for parsing the OCR string.

    Returns:
        (dict): Dict with all the 'fields' of the DRM as the keys and
                the corresponding regexp matches as the values.

    Example:

        DRM yml
        --------
        fields:
            field1: regexp1
            field2: regexp2

        Result:
        --------
        {
            "field1": "regexp_result1",
            "field2": "regexp_result2"
        }
    """
    fields_dict = drm["fields"]  # required yml key
    data = {}

    # traverses all regexp
    for field, regexp in fields_dict.items():
        rslt = re.search(regexp, ocr_result)

        if rslt:
            # checks for first group
            if rslt.groups():
                data[field] = rslt.groups()[0]
            else:
                data[field] = rslt[0]

    return data


def extract_table_data(ocr_result, drm):
    """
    Performs extraction of tabular data from the pre processed OCR result
    string. Returns a substring of the pre processed OCR string that is
    between the 'header' and 'footer' of the DRM regexp keys.

    Args:
        ocr_result (str): already pre processed OCR result string;
        drm (dict): DRM dict object for parsing the OCR string.

    Returns:
        (str): Substring that contains tabular data of the OCR string or None
               if the regexps cant find a header/footer.
    """
    table = drm.get("table")

    if table:
        header_regexp = table["header"]
        end_regexp = table["footer"]

        header = re.search(header_regexp, ocr_result)
        footer = re.search(end_regexp, ocr_result)

        if not header or not footer:
            return None

        beg = header.span()[1]
        end = footer.span()[0]

    return {
        "header": header.group(),
        "all_rows": ocr_result[beg:end],
        "footer": footer.group(),
    }


def get_table_rows(all_rows, drm):
    """
    Extract rows from the table data substring of the OCR result string
    by using the DRM key "line_start" which denotes the regexp that
    matches the beginning of EACH new line of the tabular data.

    Args:
        all_rows (str): substring containing all rows from the OCR string;
        drm (dict): DRM dict object for parsing the OCR all rows string.

    Returns:
        (list): List of all the matched rows of the all_rows substring
                of the original OCR result.
    """
    if not all_rows:
        return []

    # table data is guaranteed here
    row_start_re = drm["table"]["line_start"]
    row_matches = re.finditer(row_start_re, all_rows)

    # holds all line start indexes when regexp matches
    line_start_indexes = []

    # holds all the end of line indexes
    line_ends_indexes = []

    # holds rows slices of the original string based on start:end indexes
    rows = []

    if row_matches:

        for m in row_matches:
            # gets the indexes of all_rows string where the regexp
            # 'line_start' matches
            line_start_indexes.append(m.span()[0])

        # the end of a line in the all_rows string is marked by
        # the beginning of the next line_start_index
        for i in range(0, len(line_start_indexes) - 1):
            line_ends_indexes.append(line_start_indexes[i + 1])

        # the last index that marks the end of the last line is
        # length of the all_rows string
        all_rows_end_index = len(all_rows) - 1
        line_ends_indexes.append(all_rows_end_index)

        # appends all rows substring based on the start:end indexes
        for start, end in zip(line_start_indexes, line_ends_indexes):
            row = all_rows[start:end].replace("\n", "")
            rows.append(row)

    return rows


def extract_ocr_data(ocr_result, drm):
    """
    Performs all the data extraction by calling the extraction functions.
    The data extraction is as follows:

        fields extraction -> table data extraction -> done

    Args:
        ocr_result (str): already pre processed OCR result string;
        drm (dict): DRM dict object for parsing the OCR string.

    Returns:
        (dict): Dict with all the extracted data from the OCR string.

    Example:

        {
            "fields": {
                "field1": "result1",
                "field2": "result2"
            },
            "table": {
                "header": "table header",
                "all_rows": "all rows together here...",
                "rows": [
                    "row 1 result",
                    "row 2 result",
                    ...
                ],
                "footer": "table footer"
            }
        }
    """
    extracted_data = {"fields": {}, "table": {}}
    extracted_data["fields"] = extract_fields(ocr_result, drm)

    # may be empty
    table_data = extract_table_data(ocr_result, drm)

    if table_data:
        extracted_data["table"] = table_data

        # may be empty
        rows = get_table_rows(table_data["all_rows"], drm)

        if rows:
            extracted_data["table"]["rows"] = rows

    return extracted_data
