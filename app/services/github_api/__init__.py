# -*- coding: utf-8 -*-
"""
github.com api implementation
"""
from .config import ApiConfig
from .api import get_github_commits

__all__ = [
    get_github_commits
]
