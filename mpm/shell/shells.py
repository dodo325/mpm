#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager Shell 

This module works with the system shell.
"""
from plumbum.machines import LocalMachine, SshMachine
from plumbum.machines.paramiko_machine import ParamikoMachine
from plumbum import FG, BG
from typing import List
from subprocess import check_output, Popen, PIPE, STDOUT
import re
from mpm.utils.tools import inheritors
from mpm.utils.text_parse import parse_value_key_table
from mpm.core.logging import getLogger
from mpm.core.exceptions import PermissionDeniedError
from mpm.core.types import Machine
import getpass
from rich.console import Console
from plumbum import FG, BG

from plumbum import CommandNotFound, ProcessExecutionError
from plumbum.commands.base import BoundCommand
from plumbum.path import RemotePath, LocalPath
from getpass import getpass

logger = getLogger(__name__)

class Shell:
    """Shell is wrapper for Plumbum Commands Machine

    To use:
    >>> sh = Shell()
    >>> sh.check_command("python")
    True
    >>> sh.cmd["python"]["-c"]("print(123)")
    '123\n'
    """

    @property
    def name(self) -> str:
        """ Name """
        return self.__class__.__name__.lower()

    def __init__(self, executor: Machine = LocalMachine()):
        self.logger = logger.getChild(self.__class__.__name__)
        self.exec = executor
        self.console = Console()

    def is_sudo(self) -> bool:
        """ Check is this shell session is sudo """
        self.logger.warning("is_sudo() not support by Shell!")
        return False

    def is_installed(self) -> bool:
        return True

    def which(self, command_name: str) -> Machine:
        return self.exec.which(command_name)

    def check_command(self, command_name):
        try:
            self.which(command_name)
            return True
        except CommandNotFound:
            return False

    @property
    def cmd(self) -> Machine:
        return self.exec

    def get_sudo(self) -> bool:
        """ Elevate the privileges of the current  shell session

        To use:
        >>> sh = Shell()
        >>> sh.is sudo()
        False
        >>> sh.get_sudo()
        True
        Returns:
            bool: is sudo
        """
        sudo = self.exec["sudo"]
        try:
            sudo["ls"]()
            return True
        except ProcessExecutionError as e:
            if ("no password" in e.stderr) or ("-S" in e.stderr):
                __pass = getpass("Sudo password: ")
                p = sudo["--stdin"]["ls"].popen(stdin=PIPE)
                out = p.communicate(f"{__pass}\n".encode(), timeout=2)
                return True
            else:
                self.console.print_exception()
        
        return self.is_sudo()

    @property
    def sudo_cmd(self) -> BoundCommand:
        sudo = self.exec["sudo"]
        return sudo[self.cmd]

class Bash(Shell):
    """Wrapper for Bash Shell """
    def is_installed(self) -> bool:
        """ Check if the Bash shell is installed """
        return self.check_command(self.name)

    def is_sudo(self) -> bool:
        command = 'if sudo -n true 2>/dev/null; then echo "1"; else echo "0"; fi;'
        return self.cmd(command)[0] == "1"

    @property
    def cmd(self) -> BoundCommand:
        return self.exec[self.name]["-c"]

    def call(self, command: List[str]) -> str:
        return self.cmd[" ".join(command)]()

    def sudo_call(self, command: List[str]) -> str:
        try:
            return self.sudo_cmd[" ".join(command)]()
        except Exception as error:
            self.get_sudo()
            return self.sudo_cmd[" ".join(command)]()

    @property
    def version(self) -> str:
        out = self.exec[self.name]("--version")
        result = re.search(r"\d.+\n", out).group(0)[:-1]
        return result

class ZSH(Bash):
    """Wrapper for ZSH Shell """
    pass

class Cmd(Shell):
    def is_installed(self) -> bool:
        return self.check_command(self.name)

    @property
    def cmd(self) -> BoundCommand:
        return self.exec[self.name]["/C"]

class PowerShell(Shell):
    def is_installed(self) -> bool:
        return self.check_command(self.name)

    @property
    def cmd(self) -> BoundCommand:
        return self.exec[self.name]["-Command"]
    
    @property
    def sudo_cmd(self) -> BoundCommand:
        return self.cmd['Start-Process powershell -Verb runAs -argumentlist "-Command '] # " 

    @property
    def version(self) -> str:
        out = self.cmd("Get-Host")
        data = parse_value_key_table(out, key_lower=True)
        return data["version"]

def get_installed_shells() -> List[Shell]:
    shells_list = []
    for cls in inheritors(Shell):
        obj = cls()
        if obj.is_installed():
            shells_list.append(cls)
    return shells_list


def AutoShell(name=None, *args, **kwargs) -> Shell:
    for cls in inheritors(Shell):
        obj = cls(*args, **kwargs)
        if name != None:
            if obj.name == name:
                return obj
        elif obj.is_installed():
            return obj
