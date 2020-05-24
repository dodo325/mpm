#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Main Package Manager 
'''

# class LinuxChs:
#     pass

class PackageManager:
    """ Main Package Manager """
    package_name: str

    def __init__(self, package_name):
        self.package_name = package_name
    
    def __str__(self):
        return f"{package_name}"

    def is_install() -> bool:
        return False
    

class AptPackage(PackageManager):
    """ Apt Package """



def main():
    pass

if __name__ == "__main__":
    main()
