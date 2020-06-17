#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Main Package Manager
Данный модуль отвечает за управлетние и парсинг Sh скрипотов
"""
from mpm.shell import AutoShell, AbstractShell
from typing import List, Tuple
from mpm.core.logging import getLogger
from pathlib import Path
from mpm.utils.text_parse import not_nan_split

logger = getLogger(__name__)


class BashScriptFile:
    """
    Bash скрипт файл
    """

    content = ""

    def _filter_comments(self, lines: list) -> list:
        return list(filter(lambda s: not s.lstrip().startswith("#"), lines))

    def get_alias(self) -> dict:
        """
        >>> self.get_alias()
        {'lsp': 'stat -c "%a %n" *',
        'locip': "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\\.){3}[0-9]*' | grep -Eo '([0-9]*\\.){3}[0-9]*' | grep -v '127.0.0.1'",
        'myip': 'curl ipinfo.io/ip',
        'lsip': 'arp',
        'lsports': 'sudo lsof -i -P -n',
        'ды': 'ls',
        'св': 'св',
        'd2': 'source activate Django2',
        'dea': 'source deactivate',
        'pipver': "pip freeze | grep' "}
        """
        li = self.get_lines()
        li = list(filter(lambda s: s.startswith("alias "), li))
        alias_data = {}
        for alias in li:
            alias = alias.replace("alias ", "")
            name = alias[: alias.index("=")]
            cmd = alias[alias.index("=") + 1 :]
            if cmd.startswith('"') or cmd.startswith("'"):
                cmd = cmd[1:]
            if cmd.endswith('"') or cmd.endswith("'"):
                cmd = cmd[:-1]
            alias_data[name] = cmd
        return alias_data

    def get_lines(self) -> list:
        li = not_nan_split(self.content)
        return self._filter_comments(li)

    def __init__(self, path: str, shell: AbstractShell = None):
        self.logger = logger.getChild(self.__class__.__name__)
        if shell == None:
            self.shell = AutoShell()
        else:
            self.shell = shell

        file = Path(self.shell.echo(path))
        if file.is_file():
            self.file = file
            self.update()
        else:
            raise FileExistsError(f"Not found {path}")

    def add_data_in_file(self, data: str):
        if not data.endswith("\n"):
            data = data + "\n"
        with self.file.open("a") as file_object:
            file_object.write(data)

    def update(self):
        """
        update content
        """
        self.content = self.file.open().read().rstrip("\n")

    def add_alias(self, name: str, cmd: str):
        if name in self.get_alias():
            self.logger.info(f"Alias {name} already in {str(self.file)}!")
            return
        self.add_data_in_file(f'\nalias {name}="{cmd}"\n')
