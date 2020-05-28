#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform

def auto_decode(text: bytes) -> str:
    if type(text) == str:
        return text
    os = platform.system()
    if os == "Windows":
        return text.decode("cp1251")
    else:
        return text.decode("utf-8")
