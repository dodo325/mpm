"""
Global MPM exception and warning classes.
"""


class ShellError(Exception):
    """ Shell Error """
    pass


class CommandNotFound(ShellError):
    """The Command Not Found"""
    pass


class PackageDoesNotExist(ShellError):
    """The Package does not exist"""
    pass
