#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager 
"""
from typing import List, Tuple
from subprocess import CalledProcessError, STDOUT

from mpm.shell import AutoShell
from mpm.pm.package_managers import Apt, AptGet, Pip, PackageManager, Conda, NPM, get_installed_pms, NAMES_TO_PACKAGE_MANAGERS
from mpm.utils.text_parse import is_first_ascii_alpha
from mpm.core.configs import get_known_packages
from mpm.utils.string import auto_decode
from mpm.core.logging import getLogger
from mpm.core.exceptions import PackageDoesNotExist, ShellError
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
            self._info = self._get_info()
        return self._info
    
    @property
    def version(self) -> str:
        return self.info["version"]

    def _get_info(self) -> dict:
        return {"package": self.package_name}


    def __init__(self, package_name, shell=None):
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
        return self.pm.is_installed()

    def is_installed(self) -> bool:
        return self.package_name in self.pm.get_all_packages()

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
        info.pop('w', None)
        info.pop('e', None)
        info.pop('W', None)
        info.pop('E', None)
        info.pop('N', None)
        if info == {}:
            raise PackageDoesNotExist( # FIXME: Не правда! Т.к. show показывает тольок из установленных пакетов
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
    
    Пример:
    >>> pkg = UniversalePackage("pytest")
    >>> pkg.info
    >>> pkg.install()
    >>> pkg.config
    {'package_managers': {'pip': {}}}
    """

    package_name: str
    config = dict()
    pms_classes = [] # TODO: refactor names
    auto_update_conf = True
    _info = None
    version = None
    @property
    def info(self) -> dict:
        if not self._info:
            self._info = self.get_info()
        return self._info

    def is_installed(self) -> bool:
        info = self.info
        for pm in self.pm_packages:
            if pm.is_installed():
                self.pm = pm
                self.version = pm.version
                return True
        return False
    
    

    def _get_correct_pms_classes_names(self, all_pm=False)->list:
        pms_names = list(self.config.get("package_managers", {}).keys())
        if pms_names == [] or all_pm:
            pms_names = [PM.name for PM in self.pms_classes]
        if 'apt' in pms_names and 'apt-get' in pms_names:
            pms_names.remove('apt-get')
        self.logger.debug(f"Out pms_names: {pms_names}")
        return pms_names
    
    def update_package_info(self):
        '''
        Update self.info and self.pm_packages
        '''
        # is_installed()
        self._info = self.get_info()


    def get_packages(self, all_pm=False) -> list:
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
                            shell=self.shell
                        )
                    )
        return pkg_objects
    
    def get_info(self, all_pm=False) -> dict:
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
                    self.add_package_manager_in_config(pkg.pm.name)
            except PackageDoesNotExist as e:
                self.logger.warn(
                    f"Package {pkg.package_name} Does Not found in '{pkg.pm.name}' package manager")
        self.logger.debug(f"'{self.package_name}' info: {info}")
        return info

    def add_package_manager_in_config(self, package_manager: str):
        if "package_managers" not in self.config:
            self.config["package_managers"] = {package_manager:{}}
            return
        if package_manager not in self.config["package_managers"]:
            self.config["package_managers"][package_manager] = {}

    def __init__(self, package_name, 
            shell=None, pms_classes: List[PackageManager] = None, 
            known_packages: dict() = None,
            offline=False,
            auto_update_conf=True
            ):
        self.package_name = package_name
        self.logger = logger.getChild(self.__class__.__name__)
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

    def ask_user_select_pm(self) -> "pm_package":
        # if len(self.pm_packages) == 1:
        #      return self.pm_packages[0]

        pm_package_data = {
            i: {"name": pkg.pm.name, "pm_package": pkg} for i, pkg in enumerate(self.pm_packages)
        }
        print("Package Managers:")
        for x, y in pm_package_data.items():
            print(x, ':', pm_package_data[x]['name'])

        while True:
            print("\nSelect a package manager:")
            d_val = int(input())

            if d_val in pm_package_data.keys():
                d_val = int(d_val)
                print("\nYou have chosen {0}".format(
                    pm_package_data[d_val]['name']))
                return pm_package_data[d_val]["pm_package"]
            else:
                print('\nYou chosen wrong!')

        
    def install(self, auto=False):
        self.update_package_info()
        if self.is_installed():
            logger.success("Package already installed")
            return

        package_managers_config = self.config["package_managers"]

        pkg = self.ask_user_select_pm()
        pkg_config = package_managers_config.get(pkg.pm.name, {})
        install_config = pkg_config.get("install", {})
        pkg.install(**install_config)
       
