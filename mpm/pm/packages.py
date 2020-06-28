#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager
Данный модуль отвечает за управлетние отдельными пакетами
"""
from typing import List, Tuple
from subprocess import CalledProcessError, STDOUT
import json

from mpm.shell import AutoShell, AbstractShell
from mpm.pm.package_managers import (
    Snap,
    Apt,
    AptGet,
    Pip,
    PackageManager,
    Conda,
    NPM,
    BashAliasManager,
    get_installed_pms,
    NAMES_TO_PACKAGE_MANAGERS,
)
from mpm.utils.text_parse import parse_table_with_columns, parse_value_key_table
from mpm.core.configs import get_known_packages, get_packages_dependences_order
from mpm.utils.string import auto_decode
from mpm.core.logging import getLogger
from mpm.core.exceptions import PackageManagerNotInatalled, PackageDoesNotExist, ShellError, PackageDoesNotInatalled
from mpm.scripts.bash import BashScriptFile

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
        for pkg_class in cls._inheritors():
            if pkg_class.pm_class.name == pm_name:
                return pkg_class

    @classmethod
    def _inheritors(cls) -> list:
        """
        Возвращает всех наследников данного класса
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

    def install(self):
        """
        Install package
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

    def show(self) -> dict:
        """
        Позволяет получить информацию об установленном пакете 
        """
        raise NotImplementedError()

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
        except CalledProcessError as e:
            if "E: " in e.output.decode("utf-8"):
                raise PackageDoesNotInatalled(
                    "Package not install: " + self.package_name
                )
            raise ShellError(
                "command '{}' return with error (code {}): {}".format(
                    e.cmd, e.returncode, e.output
                )
            )
        out = self.pm._remove_warnings(out)
        info = parse_value_key_table(out, key_lower=True)
        if info == {}:
            raise PackageDoesNotInatalled("Package not found: " + self.package_name)
        return info

    def install(self, enter_password: bool = False, repository: str = None):
        if repository != None:
            self.pm.add_repository(repository)

        if self.is_installed():
            self.logger.success("Package already installed")
            return

        self.logger.info(f"Installing {self.package_name} ({self.info})...")
        self.pm.update(enter_password=enter_password)
        self.shell.sudo_call(
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
        except CalledProcessError as e:
            if "not found:" in auto_decode(e.output):
                raise PackageDoesNotInatalled("Package not found: " + self.package_name)
            raise ShellError(
                "command '{}' return with error (code {}): {}".format(
                    e.cmd, e.returncode, e.output
                )
            )
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
        except CalledProcessError as e:
            raise ShellError(
                "command '{}' return with error (code {}): {}".format(
                    e.cmd, e.returncode, e.output
                )
            )
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
        out = self.shell.call(["npm", "view", self.package_name, "--json"])
        data = json.loads(out)
        data["version"] = data["versions"][-1]
        data.pop("name")
        return data


class CondaPackage(Package):
    """ Anaconda Package """

    pm_class = Conda

    def get_info(self) -> dict:
        return self.get_search_info()


# Bash
class BashAlias(Package):
    """
    Пользовательский alias. Устанавливается в .zshrc .bashrc или в файлы, которые указал пользователь
    """

    pm_class = BashAliasManager


    def __init__(
        self, package_name: str, shell: AbstractShell = None, profiles: List[str] = None
    ):
        super().__init__(package_name=package_name, shell=shell)
        self.pm.init_profiles(profiles=profiles)

    def is_installed(self) -> bool:
        self.update_package_info()
        return self.info != {}

    def install(self, cmd: str, profiles: List["str"] = None):
        """
        Устанавливает Alias во все файлы из profiles
        """
        if profiles:
            self.pm.init_profiles(profiles=profiles)
        for script in self.pm.profiles_scripts:
            script.add_alias(self.package_name, cmd)

    def auto_config(self) -> dict:
        return {
            "profiles": list(self.info.keys()),
            # TODO: а что делать если команды в различных файлах отличаются?
            "cmd": next(iter(self.info))
        }

    def get_info(self) -> dict:
        """
        Показывает всю информацию о alias

        Пример:
        >>> alias.get_info()
        {'/home/dodo/.zshrc': {'cmd': 'git'}, '/home/dodo/.bashrc': {'cmd': 'git'}}
        """
        info = {}
        for script in self.pm.profiles_scripts:
            aliases = script.get_alias()
            if self.package_name in aliases:
                info[str(script.file)] = {"cmd": aliases[self.package_name]}
        if info == {}:
             raise PackageDoesNotExist("Alias not found: " + self.package_name)
        return info


# UniversalePackage
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
    _info = None
    pm_packages: List[
        Package
    ] = []  # список валидных пакетных менеджеров для данного пакета

    @property
    def info(self) -> dict:
        if not self._info:
            self._info = self.get_info()
        return self._info

    def is_installed(self) -> bool:
        """
        Установленн ли пакет в системе
        """
        for pkg in self.pm_packages:
            if pkg.is_installed():
                self.logger.debug(
                    "Package {self.package_name} installed in {pkg.pm.name} package manager"
                )
                return True
        return False

    def update_package_info(self):
        """
        Update self.info
        """
        self._info = self.get_info()

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

        if not pms_classes:
            self.pms_classes = get_installed_pms(shell=self.shell)
        else:
            self.pms_classes = pms_classes

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
        for pkg_class in Package._inheritors():
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

    def ask_user_select_pm(self) -> "pm_package":
        """
        Просит пользователя выбрать один из пакетных метнджеров
        """
        if len(self.pm_packages) == 1:
            return self.pm_packages[0]

        pm_package_data = {
            i: {"name": pkg.pm.name, "pm_package": pkg}
            for i, pkg in enumerate(self.pm_packages)
        }
        print("Package Managers:")
        for x, y in pm_package_data.items():
            print(x, ":", pm_package_data[x]["name"])

        while True:
            print("\nSelect a package manager:")
            d_val = int(input())

            if d_val in pm_package_data.keys():
                d_val = int(d_val)
                print("\nYou have chosen {0}".format(pm_package_data[d_val]["name"]))
                return pm_package_data[d_val]["pm_package"]
            else:
                self.logger.warning("You chosen wrong!")

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
