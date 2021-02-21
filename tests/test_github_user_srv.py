#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from requests import Session
from unittest import TestCase

from app.config import load_config, ConfigSections, DefaultSectionKeys
from app.services import get_users, User, parse_dt
from app.database import DbEngine

REPO = 'teradici/deploy'


class GitHubUserServiceTest(TestCase):
    def setUp(self):
        self.config = load_config()
        conn_string = self.config[ConfigSections.DEFAULT][DefaultSectionKeys.CACHE_CONNECTION_STRING]
        self.db = DbEngine(conn_string)
        self.session = Session()

    def test_get_users(self):
        start = parse_dt('2019-06-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end = parse_dt('2020-05-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        result = get_users(REPO, start, end, self.db, self.session)

        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0, 'get_users does not work correctly')

