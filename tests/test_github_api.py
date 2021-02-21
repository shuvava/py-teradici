#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from app.config import load_config
from app.services.github_api import get_github_commits


class GitHubApiTest(TestCase):
    def setUp(self):
        self.config = load_config()

    def test_get_all_commits(self):
        result = get_github_commits('teradici/deploy')

        self.assertIsNotNone(result)
        self.assertGreater(len(result['authors']), 0, 'authors not populated')
        self.assertGreater(len(result['commits']), 0, 'commits not populated')
