"""
Module with convenience functions to manipulate data files
for testing.
"""


def open_file(file_path, read_mode="r"):
    """
    Opens a file from the OS and reads it to cast
    it to string.

    Args:
        file_path (str): OS file path of the archive;
        read_mode (str): read mode.

    Returns:
        (str): the file contents as a string.
    """
    with open(file_path, read_mode) as myfile:
        file_txt = myfile.read()

    return file_txt
