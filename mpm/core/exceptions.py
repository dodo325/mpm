"""
Global MPM exception and warning classes.
"""
from plumbum.commands import ProcessExecutionError

class PackageManagerNotInatalled(Exception):
    """Package Manager Not Inatalled"""

    pass


class PackageDoesNotExist(FileNotFoundError):
    """The Package does not exist"""
    pass

class PermissionDeniedError(ProcessExecutionError):
    pass

class PackageDoesNotInatalled(FileNotFoundError):
    """The Package does not Inatalled"""
    pass
