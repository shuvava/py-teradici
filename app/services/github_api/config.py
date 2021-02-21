# -*- coding: utf-8 -*-
import distutils.util

from ...config import load_config, ConfigSections, CONFIGS_INITS


class GitHubSectionKeys:
    DEBUG_LOG_LEVEL = 'DEBUG_LOG_LEVEL'
    DEFAULT_REPO = 'REPO'


class ApiConfig:
    def __init__(self):
        app_settings = load_config()
        _print_log = app_settings[ConfigSections.GITHUB][GitHubSectionKeys.DEBUG_LOG_LEVEL]
        _default_repo = app_settings[ConfigSections.GITHUB][GitHubSectionKeys.DEFAULT_REPO]
        self._print_log = distutils.util.strtobool(_print_log)
        self._default_repo = _default_repo

    @property
    def print_log(self):
        return self._print_log

    @print_log.setter
    def print_log(self, value):
        self._print_log = value

    @property
    def default_repo(self):
        return self._default_repo

    @default_repo.setter
    def default_repo(self, value):
        self._default_repo = value


def init_github(config):
    config[ConfigSections.GITHUB] = {
        GitHubSectionKeys.DEBUG_LOG_LEVEL: True,
        GitHubSectionKeys.DEFAULT_REPO: 'teradici/deploy'
    }


CONFIGS_INITS.append(init_github)
