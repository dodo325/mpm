#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Scripts Manager 
"""
from shell import AutoShell
from typing import List, Tuple
from mpm.shell import AutoShell, Bash
from mpm.core.logging import getLogger

logger = getLogger(__name__)


class ScriptManager:
    """
    Base Script Manager
    """

    path = None
    name = ""

    def __init__(self, path):
        self.path
        self.logger = logger.getChild(self.__class__.__name__)


class BashScript(ScriptManager):
    pass


def main():
    print(__file__)


if __name__ == "__main__":
    main()
