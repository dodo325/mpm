#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Main Scripts Manager 
'''
from shell import AutoShell
from typing import List, Tuple
from text_parse import is_first_ascii_alpha
from my_logging import logging
from shell import AutoShell, Bash
_LOG_PERFIX = __file__


class ScriptManager:
    """
    Base Script Manager
    """
    path = None
    name = ""

    def __init__(self, path):
        self.path
    

class BashScript(ScriptManager):
    pass


def main():
    print(__file__)


if __name__ == "__main__":
    main()
