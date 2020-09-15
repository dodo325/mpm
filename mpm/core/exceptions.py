"""
Global MPM exception and warning classes.
"""
from plumbum.commands import ProcessExecutionError

class PackageManagerNotInatalled(Exception):
    """Package Manager Not Inatalled"""

    pass


class PackageDoesNotExist():
    """The Package does not exist"""

    pass


class PackageDoesNotInatalled():
    """The Package does not Inatalled"""

    pass

class PermissionDeniedError(ProcessExecutionError):
    pass
