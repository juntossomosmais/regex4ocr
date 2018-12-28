"""
Module with a miscellania of validation functions used throughout
the application.
"""


def is_valid_drm(drm):
    """
    Verifies if a parsed DRM dict has the minimum required fields.

    Args:
        drm (dict): the DRM dict to be validated.

    Returns:
        (bool): True if the DRM is valid. Otherwise, False.
    """
    required_keys = ("identifiers", "fields")

    return all(key in drm for key in required_keys)
