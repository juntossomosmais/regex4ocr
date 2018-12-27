#!/usr/bin/env python
import logging

import yaml


def parse_yml(file_path):
    """ Parses Yml file to python dict. """

    with open(file_path, "r") as stream:
        try:

            config_dict = yaml.load(stream)

            return config_dict

        except yaml.YAMLError as exc:
            logging.warning(exc)

            return None
