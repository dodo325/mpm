#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager 
"""
from mpm.shell import AutoShell, AbstractShell, Bash
from typing import List, Tuple
from mpm.utils.string import is_first_ascii_alpha
from mpm.core.logging import getLogger
from mpm.utils.text_parse import (
    parse_table_with_columns,
    parse_value_key_table,
    not_nan_split,
)
from mpm.core.exceptions import PackageDoesNotExist
from mpm.scripts.bash import BashScriptFile
from subprocess import CalledProcessError, STDOUT
import re
import json

logger = getLogger(__name__)


class PackageManager:
    """ Main Package Manager """

    executable_path: str

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __init__(self, shell: AbstractShell = None):
        self.logger = logger.getChild(self.__class__.__name__)
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def _inheritors(cls) -> list:
        """
        return all subclasses
        """
        subclasses = []
        work = [cls]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.append(child)
                    work.append(child)
        return subclasses

    def search(self, package_name: str) -> dict:
        """
        Поиск пакета по имени
        """
        raise NotImplementedError()

    def is_installed(self) -> bool:
        return self.shell.check_command(self.name)


class Snap(PackageManager):
    """ Python Package Manager """

    name = "snap"

    def get_all_packages(self) -> List[str]:
        out = self.shell.call(["snap", "list"])
        rex = r"\n\S+(?=\s)"
        li = re.findall(rex, out)
        li = [s.replace("\n", "") for s in li]
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        out = self.shell.call(["LANG=en_US.UTF-8;", "snap", "find", package_name])
        return parse_table_with_columns(out, key_lower=True)


class NPM(PackageManager):
    """ Node js package manager """

    name = "npm"

    def get_all_packages(self) -> List[str]:
        out = self.shell.call("npm list -g --depth=0")
        rex = r"(?=\s).+(?=@)"
        li = re.findall(rex, out)
        li = [s.replace(" ", "") for s in li]
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        out = self.shell.call(["npm", "search", package_name])
        return parse_table_with_columns(out, key_lower=True, delimiter="|")


class Pip(PackageManager):
    """ Python Package Manager """

    name = "pip"

    def get_all_packages(self) -> List[str]:
        li = self.shell.call([self.name, "freeze"]).split("\n")
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
        except CalledProcessError as e:
            self.logger.error(f"Nothing found for {package_name}!") #, exc_info=True)
            return {}
        li = not_nan_split(out)
        data = {}
        for line in li:
            if line.startswith(" "):
                key, val = line.split(":")
                key, val = key.strip(), val.strip()
                key, val = key.lower(), val.lower()
                data[name][key] = val
                continue
            version = re.search(r"\((.*?)\)", line).group(1)
            name = line[: line.find("(")].strip()
            description = line[line.rfind("-") + 1 :].strip()
            data[name] = {"version": version, "description": description}
        return data


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
        except CalledProcessError as e:
            self.logger.error(f"Nothing found for {package_name}!") # , exc_info=True)
            return {}
        data = json.loads(out)
        out_data = {}
        for builds_list in data.values():
            last_build = builds_list[-1]
            name = last_build.pop("name")
            out_data[name] = last_build
        return out_data


class AptGet(PackageManager):
    """ Apt Package """

    name = "apt-get"
    # def _install_software_properties_common():

    def _remove_warnings(self, consol_output: str, error=False) -> str:
        out = ""
        perfix_list = ["W", "N"]
        if error:
            perfix_list.append("E")
        for line in consol_output.splitlines():
            if not line.startswith(tuple(perfix_list)):
                out += line + "\n"
        return out

    def check_repository(self, repository: str) -> bool:
        if not self.shell.check_command("add-apt-repository"):
            self.logger.error("Not found add-apt-repository!!!")
            # self._install_software_properties_common()

    def add_repository(self, repository: str):
        self.logger.info(f"Add repository {repository}")
        if not self.shell.check_command("add-apt-repository"):
            self.logger.error("Not found add-apt-repository!!!")
            # self._install_software_properties_common()
        if check_repository(repository):
            self.logger.success("Repository already add")

    def remove_repository(self, repository: str):
        pass  # TODO: поиск и удаление регистри

    def get_all_packages(self) -> List[str]:
        li = self.shell.call(['dpkg -l | cut -d " " -f 3 | grep ""']).split("\n")
        li = list(filter(is_first_ascii_alpha, li))
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def update(self, enter_password=False):
        self.shell.sudo_call([self.name, "update"], enter_password=enter_password)

    def search(self, package_name: str) -> dict:
        out = self.shell.call(["apt-cache", "search", package_name])
        out = self._remove_warnings(out)
        if out == "":
            return {}
        data = {}
        for line in not_nan_split(out):
            delimiter = " - "
            n = line.find(delimiter)
            name = line[:n]
            description = line[n + len(delimiter) :]
            data[name] = {"description": description}
        return data


class Apt(AptGet):
    """ Apt Package """

    name = "apt"


# Scripts:

## Bash
class BashAliasManager(PackageManager):
    """
    Класс управления пользовательскими alias
    """

    name = "bash-alias"
    profiles: List["str"] = ["$HOME/.zshrc", "$HOME/.bashrc"]
    profiles_scripts: List[BashScriptFile] = []

    def __init__(self, shell: AbstractShell = None, profiles: List["str"] = None):
        self.logger = logger.getChild(self.__class__.__name__)
        if shell != None and shell.name == "bash":
            self.shell = shell
        else:
            self.shell = Bash()
        if profiles:
            self.profiles = profiles

        self.init_profiles()

    def init_profiles(self, profiles: List["str"] = None):
        if profiles:
            self.profiles = profiles

        for path in self.profiles:
            try:
                self.profiles_scripts.append(BashScriptFile(path, shell=self.shell))
            except FileExistsError as e:
                self.logger.warn(e)

    def is_installed(self) -> bool:
        return self.shell.is_installed()
    
    def get_all_packages(self) -> List[str]:
        names = set()
        for script in self.profiles_scripts:
            aliases = script.get_alias()
            names.update(aliases.keys())
        return list(names)

    def search(self, package_name: str) -> dict:
        data = {}
        self.logger.info(f"Search in {self.profiles}")
        for script in self.profiles_scripts:
            aliases: dict = script.get_alias()
            for aliase_name, aliase in aliases.items():
                if aliase_name.startswith(package_name):
                    data[aliase_name] = {"cmd": aliase, "file": str(script.file)}
        return data
# class BashScriptFileManager(BashAliasManager):
#     """
#     Класс управления пользовательскими скриптовыми файлами
#     """
#     name = "bash-script"


def get_installed_pms(shell: AbstractShell = None) -> List[PackageManager]:
    pms_list = []
    if not shell:
        shell = AutoShell()
    for cls in PackageManager._inheritors():
        obj = cls(shell=shell)
        if obj.is_installed():
            pms_list.append(cls)
    pm_names = [pm.name for pm in pms_list]
    logger.info(f"Installed packege managers: {pm_names}")
    return pms_list


NAMES_TO_PACKAGE_MANAGERS = {cls.name: cls for cls in PackageManager._inheritors()}
PACKAGE_MANAGERS_TO_NAMES = {cls: cls.name for cls in PackageManager._inheritors()}
PACKAGE_MANAGERS_NAMES = list(NAMES_TO_PACKAGE_MANAGERS.keys())
