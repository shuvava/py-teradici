# -*- coding: utf-8 -*-


class GitHubAuthor:
    def __init__(self, user_id: int, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<GitHubAuthor(id='{self.id}' name='{self.name}', email={self.email})>"
