#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager
Данный модуль отвечает за управлетние отдельными пакетами
"""

from mpm.pm.package_managers import (get_installed_pms,
                                     AptGet,
                                     Conda,
                                     Pip,
                                     Snap,
                                     PackageManager,
                                     NPM,
                                     NAMES_TO_PACKAGE_MANAGERS,
                                     PACKAGE_MANAGERS_TO_NAMES,
                                     PACKAGE_MANAGERS_NAMES
                                     )
from mpm.utils.text_parse import parse_table_with_columns, parse_value_key_table, not_nan_split
from mpm.core.configs import get_known_packages, get_packages_dependences_order
from mpm.core.logging import getLogger
from mpm.shell import AutoShell, Shell

from plumbum import CommandNotFound, ProcessExecutionError
from mpm.utils.tools import inheritors
from mpm.core.exceptions import PackageManagerNotInatalled, PackageDoesNotExist, PackageDoesNotInatalled

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

    def __init__(self, package_name: str, shell: Shell = None):
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
        """
        Возвращает установлен ли данный пакетный менеджер
        """
        return self.pm.is_installed()

    def is_installed(self) -> bool:
        """
        Возвращает установлен ли данный пакет
        """
        return self.package_name in self.pm.get_all_packages()

    @classmethod
    def get_package_by_pm_name(cls, pm_name: str) -> "Package":
        """
        Возвращает коасс пакнта по названию пакетного менеджнра
        """
        for pkg_class in inheritors(cls):
            if pkg_class.pm_class.name == pm_name:
                return pkg_class

    def install(self):
        """
        Install package
        """
        raise NotImplementedError()

    def show(self) -> dict:
        """
        Позволяет получить информацию об установленном пакете 
        """
        raise NotImplementedError()

    def get_search_info(self) -> dict:
        """
        Позволяет получить информацию полученную из pm.search, а так же проверить пакет на существование
        """
        data_search = self.pm.search(self.package_name)
        data = data_search.get(self.package_name, None)
        if data == None:
            raise PackageDoesNotExist("Package not found: " + self.package_name)
        return data

    def get_info(self) -> dict:
        """
        Показывает всю информацию о пакете
        """
        info = self.get_search_info()
        if self.is_installed():
            data = self.show()
            info.update(data)
        return info

    def auto_config(self) -> dict:
        """
        Генерация конфигурации для последующей установки из known_packages
        """
        return {}

    def update_package_info(self):
        """
        Update self.info
        """
        self._info = self.get_info()

class AptGetPackage(Package):
    """ AptGet Package """

    pm_class = AptGet

    def show(self) -> dict:
        try:
            out = self.shell.call(["apt-cache", "show", self.package_name])
        except ProcessExecutionError as error:
            if "E: " in error.stderr:
                raise PackageDoesNotInatalled(
                    "Package not install: " + self.package_name
                )
            raise error
        out = self.pm._remove_warnings(out)
        info = parse_value_key_table(out, key_lower=True)
        if info == {}:
            raise PackageDoesNotInatalled("Package not found: " + self.package_name)
        return info
