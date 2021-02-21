# -*- coding: utf-8 -*-
import distutils.util

from ...config import load_config, ConfigSections, CONFIGS_INITS


class GitHubSectionKeys:
    DEBUG_LOG_LEVEL = 'DEBUG_LOG_LEVEL'


class ApiConfig:
    def __init__(self):
        app_settings = load_config()
        _print_log = app_settings[ConfigSections.GITHUB][GitHubSectionKeys.DEBUG_LOG_LEVEL]
        self._print_log = distutils.util.strtobool(_print_log)

    @property
    def print_log(self):
        return self._print_log

    @print_log.setter
    def print_log(self, value):
        self._print_log = value


def init_realorca(config):
    config[ConfigSections.GITHUB] = {
        GitHubSectionKeys.DEBUG_LOG_LEVEL: True,
    }


CONFIGS_INITS.append(init_realorca)
