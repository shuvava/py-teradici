#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import timezone
from requests import Session
from unittest import TestCase

from app.config import load_config, ConfigSections, DefaultSectionKeys
from app.services import get_users, get_commit_frequency , parse_dt
from app.database import DbEngine

REPO = 'teradici/deploy'


class GitHubUserServiceTest(TestCase):
    def setUp(self):
        self.config = load_config()
        conn_string = self.config[ConfigSections.DEFAULT][DefaultSectionKeys.CACHE_CONNECTION_STRING]
        self.db = DbEngine(conn_string)
        self.session = Session()

    def test_get_users(self):
        key = 'github_users_service__User_teradici/deploy_2019-06-01T00:00:00+0000_2020-05-01T00:00:00+0000'
        client = self.db.get_session()
        client.delete(key)

        start = parse_dt('2019-06-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end = parse_dt('2020-05-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        result = get_users(REPO, start, end, self.db, self.session)

        val = client.exists(key)

        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0, 'get_users does not work correctly')
        self.assertEqual(val, 1, 'db records should be created')

    def test_get_commit_frequency(self):
        key = 'github_users_service__CommitFrequency_teradici/deploy_2019-06-01T00:00:00+0000_2020-05-01T00:00:00+0000__5'
        client = self.db.get_session()
        client.delete(key)

        start = parse_dt('2019-06-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end = parse_dt('2020-05-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        result = get_commit_frequency(REPO, 5, start, end, self.db, self.session)

        val = client.exists(key)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5, 'get_commit_frequency does not work correctly')
        self.assertEqual(val, 1, 'db records should be created')
