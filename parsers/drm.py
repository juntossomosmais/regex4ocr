"""
Module with the drm parser.
"""
import re

from unidecode import unidecode


def has_drm_match(ocr_result, drm_dict):
    """
    Checks if a drm matches the ocr_result format.
    """
    id_regexps = drm_dict["identifiers"]

    for id_regexp in id_regexps:
        regexp = re.compile(id_regexp, re.IGNORECASE)

        if not re.search(regexp, ocr_result):
            return False

    return True


def get_drm_match(ocr_result, drm_dicts):
    """
    Returns the first drm match.
    """
    drm_matches = [
        drm_dict
        for drm_dict in drm_dicts
        if has_drm_match(ocr_result, drm_dict)
    ]

    if not drm_matches:
        raise RuntimeError("No DRM match!")

    # uses first match
    return drm_matches[0]


def process_replaces(pre_process_str, replaces):
    """
    Replaces in the original ocr_result.
    """
    for regexp, replacement in replaces:
        pre_process_str = re.sub(regexp, replacement, pre_process_str)

    return pre_process_str


def pre_process_result(ocr_result, drm):
    """
    Pre processes ocr result.
    """
    pre_process_str = ocr_result

    options = drm.get("options")

    if options:

        if options.get("lowercase"):
            pre_process_str = pre_process_str.lower()

        if options.get("remove_whitespace"):
            pre_process_str = re.sub(r"\s", "", pre_process_str)

        if options.get("force_ascii"):
            pre_process_str = unidecode(pre_process_str)

        if options.get("replace"):
            pre_process_str = process_replaces(
                pre_process_str, options["replace"]
            )

    return pre_process_str


def extract_fields(ocr_result, drm):
    """
    Performs field extraction of the ocr_result.
    """
    fields_dict = drm["fields"]
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
    Extracts tabular data.
    """
    table = drm.get("table")

    if table:
        header_regexp = table["header"]
        end_regexp = table["footer"]

        beg = re.search(header_regexp, ocr_result)
        end = re.search(end_regexp, ocr_result)

        if not beg or not end:
            return None

    beg = beg.span()[1]
    end = end.span()[0]

    return ocr_result[beg:end]


def get_table_rows(table_data, drm):
    """
    Processes table data in order to extract its lines.
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

    # print(f"match: {table_data[row_start:row_end]}")
    # row = table_data[row_start:row_end].replace("\n", " ")
    # rows.append(row)
    # row_regexp = re.compile(
    #     row_start_re + ".+" + f"(?={row_end_re})", re.MULTILINE | re.DOTALL
    # )
    # row_matches = re.finditer(row_regexp, table_data)

    # for m in row_matches:
    #     row_start, row_end = m.span()

    #     print(f"match: {table_data[row_start:row_end]}")
    #     row = table_data[row_start:row_end].replace("\n", " ")
    #     rows.append(row)

    return rows


def extract_ocr_data(ocr_result, drm):
    """
    Extracts OCR data based on the DRM.
    """
    data = extract_fields(ocr_result, drm)
    table_data = extract_table_data(ocr_result, drm)

    data["table"] = table_data
    data["rows"] = get_table_rows(table_data, drm)

    return data


def parse_ocr_result(ocr_result, drm_dicts):
    """
    Attempts to parse the ocr result with the DRMs.
    """
    drm = get_drm_match(ocr_result, drm_dicts)
    pre_processed_result = pre_process_result(ocr_result, drm)
    data = extract_ocr_data(pre_processed_result, drm)

    print("\n=========== Pre Processed Rslt ===========")
    print(pre_processed_result)
    print("=========== // ============ // ===========\n")

    return data
