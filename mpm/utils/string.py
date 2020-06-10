#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform


def auto_decode(text: bytes) -> str:
    if type(text) == str:
        return text
    if text == None:
        return ""
    os = platform.system()
    if os == "Windows":
        try:
            return text.decode("cp1251")
        except UnicodeDecodeError as e:
            return text.decode("utf-8")
        
    else:
        return text.decode("utf-8")


def is_ascii(s: str) -> bool:
    if s == "":
        return False
    return all(ord(c) < 128 for c in s)


def is_first_alpha(s: str) -> bool:
    if s == "":
        return False
    return s[0].isalpha()


def is_first_ascii_alpha(s: str) -> bool:
    if s == "":
        return False
    return ord(s[0]) < 128 and s[0].isalpha()
