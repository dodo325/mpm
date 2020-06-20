from mpm.core.configs import get_settings, CONFIGS_DIR, settings_file, known_packages_file
import pytest

def test_CONFIGS_DIR():
    assert CONFIGS_DIR.exists()
    assert known_packages_file.is_file()
    assert settings_file.is_file()

def test_get_settings():
    settings = get_settings()
    assert "known_packages_url" in settings
