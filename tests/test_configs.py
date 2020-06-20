from mpm.core.configs import CONFIGS_DIR, user_known_packages_file, user_settings_file
import pytest

def test_CONFIGS_DIR():
    assert CONFIGS_DIR.exists()
    assert user_known_packages_file.is_file()
    assert user_settings_file.is_file()