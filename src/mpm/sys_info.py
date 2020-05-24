#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform

def is_64bit():
    return platform.architecture()[0] == "64bit"


def main():
    pass

if __name__ == "__main__":
    main()