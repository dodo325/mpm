__version__ = '0.1'

from mpm.core.exceptions import PackageDoesNotExist
from mpm.core.logging import logging
from pathlib import Path
from mpm import __file__ as mpm__file__

USER_DATA_DIR = Path.home() / ".mpm"
USER_CONFIGS_DIR = USER_DATA_DIR / "configs"
USER_SCRIPTS_DIR = USER_DATA_DIR / "scripts"

PACKAGE_DIR = Path(mpm__file__).resolve().parent
