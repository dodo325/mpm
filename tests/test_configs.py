from mpm.core.configs import (
    get_settings, CONFIGS_DIR, USER_DATA_DIR, USER_SCRIPTS_DIR,
    settings_file, user_settings_file, USER_CONFIGS_DIR, init_user_configs_dir,
    known_packages_file, get_known_packages, update_user_known_package, 
    get_remote_known_packages, get_packages_dependences_order)
import pytest

def test_CONFIGS_DIR():
    assert CONFIGS_DIR.exists()
    assert known_packages_file.is_file()
    assert settings_file.is_file()

def test_get_settings():
    settings = get_settings()
    assert "known_packages_url" in settings

def test_get_remote_known_packages():
    known_packages = get_remote_known_packages()
    assert "pytest" in known_packages


@pytest.mark.parametrize("offline", [True, False])
def test_get_known_packages(offline):
    known_packages = get_known_packages(offline=offline)
    assert "pytest" in known_packages
    assert user_settings_file.is_file()


def test_get_packages_dependences_order():
    known_packages = {
        "A": {
            "package_managers": {"apt": {}},
            "dependence": ["B", "C"]
        },
        "B": {
            "package_managers": {"apt": {}},
            "dependence": ["C"]
        },
        "C": {
            "package_managers": {"apt": {}}
        }
    }
    assert get_packages_dependences_order(known_packages, "A") == ["C", "B", "A"]
    assert get_packages_dependences_order(known_packages, "B") == ["C", "B"]
    assert get_packages_dependences_order(known_packages, "C") == ["C"]

# def test_get_packages_dependences_order_oh_my_zsh():
#     known_packages = get_known_packages(offline=True)
#     assert get_packages_dependences_order(
#         known_packages, "oh-my-zsh") == ["curl", "git", "zsh"]


def test_init_user_configs_dir():
    init_user_configs_dir()
    assert USER_DATA_DIR.is_dir()
    assert USER_SCRIPTS_DIR.is_dir()
    assert USER_CONFIGS_DIR.is_dir()
    assert user_settings_file.is_file()

@pytest.mark.parametrize("pretty", [True, False])
def test_update_user_known_package(pretty):
    init_user_configs_dir()
    assert USER_DATA_DIR.is_dir()
    config = {"package_managers": {"apt-get": {}, "apt": {}}}
    update_user_known_package("dbus", config, pretty=pretty)
    update_user_known_package("test", config, pretty=pretty)
    known_packages = get_known_packages()
    assert "dbus" in known_packages
    assert "test" in known_packages
    assert known_packages["dbus"] == config
    assert known_packages["test"] == config
