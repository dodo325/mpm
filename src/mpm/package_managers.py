#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Main Package Manager 
'''
from shell import AutoShell
# class LinuxChs:
#     pass

class PackageManager:
    """ Main Package Manager """
    name: str
    executable_path: str
    def __init__(self):
        pass
    
    def __str__(self):
        return f"{package_name}"

    def is_installed(self) -> bool:
        return False

class Apt(PackageManager):
    """ Apt Package """
    
    def __init__(self):
        self.shell = AutoShell()


    def is_installed(self) -> bool:
        return self.shell.check_command("apt")

# Package:
class Package:
    """ Package Class """
    package_name: str
    pm: "PackageManager" = None

    def __init__(self, package_name):
        self.package_name = package_name

    def __str__(self):
        return f"{package_name}"

    def is_pm_installed(self) -> bool:
        return self.pm.is_installed()
        
    def is_installed(self) -> bool:
        return False

# class PipPackage(PackageManager):
#     """ PIP Package """

#     @classmethod
#     def is_pm_installed(cls) -> bool:
#         shell = AutoShell()
#         return shell.check_command

class AptPackage(PackageManager):
    """ Apt Package """
    pm = Apt


def main():
    pass

if __name__ == "__main__":
    main()
