# -*- coding: utf-8 -*-
from datetime import  datetime

from app.database.models import GitHubCommit

REPO = 'teradici/deploy'

commits = [
    GitHubCommit('user1', 'user1@mock,com', 1, datetime.now(), '0001'),
    GitHubCommit('user1', 'user1@mock,com', 1, datetime.now(), '0002'),
    GitHubCommit('user2', 'user2@mock,com', 1, datetime.now(), '0003'),
]

content = [
    {
        "sha": "00003",
        "commit": {
            "author": {
                "name": "user1",
                "email": "user1@users.noreply.github.com",
                "date": "2020-12-01T00:00:00Z"
            }
        },
        "author": {
            "login": "user1",
            "id": 1
        }
    },
    {
        "sha": "00002",
        "commit": {
            "author": {
                "name": "user1",
                "email": "user1@users.noreply.github.com",
                "date": "2020-11-01T00:00:00Z"
            }
        },
        "author": {
            "login": "user1",
            "id": 1
        }
    },
    {
        "sha": "00001",
        "commit": {
            "author": {
                "name": "user2",
                "email": "user2@users.noreply.github.com",
                "date": "2020-10-01T00:00:00Z"
            }
        },
        "author": {
            "login": "user2",
            "id": 2
        }
    }
]


class MockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content
        self.history = None
        self.url = 'http://mock'

    def json(self):
        self.status_code = 403
        return self.content


class MockRedis:
    def __init__(self, conn):
        self.conn = conn
        self.cache = {}

    def client(self):
        if self.conn is not None:
            return self
        raise ValueError("connection not setup")

    def set(self, key, val, ex):
        if self.conn is None:
            raise ValueError("connection not setup")
        self.cache[key] = (val, datetime.now() + ex)

    def get(self, key):
        if self.conn is None:
            raise ValueError("connection not setup")
        if key not in self.cache:
            return None
        val, ex = self.cache[key]
        if ex < datetime.now():
            del self.cache[key]
            return None
        return val

    def delete(self, key):
        if self.conn is None:
            raise ValueError("connection not setup")
        if key in self.cache:
            del self.cache[key]

    def exists(self, key):
        if self.conn is None:
            raise ValueError("connection not setup")
        return key in self.cache

    def check_health(self):
        if self.conn is None:
            raise ValueError("connection not setup")
        return True

    def get_session(self):
        return self
