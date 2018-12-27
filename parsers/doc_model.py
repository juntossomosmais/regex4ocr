"""
Module with the Document Regexp Model (DRM) parser.
"""
import os
from yml_parser import parse_yml


def is_valid_drm(drm):
    """ Validates the drm keys. """
    required_keys = ("identifiers", "fields")

    return all(key in drm for key in required_keys)


def get_drms(drms_path):
    all_files = os.listdir(drms_path)
    drms = []

    for file in all_files:
        drm_dict = parse_yml(drms_path + "/" + file)

        if drm_dict and is_valid_drm(drm_dict):
            drms.append(drm_dict)

    return drms
