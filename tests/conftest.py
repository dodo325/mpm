import pytest
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
from typing import List, Tuple

# @pytest.fixture(scope="session", autouse=True)
# def auto_session_resource(request):
#     """ Auto session resource fixture
#     """
#     print("auto_session_resource_setup")

#     def auto_session_resource_teardown():
#         print("auto_session_resource_teardown")
#     request.addfinalizer(auto_session_resource_teardown)

# @pytest.fixture(scope="session")
# def manually_session_resource(request):
#     """ Manual set session resource fixture
#     """
#     print("manually_session_resource_setup")

#     def manually_session_resource_teardown():
#         print("manually_session_resource_teardown")
#     request.addfinalizer(manually_session_resource_teardown)

# @pytest.fixture(scope="function")
# def function_resource(request):
#     """ Function resource fixture
#     """
#     print("function_resource_setup")

#     def function_resource_teardown():
#         print("function_resource_teardown")
    # request.addfinalizer(function_resource_teardown)

def add_cmd_from_file(fake_process, command: list, file_name: str) -> "fake_process":
    path = Path(__file__).parent / "callss_output" / file_name
    with path.open() as f:
        out = f.read()
    # print(f"command = {command}, out = {out}")
    fake_process.register_subprocess(
        command, stdout=out.splitlines()
    )
    return fake_process


@pytest.fixture
def fake_bash_shell(request):
    def get_shell(
            fake_process, 
            command_list: List[Tuple["cmd", "output_file"]] = [
                (["bash", "--version"], "bash_version.txt"),
                (["compgen", "-abcdefgjksuv"], "bash_compgen.txt")],
            extend_list: List[Tuple["cmd", "output_file"]] = []
            ) -> AbstractShell:
        sh = Bash()
        command_list.extend(extend_list)
        for cmd, file_name in command_list:
            fake_process = add_cmd_from_file(
                fake_process,
                sh.get_full_command(cmd),
                file_name)
            fake_process = add_cmd_from_file(
                fake_process,
                cmd,
                file_name)
        return sh
    return get_shell
