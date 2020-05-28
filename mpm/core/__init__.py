__version__ = '0.1'

from mpm.core.exceptions import PackageDoesNotExist
from pathlib import Path
from mpm import __file__ as mpm__file__


PACKAGE_DIR = Path(mpm__file__).resolve().parent.parent
SCRIPTS_DIR = PACKAGE_DIR / "scripts"
CONFIGS_DIR = PACKAGE_DIR / "configs"

USER_DATA_DIR = Path.home() / ".mpm"
USER_CONFIGS_DIR = USER_DATA_DIR / "configs"
USER_SCRIPTS_DIR = USER_DATA_DIR / "scripts"

LOGGING_DIR = USER_DATA_DIR / "logs"


