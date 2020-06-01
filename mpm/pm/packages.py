#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager
Данный модуль отвечает за управлетние отдельными пакетами
"""
from typing import List, Tuple
from subprocess import CalledProcessError, STDOUT

from mpm.shell import AutoShell, AbstractShell
from mpm.pm.package_managers import Snap, Apt, AptGet, Pip, PackageManager, Conda, NPM, get_installed_pms, NAMES_TO_PACKAGE_MANAGERS
from mpm.utils.text_parse import parse_table_with_columns, parse_value_key_table
from mpm.core.configs import get_known_packages
from mpm.utils.string import auto_decode
from mpm.core.logging import getLogger
from mpm.core.exceptions import PackageDoesNotExist, ShellError, PackageDoesNotInatalled
logger = getLogger(__name__)


class Package:
    """ Package Class """

    package_name: str
    pm_class: PackageManager = None
    pm = None

    _info = None
    @property
    def info(self) -> dict:
        if not self._info:
            self._info = self.get_info()
        return self._info

    def __init__(self, package_name: str, shell: AbstractShell = None):
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell
        self.package_name = package_name

        self.pm = self.pm_class(shell=self.shell)

        self.logger = logger.getChild(self.__class__.__name__)

    def __str__(self):
        return f"{self.package_name}"

    def is_pm_installed(self) -> bool:
        '''
        Возвращает установлен ли данный пакетный менеджер
        '''
        return self.pm.is_installed()

    def is_installed(self) -> bool:
        '''
        Возвращает установлен ли данный пакет
        '''
        return self.package_name in self.pm.get_all_packages()

    @classmethod
    def _inheritors(cls) -> list:
        '''
        Возвращает всех наследников данного класса
        '''
        subclasses = set()
        work = [cls]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        return list(subclasses)

    def install(self):
        '''
        Install package
        '''
        raise NotImplementedError()
    
    def get_search_info(self) -> dict:
        '''
        Позволяет получить информацию полученную из pm.search, а так же проверить пакет на существование
        '''
        data_search = self.pm.search(self.package_name)
        data = data_search.get(self.package_name, None)
        if data == None:
            raise PackageDoesNotExist(
                "Package not found: " + self.package_name)
        return data

    def show(self) -> dict:
        '''
        Позволяет получить информацию об установленном пакете 
        '''
        raise NotImplementedError()

    def get_info(self) -> dict:
        '''
        Показывает всю информацию о пакете
        '''
        info = self.get_search_info()
        if self.is_installed():
            data = self.show()
            info.update(data)
        return info

    def update_package_info(self):
        '''
        Update self.info
        '''
        self._info = self.get_info()


class AptGetPackage(Package):
    """ AptGet Package """
    pm_class = AptGet
    def show(self) -> dict:
        try:
            out = self.shell.cell(["apt-cache", "show", self.package_name])
        except CalledProcessError as e:
            if 'E: ' in e.output.decode("utf-8"):
                raise PackageDoesNotInatalled(
                    "Package not install: " + self.package_name)
            raise ShellError("command '{}' return with error (code {}): {}".format(
                e.cmd, e.returncode, e.output))
        out = self.pm._remove_warnings(out)
        info = parse_value_key_table(out, key_lower=True)
        if info == {}:
            raise PackageDoesNotInatalled(
                "Package not found: " + self.package_name)
        return info

    def install(self, enter_password: bool = False, repository: str = None):
        if repository != None:
            self.pm.add_repository(repository)

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
    
    def show(self) -> dict:
        try:
            out = self.shell.cell(
                ["pip", "show", self.package_name, '-v'])
        except CalledProcessError as e:
            if 'not found:' in auto_decode(e.output):
                raise PackageDoesNotInatalled(
                    "Package not found: " + self.package_name)
            raise ShellError("command '{}' return with error (code {}): {}".format(
                e.cmd, e.returncode, e.output))
        info = parse_value_key_table(out, key_lower=True)
        return info

class SnapPackage(Package):
    """ Snap Package """
    pm_class = Snap

    def get_info(self) -> dict:
        info = self.get_search_info()
        data = self.show()
        info.update(data)
        return info

    def show(self) -> dict:
        try:
            out = self.shell.cell(
                ["snap", "info", self.package_name])
        except CalledProcessError as e:
            raise ShellError("command '{}' return with error (code {}): {}".format(
                e.cmd, e.returncode, e.output))
        info = parse_value_key_table(out, key_lower=True)
        return info

class NPMPackage(Package):
    """ NPM Package """
    pm_class = NPM

    def get_info(self) -> dict:
        info = self.get_search_info()
        data = self.show()
        info.update(data)
        return info

    def show(self) -> dict:
        out = self.shell.cell(["npm", "view", package_name, '--json'])
        data = json.loads(out)
        data['version'] = data['versions'][-1]
        data.pop('name')
        return data

class CondaPackage(Package):
    """ Anaconda Package """
    pm_class = Conda

    def get_info(self) -> dict:
        return self.get_search_info()

