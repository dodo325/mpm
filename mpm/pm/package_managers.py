#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager 
"""
from mpm.utils.tools import inheritors
from mpm.shell import AutoShell, Bash, ZSH, Shell
from plumbum import FG, BG
from plumbum import CommandNotFound
from plumbum.commands.base import BoundCommand
from mpm.core.logging import getLogger
from typing import List
from mpm.utils.string import is_first_ascii_alpha
from mpm.utils.text_parse import parse_value_key_table, not_nan_split, parse_table_with_columns
import re
import json

logger = getLogger(__name__)

class PackageManager:

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __init__(self, shell: Shell = None):
        self.logger = logger.getChild(self.__class__.__name__)
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell

    def __str__(self):
        return f"{self.name}"

    def search(self, package_name: str) -> dict:
        """
        Поиск пакета по имени
        """
        raise NotImplementedError()
    
    def is_installed(self) -> bool:
        return self.shell.check_command(self.name)

class AptGet(PackageManager):
    """ Apt Package Manager """

    name = "apt-get"

    def _remove_warnings(self, consol_output: str, error=False) -> str:
        out = ""
        perfix_list = ["W", "N"]
        if error:
            perfix_list.append("E")
        for line in consol_output.splitlines():
            if not line.startswith(tuple(perfix_list)):
                out += line + "\n"
        return out

    def get_all_packages(self) -> List[str]:
        li = self.shell.cmd('dpkg -l | cut -d " " -f 3 | grep ""').split("\n")
        li = list(filter(is_first_ascii_alpha, li))
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def update(self):
        return self.shell.sudo_call([self.name, "update"])

    def get_list_repository(self) -> List[str]:
        li = not_nan_split(self.shell.call(
            ["grep ^ /etc/apt/sources.list /etc/apt/sources.list.d/*"]))
        li = list(map(lambda s: s[s.find(':') + 1:], li))
        li = list(filter(lambda s: not s.startswith("#"), li))
        li = list(filter(None, li))
        return li

    def search(self, package_name: str) -> dict:
        try:
            out = self.shell.call(["apt-cache", "search", package_name])
        except Exception as e:
            self.logger.error(f"Nothing found for {package_name}!")
            return {}
        out = self._remove_warnings(out)
        if out == "":
            return {}
        data = {}
        for line in not_nan_split(out):
            delimiter = " - "
            n = line.find(delimiter)
            name = line[:n]
            description = line[n + len(delimiter):]
            data[name] = {"description": description}
        return data

class Apt(AptGet):
    """ Apt Package """
    name = "apt"

class Conda(PackageManager):
    """ Anaconda Python Package Manager """
    name = "conda"
    def get_all_packages(self, no_pip=True) -> List[str]:
        cmd = [self.name, "list"]
        if no_pip:
            cmd.append("--no-pip")
        out = self.shell.call(cmd)
        rex = r"\n[^#]\S+(?=\s)"
        li = re.findall(rex, out)
        li = [s.replace("\n", "") for s in li]
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        try:
            out = self.shell.call(["conda", "search", package_name, "--json"])
        except Exception as e:
            self.logger.error(f"Nothing found for {package_name}!")  # , exc_info=True)
            return {}
        data = json.loads(out)
        out_data = {}
        for builds_list in data.values():
            last_build = builds_list[-1]
            name = last_build.pop("name")
            out_data[name] = last_build
        return out_data

class Snap(PackageManager):
    """ Python Package Manager """

    name = "snap"
# snap нфшёл на пустой arch системе!

    def get_all_packages(self) -> List[str]:
        out = self.shell.call(["snap", "list"])
        rex = r"\n\S+(?=\s)"
        li = re.findall(rex, out)
        li = [s.replace("\n", "") for s in li]
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        try:
            out = self.shell.call(["LANG=en_US.UTF-8;", "snap", "find", package_name])
        except Exception as e:
            self.logger.error(f"Nothing found for {package_name}!")
            return {}
        return parse_table_with_columns(out, key_lower=True)

class ShellManager(PackageManager):
    """ Shell scripts for install """
    name = "shell"

    def is_installed(self) -> bool:
        return self.shell.is_installed()

class NPM(PackageManager):
    """ Node js package manager """

    name = "npm"

    def get_all_packages(self) -> List[str]:
        out = self.shell.call(["npm list -g --depth=0"])
        # npm list -g --depth=0 --json
        rex = r"(?=\s).+(?=@)"
        li = re.findall(rex, out)
        li = [s.replace(" ", "") for s in li]
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        try:
            out = self.shell.call(["npm", "search", package_name])
        except Exception as error:
            self.logger.error(f"Nothing found for {package_name}!")
            return {}
        return parse_table_with_columns(out, key_lower=True, delimiter="|")


class Pip(PackageManager):
    """ Python Package Manager """

    name = "pip"

    def get_all_packages(self) -> List[str]:
        li = self.shell.call([self.name, "freeze"]).split(
            "\n")  # TODO: use "pip list --format=json"
        li = [s[: s.find("==")].lower() for s in li]
        li = list(filter(None, li))
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        """
        RAW output:
        numpy (1.18.4)                            - NumPy is the fundamental package
                                                    for array computing with Python.
          INSTALLED: 1.18.1
          LATEST:    1.18.4
        numpy-cloud (0.0.5)                       - Numpy in the cloud
        numpy-ext (0.9.2)                         - numpy extension
        numpy-alignments (0.0.2)                  - Numpy Alignments
        numpy-utils (0.1.6)                       - NumPy utilities.
        """
        try:
            out = self.shell.call(["pip", "search", package_name])
        except Exception as e:
            self.logger.error(f"Nothing found for {package_name}!")  # , exc_info=True)
            return {}
        li = not_nan_split(out)
        data = {}
        name = ''
        for line in li:
            try:
                if line.startswith(" "):
                    key, val = line.split(":")
                    key, val = key.strip(), val.strip()
                    key, val = key.lower(), val.lower()
                    data[name][key] = val
                    continue

                version = re.search(r"\((.*?)\)", line).group(1)
                name = line[: line.find("(")].strip()
                description = line[line.rfind("-") + 1:].strip()
                data[name] = {"version": version, "description": description}
            except (AttributeError, ValueError):
                self.logger.debug("SearchParseError", exc_info=True)
                continue
        return data



def get_installed_pms(shell: AutoShell = None) -> List[PackageManager]:
    pms_list = []
    if not shell:
        shell = AutoShell()
    for cls in inheritors(PackageManager):
        obj = cls(shell=shell)
        if obj.is_installed():
            pms_list.append(cls)
    pm_names = [pm.name for pm in pms_list]
    logger.info(f"Installed packege managers: {pm_names}")
    return pms_list


NAMES_TO_PACKAGE_MANAGERS = {cls.name: cls for cls in inheritors(PackageManager)}
PACKAGE_MANAGERS_TO_NAMES = {cls: cls.name for cls in inheritors(PackageManager)}
PACKAGE_MANAGERS_NAMES = list(NAMES_TO_PACKAGE_MANAGERS.keys())
