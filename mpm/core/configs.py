#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Парсинг конфигов
"""

from mpm.core import USER_DATA_DIR, USER_CONFIGS_DIR
from mpm.core.logging import logging
_LOG_PERFIX = "configs."

from pathlib import Path

def init_user_configs_dir():
    USER_DATA_DIR.mkdir()

def get_known_packages():
    pass
