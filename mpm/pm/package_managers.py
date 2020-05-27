#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager 
"""
from mpm.shell import AutoShell
from typing import List, Tuple
from mpm.utils.text_parse import is_first_ascii_alpha
from mpm.core.logging import getLogger
from mpm.core.exceptions import PackageDoesNotExist
from subprocess import CalledProcessError, STDOUT

logger = getLogger(__name__)

class PackageManager:
    """ Main Package Manager """

    executable_path: str

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __init__(self, shell: "AbstractShell" = None):
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


class NPM(PackageManager):
    """ Node js package manager """
    name = "npm"


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


def get_installed_pms() -> List[PackageManager]:
    pms_list = []
    for cls in PackageManager._inheritors():
        obj = cls()
        if obj.is_installed():
            pms_list.append(cls)
    return pms_list
