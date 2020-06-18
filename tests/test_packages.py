import pytest
from mpm.pm.packages import PipPackage

def test_pip_pkg_is_installed(fake_process, fake_bash_shell):
    sh = fake_bash_shell(fake_process, extend_list=[
        (["pip", "freeze"], "pip_freeze.txt"),
    ])
    pkg = PipPackage("numpy", shell=sh)
    assert pkg.is_installed()
    assert pkg.is_pm_installed()

def test_pip_info(fake_process, fake_bash_shell):
    sh = fake_bash_shell(fake_process, extend_list=[
        (["pip", "freeze"], "pip_freeze.txt"),
        (["pip", "search", "numpy"], "pip_search_numpy.txt"),
        (["pip", "show", "numpy", "-v"], "pip_show_numpy.txt"),
    ])
    pkg = PipPackage("numpy", shell=sh)
    assert pkg.info["installed"] == "1.18.1"
    assert pkg.info["author"] == "Travis E. Oliphant et al."
    assert pkg.info["summary"] == "NumPy is the fundamental package for array computing with Python."
