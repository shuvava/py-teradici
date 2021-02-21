# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Vladimir Shurygin.  All rights reserved.
#
"""
GitHub api utilities
"""
from datetime import datetime
from typing import List, Dict, Union, Optional

from fastapi.logger import logger
from requests import Session

from app.database import GitHubCommit, GitHubAuthor
from .config import ApiConfig

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


def parse_dt(dt):
    if not dt:
        return None
    try:
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S%z')
    except:
        return None


def init_session():
    _url = f'{__API_BASE_URL__}{__ENTRYPOINT__}'
    if CONFIG.print_log:
        logger.info('session init')
    _session = Session()
    response = _session.get(_url, headers=__headers__)
    print_response(response)
    return _session


def check_response_is_successful(response):
    if response.status_code != 200:
        logger.warn(f'request completed with error: HTTP code: {response.status_code} url: {response.url}')
        return False, 0, []
    content = response.json()
    return True, content


def get_author(item: Dict) -> Optional[GitHubAuthor]:
    if item is None:
        return None
    name = 'unknown'
    email = 'unknown'
    user_id = -1
    if 'commit' in item:
        if 'author' in item['commit']:
            if 'name' in item['commit']['author']:
                name = item['commit']['author']['name']
            if 'email' in item['commit']['author']:
                email = item['commit']['author']['email']
    if 'author' in item:
        if 'login' in item['author']:
            name = item['author']['login']
        if 'id' in item['author']:
            user_id = item['author']['id']
    if user_id == -1:
        return None
    return GitHubAuthor(user_id, name, email)


def get_commit(item: Dict) -> Optional[GitHubCommit]:
    if item is None:
        return None
    sha = ''
    author_id = -1
    date = None
    if 'sha' in item:
        sha = item['sha']
    if 'author' in item:
        if 'id' in item['author']:
            author_id = item['author']['id']
    if 'commit' in item:
        if 'author' in item['commit']:
            if 'date' in item['commit']['author']:
                date = parse_dt(item['commit']['author']['date'])
    if author_id == -1:
        return None
    return GitHubCommit(author_id, date, sha)


def get_github_commits(repo: str, start_page: int = None, since: datetime = None, session=None) -> Dict[
    str, Union[List[GitHubCommit], Dict[int, GitHubAuthor]]]:
    if start_page is None:
        start_page = 1
    _url = f'{__API_BASE_URL__}/{repo}/commits'
    if CONFIG.print_log:
        logger.info('get github commits')
    if not session:
        session = init_session()
    params = {
        'page': start_page,
        'per_page': 10,
    }
    if since is not None:
        params['since'] = since.isoformat()
    response = session.get(_url, headers=__headers__, params=params)
    print_response(response)
    data = check_response_is_successful(response)
    authors = {}
    commits = []
    result = {
        'authors': authors,
        'commits': commits
    }
    if not data[0]:
        return result
    for item in data[1]:
        _author = get_author(item)
        _commit = get_commit(item)
        if _author is None or _commit is None:
            logger.warn(f'error on parsing: Object not created {item}')
        if _author.id != _commit.author_id:
            logger.warn(f'error on parsing: author and commit have different ids {item}')
        if _author and _author.id not in authors:
            authors[_author.id] = _author
        commits.append(_commit)
    return result


def get_repo_commits(repo: str) -> List[GitHubCommit]:
    pass


def get_repo_authors(repo: str) -> List[GitHubAuthor]:
    pass
