# -*- coding: utf-8 -*-
from datetime import datetime


class GitHubCommit:
    def __init__(self, name: str, email: str, author_id: int, date: datetime, sha: str):
        self.author_id = author_id
        self.author_name = name
        self.author_email = email
        self.date = date
        self.sha = sha

    def __repr__(self):
        return f"<GitHubCommit(author_name='{self.author_name}', sha='{self.sha[:7]}', date={self.date.isoformat()})>"
