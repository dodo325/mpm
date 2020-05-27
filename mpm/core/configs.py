#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Парсинг конфигов
"""
import shutil
from pathlib import Path
import urllib.request
import json

from mpm.core import PACKAGE_DIR, USER_DATA_DIR, USER_CONFIGS_DIR, SCRIPTS_DIR, CONFIGS_DIR, USER_SCRIPTS_DIR
from mpm.core.logging import get_logger
logger = get_logger(__file__)


def get_settings():
    settings_file = CONFIGS_DIR / "settings.json"
    with settings_file.open() as sf:
            settings = json.load(sf)

    user_settings_file = USER_CONFIGS_DIR / "settings.json"
    if user_settings_file.is_file():
        with user_settings_file.open() as sf:
            user_settings = json.load(sf)
        settings.update(user_settings)
    return settings

def get_remote_known_packages(): 
    settings = get_settings()
    url = settings['known_packages_url']
    response = urllib.request.urlopen(url)
    return json.load(response)

def init_user_configs_dir():
    if not USER_DATA_DIR.is_dir():
        USER_DATA_DIR.mkdir()
    if not USER_CONFIGS_DIR.is_dir():
        shutil.copytree(CONFIGS_DIR, USER_CONFIGS_DIR, copy_function=shutil.copy)
    if not USER_SCRIPTS_DIR.is_dir():
        shutil.copytree(SCRIPTS_DIR, USER_SCRIPTS_DIR, copy_function=shutil.copy)

def get_known_packages():
    init_user_configs_dir()
    try:
        known_packages = get_remote_known_packages()
    except urllib.request.HTTPError as e:
        logger.error(f"HTTPError: code = {e.code}, url = {e.url}")
        known_packages_file = CONFIGS_DIR / "known_packages.json"
        with known_packages_file.open() as sf:
                known_packages = json.load(sf)

    user_known_packages_file = USER_CONFIGS_DIR / "known_packages.json"
    if user_known_packages_file.is_file():
        with user_known_packages_file.open() as sf:
            user_known_packages = json.load(sf)
        known_packages.update(user_known_packages)
    return known_packages
