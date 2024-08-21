#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read the configuration file.
"""

import os
from configparser import ConfigParser

# Read client configuration from:
# 1. ~/.phantasy-rest/client.ini
# 2. /etc/phantasy-rest/client.ini
# 3. The location with deployed package, e.g. <phantasyRestClient>/config/client.ini
#

_CWD = os.path.dirname(os.path.abspath(__file__))
_SYS_CONFIG_PATH = "/etc/phantasy-rest/client.ini"
_USER_CONFIG_PATH = "~/.phantasy-rest/client.ini"


def get_config_file():
    """Get the file path of the configuration file.
    """
    user_config_fullpath = os.path.abspath(
            os.path.expanduser(_USER_CONFIG_PATH))
    if os.path.isfile(user_config_fullpath):
        return user_config_fullpath
    if os.path.isfile(_SYS_CONFIG_PATH):
        return _SYS_CONFIG_PATH
    return os.path.join(_CWD, "client.ini")


def read_config():
    """Read out the configuration as a dict.
    """
    filepath = get_config_file()
    config = ConfigParser()
    conf_path = config.read(filepath)[0]
    svr_conf = config[config['default']['use']]
    r = dict(svr_conf.items())
    r['conf_path'] = conf_path
    return r
