import subprocess
import platform
import logging
import re
from subprocess import check_output, Popen, PIPE
from typing import List, Tuple
from getpass import getpass

_LOG_PERFIX = "shell."


class AbstractShell:
    executable_path = ""
    executable_args = []
    version = ""
    supported_platforms = []

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

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

    def is_platform_supported(self) -> bool:
        if platform.system() in self.supported_platforms:
            platform_conig = self.supported_platforms[platform.system()]

            for release_perfix in platform_conig.get("releases_perfix", []):
                if platform.release().startswith(release_perfix):
                    return True

            if platform_conig == dict():
                return True

        return False

    def is_installed(self) -> bool:
        return self.is_platform_supported()

    def check_command(self, command) -> bool:
        return None  # can't check!

    def __init__(self):
        self.logger = logging.getLogger(f"{_LOG_PERFIX}{self.name}")

    #         if not self.is_installed():
    #             self.logger.warn(f"Not Found {self.name}!!")

    # executable_path - это добавка к команде!!!
    def is_sudo_mode(self):
        return

    def sudo_cell(self, command: list, enter_password=False, *args, **kwargs):
        raise NoneType()

    def cell(
        self,
        command: list,
        shell=False,
        executable_path="",
        executable_args=[],
        *args,
        **kwargs,
    ) -> str:
        out_command = command

        if executable_path == "":
            executable_path = self.executable_path

        if executable_args == []:
            executable_args = self.executable_args

        if executable_path != "" and executable_path != None:
            if type(command) == list:
                command = " ".join(command)
            out_command = [executable_path]
            out_command.extend(executable_args)
            out_command.append(command)

        self.logger.info(f"Try call command: {out_command}")
        return check_output(out_command, shell=shell, **kwargs).decode("utf-8")


class Bash(AbstractShell):
    executable_path = "/bin/bash"
    executable_args = ["-c"]

    supported_platforms = {"Linux": {}}
    __sudo_password = None

    def sudo_cell(
        self,
        command: list,
        shell=False,
        executable_path="",
        executable_args=[],
        enter_password=False,
        *args,
        **kwargs,
    ) -> str:
        if self.is_sudo_mode():
            return self.cell(command, *args, **kwargs)

        if executable_path == "":
            executable_path = self.executable_path

        if executable_args == []:
            executable_args = self.executable_args

        out_command = ["sudo", "--stdin"]

        if executable_path != "" and executable_path != None:
            if type(command) == list:
                command = " ".join(command)
            out_command.append(executable_path)
            out_command.extend(executable_args)
            out_command.append(command)

        self.logger.info(f"Try call command: {out_command}")
        if enter_password:
            if not self.__sudo_password:
                self.__sudo_password = getpass("Sudo password: ")
            p = Popen(
                out_command,
                stdin=PIPE,
                stderr=PIPE,
                universal_newlines=True,
                shell=shell,
            )
            return p.communicate(self.__sudo_password + "\n")[1]
        return check_output(out_command, shell=shell, **kwargs).decode("utf-8")

    def whereis(self, command: str):
        out = self.cell(["whereis", command])
        out = out.replace("\n", "")
        return out.split(" ")[1:]

    def is_installed(self) -> bool:
        if self.is_platform_supported():
            try:
                out = self.cell(["bash", "--version"])
                result = re.search(r"\d.+\n", out).group(0)[:-1]
                self.version = result
                return True
            except FileNotFoundError:
                pass
        return False

    def compgen(self, perfix: str = None,) -> list:
        command = "compgen -abcdefgjksuv"
        out = self.cell(command, shell=False).splitlines()
        if perfix != None:
            out = list(filter(lambda c: c.startswith(perfix), out))
        return out

    def alias_list(self, perfix: str = None) -> list:  # TODO: load user profile!
        out = self.cell("alias", shell=True).splitlines()
        if perfix != None:
            out = list(filter(lambda c: c.startswith(perfix), out))
        return out

    def check_command(self, command):
        return command in self.compgen()


class ZSH(Bash):
    supported_platforms = {"Linux": {}}

    def is_installed(self) -> bool:
        if self.is_platform_supported():
            try:
                out = self.cell(["zsh", "--version"])
                result = re.search(r"\d.+\n", out).group(0)[:-1]
                self.version = result
                return True
            except FileNotFoundError:
                pass
        return False


class Cmd(AbstractShell):
    executable_path = "cmd.exe"
    executable_args = ["-c"]
    supported_platforms = {"Windows": {}}


class PowerShell(Cmd):
    executable_path = "powershell.exe"
    supported_platforms = {"Windows": {"releases_perfix": ["10"]}}

    def is_installed(self) -> bool:
        if self.is_platform_supported():
            try:
                out = self.cell(["Get-Host"])
                out_lines = out.split("\n")
                for line in out_lines:
                    if "Version" in line:
                        line = line.replace(" ", "")
                        line = line.replace("Version", "")
                        line = line.replace(":", "")
                        line = line.replace("\r", "")
                        self.version = line
                        return True
            except FileNotFoundError:
                pass
        return False


def get_installed_shells() -> List[AbstractShell]:
    shells_list = []
    for cls in AbstractShell._inheritors():
        obj = cls()
        if obj.is_installed():
            shells_list.append(cls)
    return shells_list


def AutoShell(name=None, *args, **kwargs) -> AbstractShell:
    for cls in AbstractShell._inheritors():
        obj = cls(*args, **kwargs)
        if name != None:
            if obj.name == name:
                return obj
        elif obj.is_installed():
            return obj


def main():
    shell = AutoShell()
    print(f"is sudo: {shell.is_sudo_mode()}")


if __name__ == "__main__":
    main()
