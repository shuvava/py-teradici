# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Vladimir Shurygin.  All rights reserved.
#

class CommitFrequency:
    def __init__(self, name: str, commits: int):
        self.name = name
        self.commits = commits

    def __repr__(self):
        return f"<CommitFrequency(name='{self.name}', commits='{self.commits}')>"
