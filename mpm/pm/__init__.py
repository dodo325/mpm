__version__ = '0.1'

from mpm.pm.package_managers import Apt, AptGet, Pip, get_installed_pms, PackageManager
from mpm.pm.packages import AptPackage, PipPackage

NAMES_TO_PACKAGE_MANAGERS = {
    cls.name:cls for cls in PackageManager._inheritors()
}
PACKAGE_MANAGERS_NAMES = list(NAMES_TO_PACKAGE_MANAGERS.keys())
