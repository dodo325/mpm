#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform


def is_64bit() -> bool:
    """is platform 64bit

    Returns:
        bool: is platform 64bit
    """
    return platform.architecture()[0] == "64bit"
