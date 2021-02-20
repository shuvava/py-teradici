# -*- coding: utf-8 -*-
from os import environ
from .config import APP_NAME, create_config


def get_env_value(key):
    """get environment variable"""
    if key in environ:
        return environ[key]
    return None


def build_key(section, key):
    return f'{APP_NAME}__{section}__{key}'.upper()


def load_env_config(config):
    for section in config:
        for key in config[section]:
            env_key = build_key(section, key)
            value = get_env_value(env_key)
            if value:
                config[section][key] = value


def load_config():
    config = create_config()
    load_env_config(config)
    return config
