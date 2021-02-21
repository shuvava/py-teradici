#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import timezone
from unittest import TestCase
from unittest.mock import patch

from requests import Session

from app.database import DbEngine
from app.services import get_users, get_commit_frequency, parse_dt
from common import REPO, content, MockResponse, MockRedis


class GitHubUserServiceTest(TestCase):
    def setUp(self):
        self.session = Session()

    @patch.object(DbEngine, 'get_session', return_value=MockRedis("redis"))
    @patch.object(Session, 'get', return_value=MockResponse(200, content))
    def test_get_users(self, mock_response, mock_redis):
        key = 'github_users_service__User_teradici/deploy_2020-09-01T00:00:00+0000_2021-12-01T00:00:00+0000'
        client = mock_redis.return_value
        client.delete(key)

        start = parse_dt('2020-09-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end = parse_dt('2021-12-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        result = get_users(start, end, REPO, client, self.session)

        val = client.exists(key)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2, 'get_users does not work correctly')
        self.assertEqual(val, 1, 'db records should be created')

    @patch.object(DbEngine, 'get_session', return_value=MockRedis("redis"))
    @patch.object(Session, 'get', return_value=MockResponse(200, content))
    def test_get_commit_frequency(self, mock_response, mock_redis):
        key = 'github_users_service__CommitFrequency_teradici/deploy_2020-09-01T00:00:00+0000_2021-12-01T00:00:00+0000__5'
        client = mock_redis.return_value
        client.delete(key)

        start = parse_dt('2020-09-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end = parse_dt('2021-12-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        result = get_commit_frequency(5, start, end, REPO, client, self.session)

        val = client.exists(key)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2, 'get_commit_frequency does not work correctly')
        self.assertEqual(result[0].name, 'user1')
        self.assertEqual(result[0].commits, 2)
        self.assertEqual(val, 1, 'db records should be created')
