# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Vladimir Shurygin.  All rights reserved.
#
"""
GitHub api utilities
"""
from datetime import datetime
from typing import List, Dict, Optional

from fastapi.logger import logger
from requests import Session

from app.database import GitHubCommit
from .config import ApiConfig
from .utils import get_dict, parse_dt, dt_to_str

__API_BASE_URL__ = 'https://api.github.com/repos'
__ENTRYPOINT__ = '/'
__headers__ = {
    'User-Agent': 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
}

CONFIG = ApiConfig()


def print_response(response):
    if not CONFIG.print_log:
        return
    if response.history:
        logger.info(' Request was redirected')
        for resp in response.history:
            logger.info(f'  status_code = {resp.status_code}, url= {resp.url}')
        logger.info(' Final destination:')
    else:
        logger.info(' Request was not redirected')
    logger.info(f'  status_code = {response.status_code}, url= {response.url}')


def get_repo(repo: Optional[str] = None) -> str:
    if repo is None:
        return CONFIG.default_repo
    if repo == '':
        raise ValueError(f'repo name can not be empty')

    if '/' not in repo:
        raise ValueError(f'repo format is incorrect it should be owner/repo')
    return repo


def init_session():
    if CONFIG.print_log:
        logger.info('session init')
    _session = Session()
    return _session


def check_response_is_successful(response):
    if response.status_code != 200:
        logger.warn(f'request completed with error: HTTP code: {response.status_code} url: {response.url}')
        return False, 0, []
    content = response.json()
    return True, content


def get_commit(item: Dict) -> Optional[GitHubCommit]:
    if item is None:
        return None
    date = None
    _author = get_dict(item, 'author')
    _commit = get_dict(item, 'commit')
    _commit_author = get_dict(_commit, 'author')

    sha = item.get('sha', '')
    author_id = _author.get('id', -1)
    email = _commit_author.get('email', 'unknown')
    name = _author.get('login', 'unknown')
    if name == 'unknown':
        name = _commit_author.get('name', 'unknown')
    _dt = _commit_author.get('date', None)
    if _dt:
        date = parse_dt(_dt)

    return GitHubCommit(name, email, author_id, date, sha)


def get_github_commits(
    repo: Optional[str] = None,
    start_page: Optional[int] = None,
    since: Optional[datetime] = None,
    session: Optional[Session] = None
) -> List[GitHubCommit]:
    if start_page is None:
        start_page = 1
    repo = get_repo(repo)
    _url = f'{__API_BASE_URL__}/{repo}/commits'
    if CONFIG.print_log:
        logger.info('get github commits')
    if not session:
        session = init_session()
    params = {
        'page': start_page,
        'per_page': 100,
    }
    if since is not None:
        params['since'] = dt_to_str(since)
    response = session.get(_url, headers=__headers__, params=params)
    print_response(response)
    data = check_response_is_successful(response)
    commits = []
    if not data[0]:
        return commits
    for item in data[1]:
        _commit = get_commit(item)
        if _commit is None:
            logger.warn(f'error on parsing: Object not created {item}')
            continue
        commits.append(_commit)
    return commits


def get_repo_commits(
    repo: Optional[str] = None,
    since: Optional[datetime] = None,
    session: Optional[Session] = None
) -> List[GitHubCommit]:
    commits = []
    page = 1
    _continue = True
    if not session:
        session = init_session()
    while _continue:
        _result = get_github_commits(repo, page, since, session)
        if len(_result) == 0:
            _continue = False
        page += 1
        commits.extend(_result)
    return commits
