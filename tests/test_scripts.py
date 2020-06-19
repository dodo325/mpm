import sys
import mpm
from mpm.scripts.bash import BashScriptFile
import pytest
from pathlib import Path
from mpm.utils.text_parse import not_nan_split

# def read_local_script(name:


def test_bash_init():
    f = Path("scripts/bash/which_term.sh")
    assert f.is_file()

    script = BashScriptFile(str(f))
    li = script.get_lines()
    assert len(li) == 25
    assert li[1] == "    term=$(ps -p $(ps -p $$ -o ppid=) -o args=);"


@pytest.fixture(scope="function")
def tmp_bash_script(tmp_path):
    CONTENT = """killport() { sudo lsof -t -i tcp:\"$1\" | xargs kill -9 ; }
alias sshi="ssh -o 'IdentitiesOnly=yes'"
"""
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.sh"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert type(p) in Path.__subclasses__()
    return p


def test_open_bash_script(tmp_bash_script):
    f = tmp_bash_script
    assert f.is_file()
    script = BashScriptFile(str(f))
    assert script.get_alias() == {"sshi": "ssh -o 'IdentitiesOnly=yes'"}
    assert len(script.get_lines()) == 2


def test_add_data_in_bash_script(tmp_bash_script):
    f = tmp_bash_script
    assert f.is_file()
    script = BashScriptFile(str(f))
    script.add_data_in_file("alias myip='curl ipinfo.io/ip'")
    script.update()
    assert len(script.get_lines()) == 3  # TODO: auto update
    with f.open("r") as ff:
        for i, l in enumerate(ff):
            pass
        assert i + 1 == 3


def test_add_data_in_bash_script(tmp_bash_script):
    f = tmp_bash_script
    assert f.is_file()
    script = BashScriptFile(str(f))
    script.add_alias("myip", "curl ipinfo.io/ip")
    script.update()
    assert script.get_alias() == {
        "myip": "curl ipinfo.io/ip",
        "sshi": "ssh -o 'IdentitiesOnly=yes'",
    }


def test_filter_comments_in_bash_script(tmp_bash_script):
    script = BashScriptFile(str(tmp_bash_script))
    script.add_data_in_file("#alias myip='curl ipinfo.io/ip'")
    script.add_data_in_file(" # 12321")
    script.add_data_in_file("  #asdad1")
    script.update()
    li = not_nan_split(script.content)
    print(f"content = {script.content}")
    assert len(li) == 5
    li_f = script._filter_comments(li)
    assert len(li_f) == 2
