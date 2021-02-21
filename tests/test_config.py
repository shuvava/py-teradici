#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from os import environ

from app.config import load_config, ConfigSections, APP_NAME, CONFIGS_INITS


class ConfigLoadTest(unittest.TestCase):
    def setUp(self):
        self.config = load_config()

    def test_load_config(self):
        self.assertIsNotNone(self.config)

    def test_default_section(self):
        self.assertIsNotNone(self.config[ConfigSections.DEFAULT])

    def test_env_var_load(self):
        key = 'CACHE_CONNECTION_STRING'
        value = 'test'
        self.add_test_env_var(ConfigSections.DEFAULT, key, value)
        config = load_config()
        self.assertEqual(value, config[ConfigSections.DEFAULT][key])

    def test_add_custom_section(self):
        key = 'test'
        value = '1'

        def test_section(c):
            c[key] = {key: value}

        CONFIGS_INITS.append(test_section)
        config = load_config()
        self.assertEqual(value, config[key][key])

    def add_test_env_var(self, section, key, value):
        key_env = f'{APP_NAME}__{section}__{key}'.upper()
        environ[key_env] = value


if __name__ == '__main__':
    unittest.main()
