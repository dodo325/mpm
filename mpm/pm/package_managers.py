#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager 
"""
import re
from mpm.utils.tools import inheritors
from mpm.shell import AutoShell, Bash, ZSH, Shell
from plumbum import CommandNotFound

class PackageManager:

    executable_path: str

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __init__(self, shell: Shell = None):
        self.logger = logger.getChild(self.__class__.__name__)
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell

    def __str__(self):
        return f"{self.name}"

    def search(self, package_name: str) -> dict:
        """
        Поиск пакета по имени
        """
        raise NotImplementedError()

    def is_installed(self) -> bool:
        return self.shell.check_command(self.name)
