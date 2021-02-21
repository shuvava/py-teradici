#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch

from requests import Session

from app.services.github_api.api import get_github_commits
from common import REPO, content, MockResponse


class GitHubApiTest(TestCase):
    def setUp(self):
        self.session = Session()

    @patch.object(Session, 'get', return_value=MockResponse(200, content))
    def test_get_github_commits_successful(self, mock_response):
        result = get_github_commits(REPO)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3, 'commits not populated correctly')

    @patch.object(Session, 'get', return_value=MockResponse(500, "some string error"))
    def test_get_github_commits_error(self, mock_response):
        since = datetime.utcnow() + timedelta(days=1)
        result = get_github_commits(REPO, since=since, session=self.session)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

