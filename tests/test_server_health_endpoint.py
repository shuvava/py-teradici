# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from app.server import get_app


class ServerTest(unittest.TestCase):
    def setUp(self) -> None:
        app = get_app()
        self.client = TestClient(app)

    def test_is_alive_endpoint(self):
        response = self.client.get('/health/isAlive')
        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(data) > 0)

    def test_is_ready_endpoint(self):
        response = self.client.get('/health/isReady')
        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(data) > 0)
