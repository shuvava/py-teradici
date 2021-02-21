# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Vladimir Shurygin.  All rights reserved.
#
from typing import List
from collections import Counter
from datetime import datetime, timedelta
from pickle import loads, dumps
from requests import Session

from .github_api import get_repo_commits, dt_to_str
from .models import User, CommitFrequency
from ..database import GitHubCommit, DbEngine

DEFAULT_TIMEOUT = timedelta(minutes=60)


def get_key(repo: str, start: datetime, end: datetime, obj_type: str) -> str:
    return f'github_users_service__{obj_type}_{repo}_{dt_to_str(start)}_{dt_to_str(end)}'


def dumps_item(db: DbEngine, key: str, values: List[any]):
    if db is None:
        return
    vals = dumps(values)
    client = db.get_session()
    client.set(key, vals, ex=DEFAULT_TIMEOUT)


def loads_item(db: DbEngine, key: str):
    if db is None:
        return None
    client = db.get_session()
    vals = client.get(key)
    if vals is None:
        return None
    values = loads(vals)
    return values


def get_commits(
    repo: str,
    start: datetime,
    end: datetime,
    db: DbEngine = None,
    session: Session = None
) -> List[GitHubCommit]:
    """getting github commits for repo and date range"""
    if repo is None or repo == '':
        raise ValueError(f'repo name can not be empty')
    if '/' not in repo:
        raise ValueError(f'repo format is incorrect it should be owner/repo')
    key = get_key(repo, start, end, 'GitHubCommit')
    cache = loads_item(db, key)
    if cache is not None:
        return cache
    all_commits = get_repo_commits(repo, start, session=session)
    commits = [commit for commit in all_commits if commit.date <= end]
    dumps_item(db, key, commits)
    return commits


def get_users(
    repo: str,
    start: datetime,
    end: datetime,
    db: DbEngine = None,
    session: Session = None,
) -> List[User]:
    """getting users committed for given repo in given time period

    :param repo: repo name
    :param start: lower time border
    :param end: upper time border
    :param db: database instance
    :param session: Request context
    """
    key = get_key(repo, start, end, 'User')
    cache = loads_item(db, key)
    if cache is not None:
        return cache
    commits = get_commits(repo, start, end, db, session)
    user_set = {}
    for commit in commits:
        if commit.author_name not in user_set:
            user = User(commit.author_name, commit.author_email)
            user_set[user.name] = user
    users = list(user_set.values())
    dumps_item(db, key, users)
    return users


def get_commit_frequency(
    repo: str,
    top_n: int,
    start: datetime,
    end: datetime,
    db: DbEngine = None,
    session: Session = None,
) -> List[CommitFrequency]:
    """getting top 5 most frequent committers for given repo in given time period

    :param repo: repo name
    :param top_n: number of top most common elements
    :param start: lower time border
    :param end: upper time border
    :param db: database instance
    :param session: Request context
    """
    key = get_key(repo, start, end, 'CommitFrequency')
    key = f'{key}__{top_n}'
    cache = loads_item(db, key)
    if cache is not None:
        return cache
    commits = get_commits(repo, start, end, db, session)
    users = []
    for commit in commits:
        user = User(commit.author_name, commit.author_email)
        users.append(user)
    counter = Counter(users)
    top_users = counter.most_common(top_n)
    result = []
    for item in top_users:
        cf = CommitFrequency(item[0].name, item[1])
        result.append(cf)
    dumps_item(db, key, result)
    return result
