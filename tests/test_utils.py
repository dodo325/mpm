import sys
import mpm
import platform
import subprocess
import pytest
from pathlib import Path
from mpm.utils.text_parse import (
    not_nan_split,
    remove_multiple_spaces,
    parse_value_key_table,
    parse_table_with_columns,
)
from mpm.utils.sys_info import is_64bit
from mpm.utils.string import auto_decode, is_ascii, is_first_alpha, is_first_ascii_alpha
from mpm.utils.json_parse import multiget


def test_multiget():
    data = {"a": 123, "b": "abc"}
    assert multiget(data, ["a", "b", "c"]) == 123
    assert multiget(data, ["d", "b", "c"]) == "abc"
    assert multiget(data, ["d", "v", "c"]) == None
    assert multiget(data, ["d", "v", "c"], default=321) == 321


def test_is_ascii_1():
    assert is_ascii("123456789")
    assert is_ascii("123456789/*-+.0qweryutop[]\asdfghjkl;'zcxvbnm.,\n")


def test_is_ascii_2():
    assert not is_ascii("фыв123456789")
    assert not is_ascii("123456789/*-+.0qweryutop[]\asdfghjkl;'zcxvbnm.,\nс")


def test_is_first_alpha_1():
    assert is_first_alpha("qwe32sa13")
    assert is_first_alpha("йыфввф123ваы")


def test_is_first_alpha_2():
    assert not is_first_alpha("1adasfa;")
    assert not is_first_alpha("123цйуывф")
    assert not is_first_alpha(" цйуывф")


def test_is_is_first_ascii_alpha_1():
    assert is_first_ascii_alpha("qweqe123")
    assert is_first_ascii_alpha("a1323")
    assert is_first_ascii_alpha("a323ы")


def test_is_is_first_ascii_alpha_2():
    assert not is_first_ascii_alpha(" qweqe123")
    assert not is_first_ascii_alpha("1a323")
    assert not is_first_ascii_alpha("ы123")


def test_auto_decode_utf8():
    text = "123qweqwasd фыаывпы"
    assert auto_decode(text.encode("utf-8")) == text


@pytest.mark.xfail(platform.system() != "Windows", reason="requires Windows")
def test_auto_decode_cp1251():
    text = "123qweqwasd фыаывпы"
    assert auto_decode(text.encode("cp1251")) == text


def test_is_64():
    assert is_64bit()


def test_not_nan_split_1():
    a = """asdasa
    asdad
    a



    asdasd"""
    out = remove_multiple_spaces(a)
    li = not_nan_split(out)
    assert len(li) == 4


def test_parse_value_key_table_1():
    t1 = """
Name             : ConsoleHost
Version          : 5.1.17763.1007
InstanceId       : c3e8ce6b-68da-4a64-8659-7feacbed8244
UI               : System.Management.Automation.Internal.Host.InternalHostUserInterface"""
    data = parse_value_key_table(t1, key_lower=False)
    assert data == {
        "Name": "ConsoleHost",
        "Version": "5.1.17763.1007",
        "InstanceId": "c3e8ce6b-68da-4a64-8659-7feacbed8244",
        "UI": "System.Management.Automation.Internal.Host.InternalHostUserInterface",
    }
    data2 = parse_value_key_table(t1, key_lower=True)
    assert data2 == {
        "name": "ConsoleHost",
        "version": "5.1.17763.1007",
        "instanceid": "c3e8ce6b-68da-4a64-8659-7feacbed8244",
        "ui": "System.Management.Automation.Internal.Host.InternalHostUserInterface",
    }


def test_parse_value_key_table_2():
    t2 = """Homepage: https://www.python.org/
Description-ru: интерактивный высокоуровневый объектно-ориентированный язык (версия python3 по умолчанию)
 Python — интерактивный, объектно-ориентированный язык высокого уровня,
 включающий в себя обширную библиотеку классов с широкими возможностями для
 сетевого программирования, системного администрирования, работы со звуком
 и графикой.
 .
 This package is a dependency package, which depends on Debian's default
 Python 3 version (currently v3.8).
Description-md5: 6c1cceeeaa25414388fa2227c3a214fe"""
    data = parse_value_key_table(t2, multiline_spase=True)
    assert data == {
        "Homepage": "https://www.python.org/",
        "Description-ru": "интерактивный высокоуровневый объектно-ориентированный язык (версия python3 по умолчанию)\n Python — интерактивный, объектно-ориентированный язык высокого уровня,\n включающий в себя обширную библиотеку классов с широкими возможностями для\n сетевого программирования, системного администрирования, работы со звуком\n и графикой.\n .\n This package is a dependency package, which depends on Debian's default\n Python 3 version (currently v3.8).",
        "Description-md5": "6c1cceeeaa25414388fa2227c3a214fe",
    }


def test_parse_table_with_columns_1():
    t1 = """
Название           Версия                     Издатель                Примечание  Описание
telegram-desktop   2.1.7                      telegram.desktop        -           Official desktop client for the Telegram messenger
smartscreen        1.0.1                      ypcloud                 -           Social Screen Interaction
telegram-cli       1.4.5                      marius-quabeck          -           Command-line interface for Telegram. Uses the readline interface.
monento            1.2.8                      ladnysoft               -           Cross-platform app for tracking personal finances with encrypted data syncing.
ramboxpro          1.3.1                      ramboxapp*              -           Rambox Pro
    """
    data = parse_table_with_columns(t1)
    assert data == {
        "telegram-desktop": {
            "Описание": "Official desktop client for the Telegram messenger",
            "Примечание": "-",
            "Издатель": "telegram.desktop",
            "Версия": "2.1.7",
        },
        "smartscreen": {
            "Описание": "Social Screen Interaction",
            "Примечание": "-",
            "Издатель": "ypcloud",
            "Версия": "1.0.1",
        },
        "telegram-cli": {
            "Описание": "Command-line interface for Telegram. Uses the readline interface.",
            "Примечание": "-",
            "Издатель": "marius-quabeck",
            "Версия": "1.4.5",
        },
        "monento": {
            "Описание": "Cross-platform app for tracking personal finances with encrypted data syncing.",
            "Примечание": "-",
            "Издатель": "ladnysoft",
            "Версия": "1.2.8",
        },
        "ramboxpro": {
            "Описание": "Rambox Pro",
            "Примечание": "-",
            "Издатель": "ramboxapp*",
            "Версия": "1.3.1",
        },
    }
    assert parse_table_with_columns(t1, key_lower=True) == {
        "monento": {
            "версия": "1.2.8",
            "издатель": "ladnysoft",
            "описание": "Cross-platform app for tracking personal finances with encrypted data syncing.",
            "примечание": "-",
        },
        "ramboxpro": {
            "версия": "1.3.1",
            "издатель": "ramboxapp*",
            "описание": "Rambox Pro",
            "примечание": "-",
        },
        "smartscreen": {
            "версия": "1.0.1",
            "издатель": "ypcloud",
            "описание": "Social Screen Interaction",
            "примечание": "-",
        },
        "telegram-cli": {
            "версия": "1.4.5",
            "издатель": "marius-quabeck",
            "описание": "Command-line interface for Telegram. Uses the readline interface.",
            "примечание": "-",
        },
        "telegram-desktop": {
            "версия": "2.1.7",
            "издатель": "telegram.desktop",
            "описание": "Official desktop client for the Telegram messenger",
            "примечание": "-",
        },
    }
