import pytest
from mpm.pm.package_managers import Pip, BashAliasManager
from mpm.shell import ZSH

def test_bash_1(fake_process, fake_bash_shell):
    sh = fake_bash_shell(fake_process)
    assert sh.name == "bash"
    assert sh.is_installed()
    assert sh.check_command("apt")


def test_pip_is_installed(fake_process, fake_bash_shell):
    sh = fake_bash_shell(fake_process)
    pip = Pip(shell=sh)
    assert sh.check_command("pip")
    assert pip.is_installed()


def test_pip_get_all_packages(fake_process, fake_bash_shell):
    sh = fake_bash_shell(
        fake_process, extend_list=[(["pip", "freeze"], "pip_freeze.txt"),]
    )
    pip = Pip(shell=sh)
    assert sh.check_command("pip")
    assert pip.is_installed()
    all_packages = pip.get_all_packages()
    assert len(all_packages) == 284


def test_pip_search(fake_process, fake_bash_shell):
    sh = fake_bash_shell(
        fake_process,
        extend_list=[
            (["pip", "freeze"], "pip_freeze.txt"),
            (["pip", "search", "mpm"], "pip_search_mpm.txt"),
            (["pip", "search", "numpy"], "pip_search_numpy.txt"),
        ],
    )
    pip = Pip(shell=sh)

    assert pip.search("mpm") == {
        "mpm": {"version": "0.1.0", "description": "package (skill) manager for Misty"},
        "pyMPM": {
            "version": "0.1.0",
            "description": "Python version of the MPM millimeter wave propagation model",
        },
    }
    data = pip.search("numpy")
    assert data["numpy"] == {
        "description": "NumPy is the fundamental package for array computing with Python.",
        "installed": "1.18.1",
        "latest": "1.18.5",
        "version": "1.18.5",
    }
    assert data["numpy-indexed"] == {
        "version": "0.3.5",
        "description": "This package contains functionality for indexed operations on numpy ndarrays, providing efficient vectorized functionality such as grouping and set operations.",
    }

def test_BashAliasManager(fake_process, fake_bash_shell):
    sh = fake_bash_shell(fake_process)
    fake_process.register_subprocess(sh.get_full_command(
        ["echo $HOME/.bashrc"]), stdout="/home/user/.bashrc")
    fake_process.register_subprocess(sh.get_full_command(["echo $HOME/.zshrc"]), stdout="/home/user/.zshrc")
    shell = ZSH()
    pm = BashAliasManager(shell=shell)
    assert pm.shell.name == "bash"

def test_BashAliasManager_is_installed(fake_process, fake_bash_shell):
    sh = fake_bash_shell(fake_process)
    fake_process.register_subprocess(sh.get_full_command(
        ["echo $HOME/.bashrc"]), stdout="/home/user/.bashrc")
    fake_process.register_subprocess(sh.get_full_command(
        ["echo $HOME/.zshrc"]), stdout="/home/user/.zshrc")
    pm = BashAliasManager(shell=sh)
    assert pm.shell.name == "bash"
    assert pm.is_installed()
