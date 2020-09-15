from plumbum.machines import LocalMachine, SshMachine
from plumbum.machines.paramiko_machine import ParamikoMachine
from plumbum import FG, BG
from typing import List, Any, Union
from subprocess import check_output, Popen, PIPE, STDOUT
import re
from mpm.utils.tools import inheritors
from mpm.core.logging import getLogger
from mpm.core.exceptions import PermissionDeniedError
import getpass
from rich.console import Console

from plumbum import CommandNotFound, ProcessExecutionError
from plumbum.commands.base import BoundCommand

from getpass import getpass

logger = getLogger(__name__)

class Shell:
    # Это терминальная оболочка самой системы

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __init__(self, executor: Union[LocalMachine, SshMachine, ParamikoMachine] = LocalMachine()):
        self.logger = logger.getChild(self.__class__.__name__)
        self.exec = executor
        self.console = Console()

    def is_sudo(self) -> bool:
        self.logger.warning("is_sudo() not support by Shell!")
        return False

    def is_installed(self) -> bool:
        return True

    def which(self, command_name):
        return self.exec.which(command_name)

    def check_command(self, command_name):
        try:
            self.which(command_name)
            return True
        except CommandNotFound:
            return False

    @property
    def cmd(self):
        return self.exec

    def get_sudo(self) -> bool:
        try:
            sudo = self.exec["sudo"]["--stdin"]
            sudo["ls"]()
        except ProcessExecutionError as e:
            if "no password" in e.stderr:
                __pass = getpass("Sudo password: ")
                p = sudo["ls"].popen(stdin=PIPE)
                out = p.communicate(f"{__pass}\n".encode(), timeout=2)
                self.logger.info(out)
            else:
                self.console.print_exception()
        
        return self.is_sudo()

    @property
    def sudo_cmd(self) -> BoundCommand:
        sudo = self.exec["sudo"]
        return sudo[self.cmd]

class Bash(Shell):
    def is_installed(self) -> bool:
        return self.check_command(self.name)

    def is_sudo(self) -> bool:
        command = 'if sudo -n true 2>/dev/null; then echo "1"; else echo "0"; fi;'
        return self.cmd(command)[0] == "1"

    @property
    def cmd(self) -> BoundCommand:
        return self.exec[self.name]["-c"]

    @property
    def version(self) -> str:
        out = self.exec[self.name]("--version")
        result = re.search(r"\d.+\n", out).group(0)[:-1]
        return result

class ZSH(Bash):
    pass


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
