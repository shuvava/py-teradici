# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import patch

from redis import Redis
from starlette.testclient import TestClient

from app.database import DbEngine
from app.server import get_app
from common import MockRedis


class ServerTest(TestCase):
    @patch.object(Redis, 'from_url', return_value=MockRedis("redis"))
    def setUp(self, mock) -> None:
        app = get_app()
        self.client = TestClient(app)

    def test_is_alive_endpoint(self):
        response = self.client.get('/health/isAlive')
        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(data) > 0)

    @patch.object(DbEngine, 'get_session', return_value=MockRedis("redis"))
    def test_is_ready_endpoint_success(self, mock):
        response = self.client.get('/health/isReady')
        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(data) > 0)

    @patch.object(DbEngine, 'get_session', return_value=MockRedis(None))
    def test_is_ready_endpoint_error(self, mock):
        response = self.client.get('/health/isReady')
        data = response.json()
        self.assertEqual(503, response.status_code, "response should be equal 500")
        self.assertEqual(data['detail'], 'db connection error', "mock api return error message")
