"""
Module with all the data extraction functions used after the OCR result
string pre processing stage.
"""
import logging
import re

from logger.formatter import format_logger

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


def get_table_rows(table_data, drm):
    """
    Extract rows from the table data substring of the OCR result string
    by using the DRM key "line_start" which denotes the regexp that
    matches the beginning of EACH new line of the tabular data.

    Args:
        table_data (str): tabular substring of the original OCR result string;
        drm (dict): DRM dict object for parsing the OCR string.

    Returns:
        (list): List of all the matched rows of the table_data substring
                of the original OCR result.
    """
    if not table_data:
        return []

    table = drm.get("table")
    rows = []

    row_start_re = table["line_start"]

    row_matches = re.finditer(row_start_re, table_data)
    starts = []
    ends = []

    if row_matches:
        for m in row_matches:
            starts.append(m.span()[0])

        for i in range(0, len(starts) - 1):
            ends.append(starts[i + 1])

        ends.append(len(table_data) - 1)

        for start, end in zip(starts, ends):
            row = table_data[start:end].replace("\n", "")
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
