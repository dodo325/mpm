#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager 
"""
from mpm.shell import AutoShell, AbstractShell
from typing import List, Tuple
from mpm.utils.text_parse import is_first_ascii_alpha
from mpm.core.logging import getLogger
from mpm.core.exceptions import PackageDoesNotExist
from subprocess import CalledProcessError, STDOUT
import re
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


class Pip(PackageManager):
    """ Python Package Manager """
    name = "pip"
    def get_all_packages(self) -> List[str]:
        li = self.shell.cell([self.name, "freeze"]).split("\n")
        li = [s[: s.find("==")].lower() for s in li]
        li = list(filter(None, li))
        self.logger.info(f"Detect {len(li)} packages")
        return li


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

class AptGet(PackageManager):
    """ Apt Package """

    name = "apt-get"

    def get_all_packages(self) -> List[str]:
        li = self.shell.cell(['dpkg -l | cut -d " " -f 3 | grep ""']).split("\n")
        li = list(filter(is_first_ascii_alpha, li))
        self.logger.info(f"Detect {len(li)} packages")
        return li

    def update(self, enter_password=False):
        self.shell.sudo_cell([self.name, "update"], enter_password=enter_password)


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
    logger.debug(f"Output: {pms_list}")
    return pms_list
