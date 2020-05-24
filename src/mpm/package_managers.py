#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Main Package Manager 
'''
from shell import AutoShell
from typing import List, Tuple
from text_parse import is_first_ascii_alpha
import logging

_LOG_PERFIX = "package_managers."

class PackageManager:
    """ Main Package Manager """

    executable_path: str

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __init__(self, shell=None):
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell

        self.logger = logging.getLogger(
            f'{_LOG_PERFIX}{self.name}')

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
    pass

class NPM(PackageManager):
    """ Node js package manager """
    pass

class Pip(PackageManager):
    """ Python Package Manager """
    pass

class Conda(PackageManager):
    """ Anaconda Python Package Manager """
    pass

class AptGet(PackageManager):
    """ Apt Package """
    name = "apt-get"

    def get_all_packages(self) -> List[str]:
        li = self.shell.cell(['dpkg -l | cut -d " " -f 3 | grep ""']).split("\n")
        self.logger.info(f"Detect {len(li)} packages")
        return list(filter(is_first_ascii_alpha, li))
    
    def update(
            self, 
            enter_password=False
        ):
        self.shell.sudo_cell([self.name, 'update'],
                             enter_password=enter_password)


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

# Package:
class Package:
    """ Package Class """
    package_name: str
    pm_class: "PackageManager" = None
    pm = None

    def __init__(self, package_name, shell=None):
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell
        self.package_name = package_name

        self.pm = self.pm_class(
            shell=self.shell
        )

        self.logger = logging.getLogger(
            f'{_LOG_PERFIX}{self.__class__.__name__.lower()}')

    def __str__(self):
        return f"{self.package_name}"

    def is_pm_installed(self) -> bool:
        return self.pm.is_installed()
        
    def is_installed(self) -> bool:
        return self.package_name in self.pm.get_all_packages()


class AptGetPackage(Package):
    """ AptGet Package """
    pm_class = AptGet

    _info = None

    @property
    def info(self) -> dict:
        if not self._info:
            self._info = self._get_info()
        return self._info

    def _get_info(self) -> dict:
        out = self.shell.cell(["apt-cache", "show", self.package_name])
        _TMP_MARK = "<!>"
        out = out.replace("\n ", _TMP_MARK)
        lines = out.split("\n")
        info = dict()
        for line in lines:
            if line == "":
                continue
            key, value = line.split(": ")
            info[key.lower()] = value.replace(_TMP_MARK, "\n ")
        return info

    def install(
            self,
            enter_password=False
        ):

        if self.is_installed():
            self.logger.info("Package already installed/")
            return
        self.logger.info(f"Installing {self.package_name}...")
        self.pm.update(enter_password=enter_password)
        self.shell.sudo_cell([self.pm.name, 'install', '-y', self.package_name],
                             enter_password=enter_password)
        

class AptPackage(AptGetPackage):
    """ Apt Package """
    pm_class = Apt

def main():
    zsh = AptPackage("zsh")
    zsh.pm.update()

if __name__ == "__main__":
    main()
