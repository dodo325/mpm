import subprocess
import platform
import logging
import re
from subprocess import check_output


class ShellAbstract():
    shell_path = None
    version = ""
    supported_platforms = []
    LOG_PERFIX = "shell."

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

    def __init__(self):
        self.logger = logging.getLogger(
            f'{self.LOG_PERFIX}{self.__class__.__name__}')

        if not self.is_installed():
            self.logger.error(f"Not Found {self.__class__.__name__}!!")

    def cell(self, command: list, shell=False, *args, **kwargs):
        if self.shell_path is None:
            return check_output(command, shell=shell).decode("utf-8")
        else:
            return check_output(command, shell=shell, executable=self.shell_path).decode("utf-8")


class Bash(ShellAbstract):
    shell_path = '/bin/bash'
    supported_platforms = {
        'Linux': {}
    }

    def is_installed(self) -> bool:
        if self.is_platform_supported():
            try:
                out = self.cell(["bash", "--version"])
                result = re.search(r'\d.+\n', out).group(0)[:-1]
                self.version = result
                return True
            except FileNotFoundError:
                pass
        return False

    def compgen(
            self,
            perfix: str = None,

    ) -> list:
        command = 'compgen -abcdefgjksuv'
        out = self.cell(command, shell=True).splitlines()
        if perfix != None:
            out = list(filter(lambda c: c.startswith(perfix), out))
        return out

    def alias_list(self, perfix: str = None) -> list: #TODO: load user profile!
        out = self.cell('alias', shell=True).splitlines()
        if perfix != None:
            out = list(filter(lambda c: c.startswith(perfix), out))
        return out

    def check_command(self, command):
        return command in self.compgen()


class ZSH(Bash):
    supported_platforms = {
        'Linux': {}
    }

    def is_installed(self) -> bool:
        if self.is_platform_supported():
            try:
                out = self.cell(["zsh", "--version"])
                result = re.search(r'\d.+\n', out).group(0)[:-1]
                self.version = result
                return True
            except FileNotFoundError:
                pass
        return False


class Cmd(ShellAbstract):
    supported_platforms = {
        'Windows': {}
    }


class PowerShell(Cmd):
    supported_platforms = {
        'Windows': {
            'releases_perfix': [
                '10'
            ]
        }
    }

    def cell(self, command: list, *args, **kwargs):
        command.insert(0, "powershell.exe")
        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate()[0].decode("utf-8")

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


def AutoShell(*args, **kwargs) -> ShellAbstract:
    for cls in ShellAbstract._inheritors():
        obj = cls(*args, **kwargs)
        if obj.is_installed():
            return obj
