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

def add_cmd_from_file(cmd, file_name: str):
    path = Path(__file__).parent / "callss_output" / file_name
    with path.open() as f:
            out = f.read()

@pytest.fixture
def fake_bash_shell(request):
    pass
