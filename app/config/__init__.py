# -*- coding: utf-8 -*-
"""Config"""

from .config import (
    APP_NAME,
    ConfigSections,
    CONFIGS_INITS,
    DefaultSectionKeys
)
from .config_loader import load_config

__all__ = [
    load_config,
    APP_NAME,
    ConfigSections, DefaultSectionKeys,
    CONFIGS_INITS
]
