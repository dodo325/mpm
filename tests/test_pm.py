import pytest
import sys
import subprocess


def inc(x):
    return x + 1


@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 11])
def test_cross_params(x, y):
    print("x: {0}, y: {1}".format(x, y))
    assert True


@pytest.mark.xfail(sys.platform != "win64", reason="requires windows 64bit")
def test_failed_for_not_win32_systems():
    assert False


@pytest.mark.skipif(sys.platform != "win64", reason="requires windows 64bit")
def test_skipped_for_not_win64_systems2():
    assert False


# def test_answer(function_resource):
#     assert inc(4) == 5


@pytest.fixture()
def resource_setup(request):
    print("resource_setup")

    def resource_teardown():
        print("resource_teardown")

    request.addfinalizer(resource_teardown)


def test_1_that_needs_resource(resource_setup):
    print("test_1_that_needs_resource")


def test_git(fake_process):
    fake_process.register_subprocess(
        ["git", "branch"], stdout=["* fake_branch", "  master"]
    )

    process = subprocess.Popen(
        ["git", "branch"], stdout=subprocess.PIPE, universal_newlines=True,
    )
    out, _ = process.communicate()

    assert process.returncode == 0
    assert out == "* fake_branch\n  master\n"
