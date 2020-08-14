#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Парсинг конфигов
"""
import shutil
from pathlib import Path
import urllib.request
import json
from mpm.core import (
    USER_DATA_DIR,
    USER_CONFIGS_DIR,
    SCRIPTS_DIR,
    CONFIGS_DIR,
    USER_SCRIPTS_DIR,
)
from mpm.utils.json_parse import iterative_topological_sort
from mpm.core.logging import getLogger

logger = getLogger(__name__)

user_known_packages_file = USER_CONFIGS_DIR / "known_packages.json"
known_packages_file = CONFIGS_DIR / "known_packages.json"
user_settings_file = USER_CONFIGS_DIR / "settings.json"
settings_file = CONFIGS_DIR / "settings.json"


def get_scripts() -> dict:
    scripts = {}
    paths = list(SCRIPTS_DIR.glob("**/*"))
    paths.extend(list(USER_SCRIPTS_DIR.glob("**/*")))
    for known_script_path in paths:
        if known_script_path.is_file():
            name = str(known_script_path)
            name = name[name.find("scripts/") + len("scripts/"):]
            scripts[name] = known_script_path
    return scripts
def get_settings():
    with settings_file.open() as sf:
        settings = json.load(sf)

    if user_settings_file.is_file():
        with user_settings_file.open() as sf:
            user_settings = json.load(sf)
        settings.update(user_settings)
    return settings


def get_remote_known_packages():
    settings = get_settings()
    url = settings["known_packages_url"]
    response = urllib.request.urlopen(url)
    return json.load(response)


def update_user_known_package(package_name: str, config: dict(), pretty=True):
    logger.info(f"Update user known package. Package {package_name}")
    logger.debug(f"\n\tconfig = {config}\n\tpretty = {pretty}")

    with open(user_known_packages_file, "r") as jsonFile:
        data = json.load(jsonFile)
    data[package_name] = config
    with open(user_known_packages_file, "w") as jsonFile:
        if pretty:
            json.dump(data, jsonFile, ensure_ascii=False, sort_keys=True, indent=4)
        else:
            json.dump(data, jsonFile)


def init_user_configs_dir():
    if not USER_DATA_DIR.is_dir():
        USER_DATA_DIR.mkdir()
        logger.debug(f"Created USER_DATA_DIR: {USER_DATA_DIR}")
    if not USER_CONFIGS_DIR.is_dir():
        shutil.copytree(CONFIGS_DIR, USER_CONFIGS_DIR, copy_function=shutil.copy)
        logger.debug(f"Created USER_DATA_DIR: {USER_CONFIGS_DIR}")
    if not USER_SCRIPTS_DIR.is_dir():
        shutil.copytree(SCRIPTS_DIR, USER_SCRIPTS_DIR, copy_function=shutil.copy)
        logger.debug(f"Created USER_DATA_DIR: {USER_SCRIPTS_DIR}")


def get_known_packages(offline=False):
    init_user_configs_dir()

    logger.debug(f"Reading : {known_packages_file}")
    with known_packages_file.open() as sf:
        known_packages = json.load(sf)

    if not offline:
        try:
            known_packages = get_remote_known_packages()
        except (urllib.request.HTTPError, urllib.error.URLError) as e:
            if type(e) == urllib.request.HTTPError:
                logger.error(f"Error: code = {e.code}, url = {e.url}", exc_info=True)
            else:
                logger.error(f"Error!", exc_info=True)

    if user_known_packages_file.is_file():
        logger.debug(f"Reading : {user_known_packages_file}")
        with user_known_packages_file.open() as sf:
            user_known_packages = json.load(sf)
        known_packages.update(user_known_packages)
    logger.debug(f"In known_packages {len(known_packages)} packages")
    return known_packages

def get_packages_dependences_order(known_packages: dict, package: list):
    graph = dict()
    for name, data in known_packages.items():
        graph[name] = data.get('dependence', [])
    logger.debug(f"graph={graph}, known_packages keys={list(known_packages.keys())}")
    return iterative_topological_sort(graph, package, reverse=True)
