"""
Global MPM exception and warning classes.
"""


class ShellError(Exception):
    """The requested model field does not exist"""
    pass


class PackageDoesNotExist(ShellError):
    """The requested model field does not exist"""
    pass
