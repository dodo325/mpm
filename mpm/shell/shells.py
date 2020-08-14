import subprocess
import platform
import re
from subprocess import check_output, Popen, PIPE, STDOUT
from typing import List, Tuple
from getpass import getpass
from pathlib import Path

from mpm.core.logging import getLogger
from mpm.utils.text_parse import not_nan_split, parse_value_key_table
from mpm.core.exceptions import CommandNotFound, ShellError

logger = getLogger(__name__)


class AbstractShell:
    """
    Абстрактный Класс для работы с коммандными строками  
    """

    executable_path = ""
    executable_args = []
    version = ""
    supported_platforms = []

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    @classmethod
    def _inheritors(cls) -> list:
        """
        return all subclasses
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

    def get_home(self) -> str:
        """
        Pls use Path.home()
        """
        return str(Path.home())

    def pwd(self) -> str:
        """
        Pls use Path.cwd()
        """
        return str(Path.cwd())

    def get_env(self) -> dict:
        """
        Environment variables
        """
        out = self.call("set")
        data = parse_value_key_table(out, delimiter="=")
        return data

    def _call_filter(self, output: str) -> str:
        output = output.rstrip("\n")
        return output

    def echo(self, cmd: str):
        return self.call(["echo", cmd])

    def is_platform_supported(self) -> bool:
        if platform.system() in self.supported_platforms:
            platform_conig = self.supported_platforms[platform.system()]

            for release_perfix in platform_conig.get("releases_perfix", []):
                if platform.release().startswith(release_perfix):
                    return True

            if platform_conig == dict():
                return True

        return False

    def whereis(cmd: str) -> list:
        """
        Находит где исполняемый файл команды
        """
        raise NotImplementedError()

    def is_installed(self) -> bool:
        """
        Оределяет установленна данная коммандная оболочка и обновляет self.version
        """
        return self.is_platform_supported()

    def check_command(self, command) -> bool:
        return None  # can't check!

    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)

    #         if not self.is_installed():
    #             self.logger.warning(f"Not Found {self.name}!!")

    def is_sudo_mode(self) -> bool:

        return False

    def sudo_call(self, command: list, enter_password=False, *args, **kwargs) -> str:
        raise NotImplementedError()

    def get_full_command(
        self, command: list, executable_path="", executable_args=[]
    ) -> list:
        """
        return full command for this Shell
        Ex:
        >>> sh = Bash()
        >>> sh.get_full_command(["bash", "--version"])
        ['/bin/bash', '-c', 'bash --version']
        """
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
        if type(out_command) == str:
            out_command = [out_command]
        return out_command

    def call(
        self,
        command: list,
        shell=False,
        executable_path="",
        executable_args=[],
        stderr=STDOUT,
        debug=False,
        *args,
        **kwargs,
    ) -> str:
        self.logger.debug(
            f"Args:\n\traw command = {command}\n\tshell = {shell}\n\t\
executable_path = {executable_path}\n\texecutable_args={executable_args}\n\t\
stderr = {stderr}\n\targs = {args}\n\tkwargs = {kwargs}"
        )
        out_command = self.get_full_command(
            command, executable_path=executable_path, executable_args=executable_args
        )
        self.logger.debug(f"Try call command: {out_command}")
        out = check_output(
            out_command, 
            shell=shell, 
            # universal_newlines=True,  #TODO: better make: .decode("utf8")
            stderr=stderr,
            **kwargs)
        out_str = out.decode("utf8")
        if debug:
            self.logger.debug(f"Output: {out_str}")
        if out_str.startswith("get-command"):
            raise CommandNotFound(f"Command not found: {command}")
        return self._call_filter(out_str)


class Bash(AbstractShell):
    executable_path = "/bin/bash"
    executable_args = ["-c"]

    supported_platforms = {"Linux": {}}
    __sudo_password = None

    def sudo_call(
        self,
        command: list,
        shell=False,
        executable_path="",  # если надо, чтобы команда вообще не использовала это, то сделай executable_path=None
        executable_args=[],
        enter_password=False,
        stdin=PIPE,
        stderr=STDOUT,
        debug=False,
        *args,
        **kwargs,
    ) -> str:
        self.logger.debug(
            f"Args:\n\traw command = {command}\n\tshell = {shell}\n\t\
executable_path = {executable_path}\n\texecutable_args={executable_args}\n\t\
stderr = {stderr}\n\targs = {args}\n\tkwargs = {kwargs}"
        )

        if self.is_sudo_mode():
            return self.call(command, *args, **kwargs)

        out_command = ["sudo", "--stdin"]
        out_command.append(
            self.get_full_command(
                command,
                executable_path=executable_path,
                executable_args=executable_args,
            )
        )

        self.logger.debug(f"Try call command: {out_command}")
        out = None
        if enter_password:
            if not self.__sudo_password:
                self.logger.debug(f"Try get pass")
                self.__sudo_password = getpass("Sudo password: ")
            p = Popen(
                out_command,
                stdin=stdin,
                stderr=stderr,
                universal_newlines=True,
                shell=shell,
            )
            out = p.communicate(self.__sudo_password + "\n")[1]
        else:
            out = check_output(
                out_command, universal_newlines=True, stdin=stdin, stderr=stderr, shell=shell, **kwargs
            )
        if debug:
            self.logger.debug(f"Output: {out}")
        return self._call_filter(out)

    def get_env(self) -> dict:
        out = self.call("set")
        data = parse_value_key_table(out, delimiter="=")
        data["PATH"] = data["PATH"].split(":")
        return data

    def whereis(self, command: str) -> list:
        try:
            out = self.call(["whereis", command])

            return out.split(" ")[1:]
        except Exception as e:
            self.logger.error(f"Not found {command}!", exc_info=True)
            return []

    def is_installed(self) -> bool:
        if self.is_platform_supported():
            try:
                out = self.call(["bash", "--version"])
                result = re.search(r"\d.+\n", out).group(0)[:-1]
                self.version = result
                self.logger.info(f"installed! ver: {result}")
                return True
            except FileNotFoundError:
                pass
        return False

    __compgen_out = None
    def compgen(
        self, 
        perfix: str = None, 
        only_commands: bool = False, 
        no_cashe: bool = False,
        exact_match: bool = False
        ) -> list:
        """
        compgen is bash built-in Unix command and it will show all available commands, aliases, and functions for you!

        only_commands - run 'compgen -c'

        Using:
        >>> sh = Bash()
        >>> cmd_list = sh.compgen()
        >>> len(cmd_list)
        6315
        >>> li = sh.compgen(only_commands=True, no_cashe=True)
        >>> len(li)
        5509
        >>> li[:5]
        ['if', 'then', 'else', 'elif', 'fi']
        """
        command = "compgen -abcdefgjksuv"
        if only_commands:
            command = "compgen -c"
        li = self.__compgen_out
        if not li or no_cashe:
            out = self.call(command, shell=False)
            out = out.replace("\n", " ")
            li = not_nan_split(out, delimiter=" ")

            if not no_cashe:
                self.__compgen_out = li
        if perfix != None:
            if exact_match:
                try:
                    li.index(perfix)
                    return [perfix]
                except ValueError:
                    return []
            else:
                li = list(filter(lambda c: c.startswith(perfix), li))
        return li

    def alias_list(self, perfix: str = None) -> list:  # TODO: load user profile!
        out = self.call("alias", shell=True).splitlines()
        if perfix != None:
            out = list(filter(lambda c: c.startswith(perfix), out))
        return out

    def check_command(self, command: str, only_commands: bool = True) -> bool:
        return command in self.compgen(only_commands=only_commands)


class ZSH(Bash):
    supported_platforms = {"Linux": {}}
    executable_path = "/bin/zsh"
    executable_args = ["-c"]

    def is_installed(self) -> bool:
        if self.is_platform_supported():
            try:
                out = self.call(["zsh", "--version"])
                out = out.replace("\n", "")
                self.version = out
                self.logger.info(f"installed! ver: {out}")
                return True
            except FileNotFoundError:
                pass
        return False


class Cmd(AbstractShell):
    executable_path = "cmd.exe"
    executable_args = ["/C"]
    supported_platforms = {"Windows": {}}
    # def call # TODO: don't WORK on Windows!!!!!!!!
    def get_all_exe(self) -> list:
        return self.whereis("*.exe")

    def whereis(self, command: str) -> list:
        try:
            out = self.call(["where", command])
            li = not_nan_split(out)
            return li
        except Exception as e:
            self.logger.error(f"Not found {command}!", exc_info=True)
            return []

    def check_command(self, command: str) -> bool:
        return self.whereis(command) != []


class PowerShell(Cmd):
    executable_path = "powershell.exe"
    executable_args = ["-Command"]
    supported_platforms = {"Windows": {"releases_perfix": ["10"]}}

    def whereis(self, command: str) -> list:
        try:
            out = self.call([f"(get-command {command}).Path"])
            li = not_nan_split(out)
            return li
        except Exception as e:
            self.logger.error(f"Not found {command}!", exc_info=True)
            return []

    def is_installed(self) -> bool:
        """
        Check is powershell installed and update powershell.version
        """
        if self.is_platform_supported():
            try:
                out = self.call(["Get-Host"])
                data = parse_value_key_table(out, key_lower=True)
                if "version" in data:
                    self.version = data["version"]
                    return True
            except FileNotFoundError:
                pass
        return False


def get_installed_shells() -> List[AbstractShell]:
    """
    Return all installed shells
    """
    shells_list = []
    for cls in AbstractShell._inheritors():
        obj = cls()
        if obj.is_installed():
            shells_list.append(cls)
    return shells_list


def AutoShell(name=None, *args, **kwargs) -> AbstractShell:
    """
    Returns one of the installed shells

    Or by 'name'
    """
    for cls in AbstractShell._inheritors():
        obj = cls(*args, **kwargs)
        if name != None:
            if obj.name == name:
                return obj
        elif obj.is_installed():
            return obj
