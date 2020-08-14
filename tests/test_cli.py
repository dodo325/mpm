# https://click.palletsprojects.com/en/7.x/testing/
from click.testing import CliRunner
from mpm.core.cli import info, main, search, version, install
import pytest
import mpm
import mpm.__main__
# @pytest.mark("cli")


@pytest.mark.cli
def test_info_pass():
    runner = CliRunner()
    result = runner.invoke(info, ["pytest"])
    assert result.exit_code == 0
    # assert result.output == 'Hello Peter!\n'

@pytest.mark.cli
def test_install_pass():
    runner = CliRunner()
    result = runner.invoke(install, ["pytest"])
    assert result.exit_code == 0

@pytest.mark.cli
def test_search_pass():
    runner = CliRunner()
    result = runner.invoke(search, ["pytest"])
    assert result.exit_code == 0
    # assert result.output == 'Hello Peter!\n'

# # @pytest.mark.skip()

def test__main__doc():
    assert mpm.__main__.__doc__ != None

def test__main__cli():
    assert mpm.__main__.main == main

def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    print(result.output)

def test_version():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    print(result.output)

def test_getAbout():
    info = mpm.getAbout()
    assert "Version" in info
