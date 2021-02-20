# -*- coding: utf-8 -*-
import configparser

APP_NAME = 'webapp'


class ConfigSections:
    DEFAULT = 'DEFAULT'


class DefaultSectionKeys:
    CACHE_CONNECTION_STRING = 'CACHE_CONNECTION_STRING'
    NAME = 'NAME'
    VERSION = 'VERSION'
    API_PREFIX = 'API_PREFIX'


def init_default(config):
    config[ConfigSections.DEFAULT] = {
        DefaultSectionKeys.CACHE_CONNECTION_STRING: 'redis',
        DefaultSectionKeys.NAME: 'GitHub API Client App',
        DefaultSectionKeys.VERSION: '0.1',
        DefaultSectionKeys.API_PREFIX: '/api'
    }


CONFIGS_INITS = [
    init_default,
]


def create_config():
    config = configparser.ConfigParser()
    for fn in CONFIGS_INITS:
        if callable(fn):
            fn(config)
    return config

