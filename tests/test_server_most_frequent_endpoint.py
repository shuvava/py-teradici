# -*- coding: utf-8 -*-
from datetime import timedelta
from pickle import dumps
from unittest import TestCase
from unittest.mock import patch

from redis import Redis
from starlette.testclient import TestClient

from app.database import DbEngine
from app.server import get_app
from common import MockRedis, commits


class ServerMostFrequentEndpointTest(TestCase):
    @patch.object(Redis, 'from_url', return_value=MockRedis("redis"))
    def setUp(self, mock) -> None:
        app = get_app()
        self.client = TestClient(app)

    @patch.object(DbEngine, 'get_session', return_value=MockRedis("redis"))
    def test_users_endpoint_success(self, mock_redis):
        key = 'github_users_service__GitHubCommit_teradici/deploy_2019-06-01T00:00:00+0000_2020-05-01T00:00:00+0000'
        mock_redis.return_value.set(key, dumps(commits), timedelta(minutes=60))
        response = self.client.get('/most-frequent')
        data = response.json()
        self.assertEqual(200, response.status_code, "response should be equal 200")
        self.assertEqual(len(data), 2, "mock api return 2 users")

    @patch.object(DbEngine, 'get_session', return_value=MockRedis(None))
    def test_users_endpoint_error(self, mock):
        response = self.client.get('/most-frequent')
        data = response.json()
        self.assertEqual(500, response.status_code, "response should be equal 500")
        self.assertEqual(data['detail'], 'Unexpected error', "mock api return error message")
