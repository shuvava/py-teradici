#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from requests import Session
from unittest import TestCase

from app.services.github_api import get_repo_commits
from app.services.github_api.api import get_github_commits

REPO = 'teradici/deploy'


class GitHubApiTest(TestCase):
    def setUp(self):
        self.session = Session()

    def test_get_github_commits(self):
        result = get_github_commits(REPO, session=self.session)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 100, 'commits not populated correctly')

    def test_get_github_commits_since_future(self):
        since = datetime.utcnow() + timedelta(days=1)
        result = get_github_commits(REPO, since=since, session=self.session)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0, 'date filter does not work correctly')

    def test_get_github_commits_since_past(self):
        since = datetime.utcnow() - timedelta(days=100)
        result = get_github_commits(REPO, since=since, session=self.session)

        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0, 'date filter does not work correctly(lower bound)')
        self.assertLess(len(result), 100, 'date filter does not work correctly(upper bound)')

    def test_get_all_commits(self):
        since = datetime.utcnow() - timedelta(days=720)
        result = get_repo_commits(REPO, since=since, session=self.session)

        self.assertIsNotNone(result)
        self.assertGreater(len(result), 100, 'commits not populated correctly ')
