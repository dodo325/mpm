#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager 
"""
from mpm.shell import AutoShell, AbstractShell
from typing import List, Tuple
from mpm.utils.string import is_first_ascii_alpha
from mpm.core.logging import getLogger
from mpm.utils.text_parse import parse_table_with_columns, parse_value_key_table, not_nan_split
from mpm.core.exceptions import PackageDoesNotExist
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
        subclasses = set()
        work = [cls]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        return list(subclasses)

    def search(self, package_name: str) -> dict:
        '''
        Поиск пакета по имени
        '''
        raise NotImplementedError()

    def is_installed(self) -> bool:
        return self.shell.check_command(self.name)


class Snap(PackageManager):
    """ Python Package Manager """
    name = "snap"

    def get_all_packages(self) -> List[str]:
        out = self.shell.cell(['snap', 'list'])
        rex = r"\n\S+(?=\s)"
        li = re.findall(rex, out)
        li = [s.replace("\n", "") for s in li]
        self.logger.info(f"Detect {len(li)} packages")
        return li
    
    def search(self, package_name: str) -> dict:
        out = self.shell.cell(
            ['LANG=en_US.UTF-8;', 'snap', 'find', package_name])
        return parse_table_with_columns(out, key_lower=True)

class NPM(PackageManager):
    """ Node js package manager """
    name = "npm"

    def get_all_packages(self) -> List[str]:
        out = self.shell.cell('npm list -g --depth=0')
        rex = r"(?=\s).+(?=@)"
        li = re.findall(rex, out)
        li = [s.replace(" ", "") for s in li]
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        out = self.shell.cell(['npm', 'search', package_name])
        return parse_table_with_columns(out, key_lower=True, delimiter="|")

class Pip(PackageManager):
    """ Python Package Manager """
    name = "pip"
    def get_all_packages(self) -> List[str]:
        li = self.shell.cell([self.name, "freeze"]).split("\n")
        li = [s[: s.find("==")].lower() for s in li]
        li = list(filter(None, li))
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        '''
        numpy (1.18.4)                            - NumPy is the fundamental package
                                                    for array computing with Python.
          INSTALLED: 1.18.1
          LATEST:    1.18.4
        numpy-cloud (0.0.5)                       - Numpy in the cloud
        numpy-ext (0.9.2)                         - numpy extension
        numpy-alignments (0.0.2)                  - Numpy Alignments
        numpy-utils (0.1.6)                       - NumPy utilities.
        numpy-demo (1.23.0)                       - NumPy-demo is a test package and
                                                    is a clone of numpy.
        numpy-sugar (1.5.0)                       - Missing NumPy functionalities
        numpy-turtle (0.2)                        - Turtle graphics with NumPy
        numpy-linreg (0.1.0)                      - Linear Regression with numpy only.
        root-numpy (4.8.0)                        - The interface between ROOT and
                                                    NumPy
        mapchete-numpy (0.1)                      - Mapchete NumPy read/write
                                                    extension
        numpy-nn (0.2.6)                          - Numpy NN is a Deep Neural Network
                                                    Package which is built on base
                                                    Numpy operations. This project is
                                                    under development and any
                                                    contributions are welcome.

        '''
        out = self.shell.cell(['pip', 'search', package_name])
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
            name = line[:line.find("(")].strip()
            description = line[line.rfind("-")+1:].strip()
            data[name] = {
                'version': version,
                'description': description
            }
        return data

class Conda(PackageManager):
    """ Anaconda Python Package Manager """
    name = "conda"

    def get_all_packages(self, no_pip = True) -> List[str]:
        cmd = [self.name, 'list']
        if no_pip:
            cmd.append("--no-pip")
        out = self.shell.cell(cmd)
        rex = r"\n[^#]\S+(?=\s)"
        li = re.findall(rex, out)
        li = [s.replace("\n", "") for s in li]
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def search(self, package_name: str) -> dict:
        out = self.shell.cell(["conda", "search", package_name, "--json"])
        data = json.loads(out)
        out_data = {}
        for builds_list in data.values():
            last_build = builds_list[-1]
            name = last_build.pop('name')
            out_data[name] = last_build
        return out_data

class AptGet(PackageManager):
    """ Apt Package """

    name = "apt-get"
    # def _install_software_properties_common():

    def _remove_warnings(self, consol_output: str, error= False) -> str:
        out = ""
        perfix_list = ['W', 'N']
        if error:
            perfix_list.append('E')
        for line in consol_output.splitlines():
            if not line.startswith(tuple(perfix_list)):
                out += line + '\n'
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
        pass # TODO: поиск и удаление регистри

    def get_all_packages(self) -> List[str]:
        li = self.shell.cell(['dpkg -l | cut -d " " -f 3 | grep ""']).split("\n")
        li = list(filter(is_first_ascii_alpha, li))
        self.logger.info(f"Detect {len(li)} packages")
        return li
    
    def update(self, enter_password=False):
        self.shell.sudo_cell([self.name, "update"], enter_password=enter_password)

    def search(self, package_name: str) -> dict:
        out = self.shell.cell(["apt-cache", "search", package_name])
        out = self._remove_warnings(out)
        if out == '':
            return {}
        data = {}
        for line in not_nan_split(out):
            delimiter = " - "
            n = line.find(delimiter)
            name = line[:n]
            description = line[n+len(delimiter):]
            data[name] = {"description": description}
        return data
        
class Apt(AptGet):
    """ Apt Package """
    name = "apt"


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


NAMES_TO_PACKAGE_MANAGERS = {
    cls.name: cls for cls in PackageManager._inheritors()
}
PACKAGE_MANAGERS_TO_NAMES = {
    cls: cls.name for cls in PackageManager._inheritors()
}
PACKAGE_MANAGERS_NAMES = list(NAMES_TO_PACKAGE_MANAGERS.keys())
