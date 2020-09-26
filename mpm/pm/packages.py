#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager
Данный модуль отвечает за управлетние отдельными пакетами
"""

from mpm.pm.package_managers import (get_installed_pms,
                                     AptGet,
                                     Apt,
                                     Conda,
                                     Pip,
                                     Snap,
                                     PackageManager,
                                     ShellManager,
                                     NPM,
                                     NAMES_TO_PACKAGE_MANAGERS,
                                     PACKAGE_MANAGERS_TO_NAMES,
                                     PACKAGE_MANAGERS_NAMES
                                     )
from mpm.utils.text_parse import parse_table_with_columns, parse_value_key_table, not_nan_split
from mpm.core.configs import get_known_packages, get_packages_dependences_order
from mpm.core.logging import getLogger
from mpm.shell import AutoShell, Shell
from typing import List

from rich.prompt import Prompt
from rich import print

from plumbum import CommandNotFound, ProcessExecutionError
from mpm.utils.tools import inheritors
from mpm.core.exceptions import PackageManagerNotInatalled, PackageDoesNotExist, PackageDoesNotInatalled
import json

logger = getLogger(__name__)

class Package:
    """ Package Class """
    package_name: str
    pm_class: PackageManager = None
    pm = None

    _info = {}

    @property
    def info(self) -> dict:
        if self._info == {} or not self._info:
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

class ShellPackage(Package):
    """ Artificial Package via Shell """

    pm_class = ShellManager

    def install(self, cmd: str, is_sudo=False):
        self.logger.info(f"Installing {self.package_name} using {self.shell.name}...")
        if is_sudo:
            self.shell.sudo_call([cmd])
        else:
            self.shell.call([cmd])
            
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

    def remove(self):
        if not self.is_installed():
            self.logger.info("Package not installed")
            return
        
        self.shell.sudo_call(
            [self.pm.name, "remove", "-y", self.package_name]
        )

        if not self.is_installed():
            self.logger.success("Package removed!")
        
    def install(self, repository: str = None):
        if self.is_installed():
            self.logger.success("Package already installed")
            return
        self.logger.info(
            f"Removing {self.package_name} ({self.info})...", extra={"markup": True})
        if repository != None:
            self.pm.add_repository(repository) # todo
        
        self.logger.info(f"Installing {self.package_name} ({self.info})...")
        self.pm.update()
        self.shell.sudo_call(
            [self.pm.name, "install", "-y", self.package_name]
        )

        if self.is_installed():
            self.logger.success("Package installed!")
        else:
            self.logger.warning("Package not installed")

        

class AptPackage(AptGetPackage):
    """ Apt Package """
    pm_class = Apt

class PipPackage(Package):
    """ Python PIP Package """

    pm_class = Pip

    def install(self):
        if self.is_installed():
            self.logger.success("Package already installed")
            return

        self.logger.info(f"Installing {self.package_name} ({self.info})...")
        self.shell.call([self.pm.name, "install", self.package_name])

        if self.is_installed():
            self.logger.success("Package installed!")

    def remove(self):
        if not self.is_installed():
            self.logger.info("Package not installed")
            return

        self.logger.info(f"Removing {self.package_name} ({self.info})...")
        self.shell.call([self.pm.name, "uninstall", "-y", self.package_name])

        if not self.is_installed():
            self.logger.success("Package removed!")

    def show(self) -> dict:
        try:
            out = self.shell.call(["pip", "show", self.package_name, "-v"])
        except ProcessExecutionError as error:
            if "not found:" in error.stderr:
                raise PackageDoesNotInatalled("Package not found: " + self.package_name)
            else:
                self.console.print_exception()
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

    def install(self, argument: str = None):
        """
        Этот метод не работает в Jupyter. Иногда надо указывать argument="--classic"
        """
        if self.is_installed():
            self.logger.success("Package already installed")
            return

        self.logger.info(f"Installing {self.package_name} ({self.info})...")
        cmd = [self.pm.name, "install", self.package_name]
        if argument:
            cmd.append(argument)
        self.shell.call(cmd)

        if self.is_installed():
            self.logger.success("Package installed!")

    def show(self) -> dict:
        try:
            out = self.shell.call(["snap", "info", self.package_name])
        except ProcessExecutionError as e:
            self.console.print_exception()
            
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

    def is_installed(self) -> bool:
        """
        Возвращает установлен ли данный пакет
        """
        # TODO: должен проверять нет ли поблизости node_modules и данного пакнта
        return self.package_name in self.pm.get_all_packages()

    def install(self, argument: str = None):  # TODO: он в текущую папку устанавлевает!
        if self.is_installed():
            self.logger.success("Package already installed")
            return

        self.logger.info(f"Installing {self.package_name} ({self.info})...")
        cmd = [self.pm.name, "install", self.package_name]
        if argument:
            cmd.append(argument)
        self.shell.call(cmd)

        if self.is_installed():
            self.logger.success("Package installed!")

    def show(self) -> dict:
        try:
            out = self.shell.call(["npm", "view", self.package_name, "--json"])
        except ProcessExecutionError as e:
            self.console.print_exception()
        # out = out[out.find("{\n"):]
        out_2 = ""
        for line in not_nan_split(out):
            if not line.startswith("npm"):
                out_2 += line + "\n"
        out = out_2
        data = json.loads(out)
        data["version"] = data["versions"][-1]
        data.pop("name")
        return data


class CondaPackage(Package):
    """ Anaconda Package """

    pm_class = Conda

    def get_info(self) -> dict:
        return self.get_search_info()

class UniversalePackage:
    """ Universale Package Class 
    Единый интерфейс взаимодействия с пакетными менеджарами. Кушает конфиги из known_packages
    
    Пример:
    >>> pkg = UniversalePackage("pytest")
    >>> pkg.info
    >>> pkg.install()
    >>> pkg.config
    {'package_managers': {'pip': {}}}
    """

    package_name: str
    config = dict()
    pms_classes: List[PackageManager] = []
    auto_update_conf = True
    dependences_order = []
    _info = {}
    pm_packages: List[
        Package
    ] = []  # список валидных пакетных менеджеров для данного пакета

    @property
    def info(self) -> dict:
        if self._info == {} or not self._info:
            self._info = self.get_info()
            self.is_installed()
        return self._info

    def is_installed(self) -> bool:
        """
        Установленн ли пакет в системе
        """
        for pkg in self.pm_packages:
            is_installed = pkg.is_installed()
            if pkg.pm.name in self._info:
                if self._info[pkg.pm.name] == None:
                    self._info[pkg.pm.name] = {}
                self._info[pkg.pm.name]["is_installed"] = is_installed
            else:
                self._info[pkg.pm.name] = {"is_installed": is_installed}
            if is_installed:
                self.logger.info(
                    f"Package '{self.package_name}' installed in '{pkg.pm.name}' package manager"
                )
                return True
        return False

    def update_package_info(self, all_pm=False):
        """
        Update self.info
        """
        self._info = self.get_info(all_pm=all_pm)
        self.is_installed()

    def __init__(
        self,
        package_name,
        shell=None,
        pms_classes: List[PackageManager] = None,
        known_packages: dict() = None,
        offline=False,
        auto_update_conf=True,
    ):
        self.package_name = package_name
        self.logger = logger.getChild(self.__class__.__name__)

        self.logger.debug(
            f"Args:\n\tpackage_name = {package_name}\n\tshell = {shell}\n\tpms_classes = {pms_classes}\n\toffline = {offline}\n\tauto_update_conf = {auto_update_conf}\n\tis_known_packages = {known_packages != None}")

        self.auto_update_conf = auto_update_conf
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell

        if not known_packages:
            known_packages = get_known_packages(offline=offline)

        if package_name in known_packages:
            logger.info(f"Package '{package_name}' found in known_packages")
            self.config = known_packages[package_name]
            self.dependences_order = get_packages_dependences_order(
                known_packages,
                package_name
            )
        else:
            self.dependences_order = [package_name]
        
        if not pms_classes:
            self.pms_classes = get_installed_pms(shell=self.shell)
        else:
            self.pms_classes = pms_classes

        self.update_package_info()

    def _get_correct_pms_classes_names(self, all_pm=False) -> List[str]:
        pms_names = []
        if all_pm:
            pms_names = [PM.name for PM in get_installed_pms(shell=self.shell)]
        else:
            pms_names = [PM.name for PM in self.pms_classes]
            known_pms_names = list(self.config.get("package_managers", {}).keys())
            logger.debug(
                f"Vars:\n\tself.pms_classes = {self.pms_classes}\n\ttmp = {pms_names}\n\tknown_pms_names={known_pms_names}")
            if known_pms_names != []:
                tmp = set(pms_names)
                tmp.intersection_update(set(known_pms_names))
                pms_names = list(tmp)

        if pms_names == []:
            raise PackageManagerNotInatalled()

        if "apt" in pms_names and "apt-get" in pms_names:
            pms_names.remove("apt-get")
        self.logger.debug(f"Out pms_names: {pms_names}")
        return pms_names

    def get_packages(self, all_pm=False) -> List[Package]:
        """
        Из  self.pms_classes или self.config получаем объекты packages
        """
        pms_names = self._get_correct_pms_classes_names(all_pm=all_pm)
        self.logger.debug(f"pms_names: {pms_names}")
        pkg_objects = []
        config_menegers = self.config.get("package_managers", {})
        for pkg_class in inheritors(Package):
            if pkg_class.pm_class.name in pms_names:
                pm_config = config_menegers.get(pkg_class.pm_class.name, {})
                pkg_objects.append(
                    pkg_class(
                        pm_config.get("package_name", self.package_name),
                        shell=self.shell,
                        # TODO: доп параметры
                    )
                )
        return pkg_objects

    def add_package_manager_in_config(self, package_manager: str, pm_config: dict = {}):
        """
        Добавить новый пакетный менеджер в self.config
        """
        self.logger.info(f"Detected in {package_manager}!")
        if "package_managers" not in self.config:
            self.config["package_managers"] = {package_manager: pm_config}
            return
        if package_manager not in self.config["package_managers"]:
            self.config["package_managers"][package_manager] = pm_config

    def get_info(self, all_pm=False) -> dict:
        """
        Получаем всю информацию о пакете
        Попутно обновляем self.pm_packages и self.config
        """
        info = dict()
        self.pm_packages = []
        pm_packages = self.get_packages(all_pm=all_pm)
        self.logger.debug(f"pm_packages: {pm_packages}")
        for pkg in pm_packages:
            try:
                self.logger.debug(f"Search '{pkg.package_name}' in {pkg.pm.name}")
                info[pkg.pm.name] = pkg.info
                self.pm_packages.append(pkg)
                if self.auto_update_conf:
                    pm_config = pkg.auto_config()
                    self.add_package_manager_in_config(pkg.pm.name, pm_config=pm_config)
            except PackageDoesNotExist as e:
                self.logger.warning(
                    f"Package {pkg.package_name} Does Not found in '{pkg.pm.name}' package manager"
                )
        self.logger.debug(f"'{self.package_name}' info: {info}")
        return info

    def install(self, auto=False):
        self.update_package_info()
        if self.is_installed():
            logger.success("Package already installed")
            return

        package_managers_config = self.config["package_managers"]

        pkg = self.ask_user_select_pm()
        if self.auto_update_conf:
            pm_config = pkg.auto_config()
            self.add_package_manager_in_config(pkg.pm.name, pm_config=pm_config)
        pkg_config = package_managers_config.get(pkg.pm.name, {})
        install_config = pkg_config.get("install", {})
        pkg.install(**install_config)

    def ask_user_select_pm(self) -> Package:
        """
        Просит пользователя выбрать один из пакетных метнджеров
        """
        if len(self.pm_packages) == 1:
            return self.pm_packages[0]

        pm_package_data = {
            pkg.pm.name: pkg for pkg in self.pm_packages
        }

        pm_name = Prompt.ask("\nSelect a package manager:",
                             choices=list(pm_package_data.keys()))
        return pm_package_data[pm_name]
