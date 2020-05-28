#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager 
"""
from typing import List, Tuple
from subprocess import CalledProcessError, STDOUT

from mpm.shell import AutoShell
from mpm.pm.package_managers import Apt, AptGet, Pip
from mpm.utils.text_parse import is_first_ascii_alpha
from mpm.utils.string import auto_decode
from mpm.core.logging import getLogger
from mpm.core.exceptions import PackageDoesNotExist, ShellError
logger = getLogger(__name__)

class Package:
    """ Package Class """

    package_name: str
    pm_class: "PackageManager" = None
    pm = None

    _info = None

    @property
    def info(self) -> dict:
        if not self._info:
            self._info = self._get_info()
        return self._info

    def _get_info(self) -> dict:
        return {"package": self.package_name}

    def __init__(self, package_name, shell=None):
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell
        self.package_name = package_name

        self.pm = self.pm_class(shell=self.shell)

        self.logger = getLogger(
            f"{_LOG_PERFIX}{self.__class__.__name__.lower()}"
        )

    def __str__(self):
        return f"{self.package_name}"

    def is_pm_installed(self) -> bool:
        return self.pm.is_installed()

    def is_installed(self) -> bool:
        return self.package_name in self.pm.get_all_packages()


class AptGetPackage(Package):
    """ AptGet Package """

    pm_class = AptGet

    def _get_info(self) -> dict:
        try:
            out = self.shell.cell(["apt-cache", "show", self.package_name])
        except CalledProcessError as e:
            if 'E: ' in e.output.decode("utf-8"):
                raise PackageDoesNotExist("Package not found: "+ self.package_name)
            raise ShellError("command '{}' return with error (code {}): {}".format(
                e.cmd, e.returncode, e.output))
        _TMP_MARK = "<!>"
        out = out.replace("\n ", _TMP_MARK)
        lines = out.split("\n")
        info = dict()
        for line in lines:
            if line == "":
                continue
            mark = ": "
            n = line.find(mark)
            key, value = line[:n], line[n + len(mark):]
            info[key.lower()] = value.replace(_TMP_MARK, "\n ")
        return info

    # def _install_software_properties_common():
    def check_repository(self, repository: str) -> bool:
        if not shell.check_command("add-apt-repository"):
            self.logger.error("Not found add-apt-repository!!!")
            # self._install_software_properties_common()

    def add_repository(self, repository: str):
        self.logger.info(f"Add repository {repository}")
        if not shell.check_command("add-apt-repository"):
            self.logger.error("Not found add-apt-repository!!!")
            # self._install_software_properties_common()
        if check_repository(repository):
            self.logger.success("Repository already add")

    def install(self, enter_password: bool = False, repository: str = None):
        if repository != None:
            self.add_repository(repository)

        if self.is_installed():
            self.logger.success("Package already installed")
            return

        self.logger.info(f"Installing {self.package_name} ({self.info})...")
        self.pm.update(enter_password=enter_password)
        self.shell.sudo_cell(
            [self.pm.name, "install", "-y", self.package_name],
            enter_password=enter_password,
        )

        if self.is_installed():
            self.logger.success("Package installed!")


class AptPackage(AptGetPackage):
    """ Apt Package """

    pm_class = Apt


class PipPackage(Package):
    """ Python PIP Package """

    pm_class = Pip

    def _get_info(self) -> dict:
        try:
            out = self.shell.cell(
                ["pip", "show", self.package_name])
        except CalledProcessError as e:
            if 'not found:' in auto_decode(e.output):
                raise PackageDoesNotExist("Package not found: "+ self.package_name)
            raise ShellError("command '{}' return with error (code {}): {}".format(
                e.cmd, e.returncode, e.output))
        _TMP_MARK = "<!>"
        out = out.replace("\n ", _TMP_MARK)
        lines = out.split("\n")
        lines = list(filter(None, lines))
        info = dict()
        for line in lines:
            if line == "":
                continue
            mark = ": "
            n = line.find(mark)
            key, value = line[:n], line[n + len(mark):]
            info[key.lower()] = value.replace(_TMP_MARK, "\n ")
        return info

    def install(self, repository: str = None):
        if self.is_installed():
            self.logger.success("Package already installed")
            return

        if repository != None:
            self.add_repository(repository)
        
        self.logger.info(f"Installing {self.package_name} ({self.info})...")
        self.shell.cell([self.pm.name, "install", self.package_name])

        if self.is_installed():
            self.logger.success("Package installed!")

# Универсальный пакет!


class UniversalePackage:
    """ Universale Package Class 
    Единый интерфейс взаимодействия с пакетными менеджарами. Кушает конфиги из known_packages
    """

    package_name: str
    _info = None

    @property
    def info(self) -> dict:
        if not self._info:
            self._info = self._get_info()
        return self._info

    def _get_info(self) -> dict:
        return {"package": self.package_name}

    def __init__(self, package_name, shell=None):
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell
        self.package_name = package_name

        self.pm = self.pm_class(shell=self.shell)

        self.logger = getLogger(
            f"{_LOG_PERFIX}{self.__class__.__name__.lower()}"
        )
