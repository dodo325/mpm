# https://click.palletsprojects.com/en/7.x/testing/
from click.testing import CliRunner
from mpm.core.cli import info, main
import pytest
# @pytest.mark("cli")

def test_info():
    runner = CliRunner()
    result = runner.invoke(info, ['pytest'])
    assert result.exit_code == 0
    # assert result.output == 'Hello Peter!\n'

def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    print(result.output)