from shell import AutoShell, Bash, ZSH, PowerShell, Cmd, ShellAbstract, get_installed_shells

def test_bash_1():
    bash = Bash()
    assert bash.is_installed()
