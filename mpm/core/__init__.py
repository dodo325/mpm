from mpm.core.exceptions import PackageDoesNotExist
from pathlib import Path
from mpm import __file__ as mpm__file__


PACKAGE_DIR = Path(mpm__file__).resolve().parent
if PACKAGE_DIR.parts[-1].startswith("mpm") and PACKAGE_DIR.parts[-2].startswith("mpm"):
    PACKAGE_DIR = PACKAGE_DIR.parent
SCRIPTS_DIR = PACKAGE_DIR / "scripts"
CONFIGS_DIR = PACKAGE_DIR / "configs"

USER_DATA_DIR = Path.home() / ".mpm"
USER_CONFIGS_DIR = USER_DATA_DIR / "configs"
USER_SCRIPTS_DIR = USER_DATA_DIR / "scripts"

LOGGING_DIR = USER_DATA_DIR / "logs"
