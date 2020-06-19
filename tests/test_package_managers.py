import pytest
from mpm.pm.package_managers import Pip


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
