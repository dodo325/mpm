import sys
import mpm
from mpm.shell.shells import (
    AutoShell,
    Bash,
    ZSH,
    PowerShell,
    Cmd,
    AbstractShell,
    get_installed_shells,
)
import platform
import subprocess
import pytest
from pathlib import Path

def test_AutoShell_init():
    sh = AutoShell()
    assert sh.is_installed()

def test_AbstractShell_inheritors():
    inheritors_list = AbstractShell._inheritors()
    inheritors_correct = [
        Bash,
        Cmd,
        PowerShell,
        ZSH,
    ]
    assert set(inheritors_list) == set(inheritors_correct), "Не все оболочки найдены"
    assert inheritors_list == inheritors_correct, "Порядок не верен!"

class TestBash:
    sh: Bash = None

    def read_calls_file(self, name: str) -> str:
        path = Path(__file__).parent / "callss_output" / name
        with path.open() as f:
            out = f.read()
        return out

    def setup_class(self):
        print("*** setup_class ***")

    def teardown_class(self):
        print(" === teardown_class ===")

    def setup(self):
        self.sh = Bash()
        print("** setup **")

    def teardown(self):
        print(" == teardown ==")

    @pytest.mark.xfail(platform.system() != "Linux", reason="Bash обычно работает только на Linux")
    def test_installed(self):
        assert self.sh.is_installed()
    
    def test_get_full_command(self):
        assert self.sh.get_full_command(
            ["bash", "--version"]) == ['/bin/bash', '-c', 'bash --version']
        assert self.sh.get_full_command(
            "apt") == ['/bin/bash', '-c', 'apt']

        assert self.sh.get_full_command("apt", executable_path=None) == ["apt"]

    def test_fake_installed(self, fake_process):
        out = self.read_calls_file("bash_version.txt")
        
        command = self.sh.get_full_command(["bash", "--version"])
        print(f"command = {command}")
        fake_process.register_subprocess(
            command, stdout=out.splitlines()
        )
        fake_process.register_subprocess(
            ["bash", "--version"], stdout=out.splitlines()
        )
        print("\n**", self.sh.call(["bash", "--version"], executable_path = None))
        assert self.sh.is_installed()
        assert self.sh.version == '5.0.16(1)-release (x86_64-pc-linux-gnu)'

    def test_fake_whereis(self, fake_process):
        fake_process.register_subprocess(
            self.sh.get_full_command(["whereis", "apt"]), stdout="apt: /usr/bin/apt /usr/lib/apt /etc/apt /usr/share/man/man8/apt.8.gz"
        )
        fake_process.register_subprocess(
            self.sh.get_full_command(["whereis", "code"]), stdout="code: /usr/share/code /snap/bin/code /snap/bin/code.url-handler"
        )
        assert self.sh.whereis("apt") == [
            '/usr/bin/apt', '/usr/lib/apt', '/etc/apt', '/usr/share/man/man8/apt.8.gz']
        assert self.sh.whereis("code") == ['/usr/share/code',
                                          '/snap/bin/code', '/snap/bin/code.url-handler']

        out = self.read_calls_file("zsh_whereis_python.txt")
        fake_process.register_subprocess(
            self.sh.get_full_command(["whereis", "python"]), stdout=out.splitlines())
        assert self.sh.whereis("python") == [
            '/usr/bin/python3.8', 
            '/usr/bin/python3.7m', 
            '/usr/bin/python3.8-config', 
            '/usr/bin/python2.7', 
            '/usr/bin/python3.7', 
            '/usr/lib/python3.8', 
            '/usr/lib/python3.7', 
            '/usr/lib/python2.7', 
            '/etc/python3.7', 
            '/etc/python2.7', 
            '/etc/python3.8', 
            '/usr/local/lib/python3.8', 
            '/usr/local/lib/python2.7', 
            '/usr/local/lib/python3.7', 
            '/usr/include/python3.8', 
            '/usr/share/python', 
            '/home/user/anaconda3/bin/python3.7-config', 
            '/home/user/anaconda3/bin/python3.7', 
            '/home/user/anaconda3/bin/python3.7m', 
            '/home/user/anaconda3/bin/python', 
            '/home/user/anaconda3/bin/python3.7m-config'
        ]

    def test_fake_compgen(self, fake_process):
        out = self.read_calls_file("bash_compgen.txt")

        command = self.sh.get_full_command("compgen -abcdefgjksuv")
        print(f"command = {command}")
        fake_process.register_subprocess(
            command, stdout=out.splitlines()
        )
        assert type(self.sh.compgen()) == list
        print(self.sh.compgen("python"))
        assert self.sh.compgen("python") == [
            'python2.7', 'python2', 
            'python3', 'python3.7-config', 
            'python3-config',
            'python3.7', 'python3.8', 
            'python', 'python3.7m-config', 
            'python3.7m', 'python3.8-config'
            ]
        assert set(self.sh.compgen("code")) == set([
            'codepage', 'code', 'code.url-handler'
            ])

    @pytest.mark.parametrize("cmd", [
            "python", "apt", "apt-get", "set", "bash", "nano", "sudo"
        ])
    def test_check_command(self, fake_process, cmd):
        out = self.read_calls_file("bash_compgen.txt")
        command = self.sh.get_full_command("compgen -abcdefgjksuv")
        fake_process.register_subprocess(
            command, stdout=out.splitlines()
        )
        assert self.sh.check_command(cmd)

    def test_fake_get_env(self, fake_process):
        out = self.read_calls_file("bash_set.txt")

        command = self.sh.get_full_command(["set"])
        print(f"command = {command}")
        fake_process.register_subprocess(
            command, stdout=out.splitlines()
        )
        env = self.sh.get_env()
        assert env["BASH"] == '/bin/bash'
        assert env["USERNAME"] == 'user'
        assert env["USER"] == 'user'
        assert env["HOME"] == '/home/user'

    def test_get_home(self):
        assert self.sh.get_home() == str(Path.home())

    def test_pwd(self):
        assert self.sh.pwd() == str(Path.cwd())

    def test_name(self):
        assert self.sh.name == "bash"
