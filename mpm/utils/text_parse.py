
import re
from typing import List

def remove_multiple_spaces(string: str) -> str:
    return re.sub(' +', ' ', string)


def not_nan_split(string: str, delimiter="\n") -> list:
    li = string.split(delimiter)
    return list(filter(None, li))

def parse_value_key_table(string: str, delimiter=":", remove_useless_space=True, multiline_spase=True, key_lower=False) -> dict:
    """
    Parse value key ASCII table
    Example:
    >>> print(t1)
    Name             : ConsoleHost
    Version          : 5.1.17763.1007
    InstanceId       : c3e8ce6b-68da-4a64-8659-7feacbed8244
    UI               : System.Management.Automation.Internal.Host.InternalHostUserInterface
    >>> parse_value_key_table(t1, key_lower=False)
    {'Name': 'ConsoleHost',
    'Version': '5.1.17763.1007',
    'InstanceId': 'c3e8ce6b-68da-4a64-8659-7feacbed8244',
    'UI': 'System.Management.Automation.Internal.Host.InternalHostUserInterface'}
    >>> parse_value_key_table(t1, key_lower=True)
    {'name': 'ConsoleHost',
    'version': '5.1.17763.1007',
    'instanceid': 'c3e8ce6b-68da-4a64-8659-7feacbed8244',
    'ui': 'System.Management.Automation.Internal.Host.InternalHostUserInterface'}
    
    >>> print(t2)
    Homepage: https://www.python.org/
    Description-ru: интерактивный высокоуровневый объектно-ориентированный язык (версия python3 по умолчанию)
     Python — интерактивный, объектно-ориентированный язык высокого уровня,
     включающий в себя обширную библиотеку классов с широкими возможностями для
     сетевого программирования, системного администрирования, работы со звуком
     и графикой.
     .
     This package is a dependency package, which depends on Debian's default
     Python 3 version (currently v3.8).
    Description-md5: 6c1cceeeaa25414388fa2227c3a214fe
    >>> parse_value_key_table(t2, multiline_spase=True)
    {'homepage': 'https://www.python.org/',
    'description-ru': "интерактивный высокоуровневый объектно-ориентированный язык (версия python3 по умолчанию)\n Python — интерактивный, объектно-ориентированный язык высокого уровня,\n включающий в себя обширную библиотеку классов с широкими возможностями для\n сетевого программирования, системного администрирования, работы со звуком\n и графикой.\n .\n This package is a dependency package, which depends on Debian's default\n Python 3 version (currently v3.8).",
    'description-md5': '6c1cceeeaa25414388fa2227c3a214fe'}
    >>> parse_value_key_table(t2, multiline_spase=False)
    {'homepage': 'https://www.python.org/',
    'description-ru': 'интерактивный высокоуровневый объектно-ориентированный язык (версия python3 по умолчанию)',
    ' python — интерактивный, объектно-ориентированный язык высокого уровня': 'Python — интерактивный, объектно-ориентированный язык высокого уровня,',
    ' включающий в себя обширную библиотеку классов с широкими возможностями дл': 'включающий в себя обширную библиотеку классов с широкими возможностями для',
    ' сетевого программирования, системного администрирования, работы со звуко': 'сетевого программирования, системного администрирования, работы со звуком',
    ' и графикой': 'и графикой.',
    '': '.',
    " this package is a dependency package, which depends on debian's defaul": "This package is a dependency package, which depends on Debian's default",
    ' python 3 version (currently v3.8)': 'Python 3 version (currently v3.8).',
    'description-md5': '6c1cceeeaa25414388fa2227c3a214fe'}
    """
    _TMP_MARK = "<!>"
    if multiline_spase:
        string = string.replace("\n ", _TMP_MARK)
    lines = string.split("\n")
    data = dict()
    for line in lines:
            if line == "":
                continue
            n = line.find(delimiter)
            key, value = line[:n], line[n + len(delimiter):]
            if remove_useless_space:
                key = key.strip()
                value = value.strip()
            if key_lower:
                key = key.lower()
            if multiline_spase:
                value = value.replace(_TMP_MARK, "\n ")
            data[key] = value
    return data


def parse_table_with_columns(string: str, delimiter=None, name_column_num=0, key_lower=False) -> dict:
    '''
    Parse ASCII tables!
    Example:
    >>> print(table)
    Название           Версия                     Издатель                Примечание  Описание
    telegram-desktop   2.1.7                      telegram.desktop        -           Official desktop client for the Telegram messenger
    smartscreen        1.0.1                      ypcloud                 -           Social Screen Interaction
    telegram-cli       1.4.5                      marius-quabeck          -           Command-line interface for Telegram. Uses the readline interface.
    monento            1.2.8                      ladnysoft               -           Cross-platform app for tracking personal finances with encrypted data syncing.
    ramboxpro          1.3.1                      ramboxapp*              -           Rambox Pro
    >>> parse_table_with_columns(table)
    {'telegram-desktop': {'Описание': 'Official desktop client for the Telegram messenger',
    'Примечание': '-',
    'Издатель': 'telegram.desktop',
    'Версия': '2.1.7'},
    'smartscreen': {'Описание': 'Social Screen Interaction',
    'Примечание': '-',
    'Издатель': 'ypcloud',
    'Версия': '1.0.1'},
    'telegram-cli': {'Описание': 'Command-line interface for Telegram. Uses the readline interface.',
    'Примечание': '-',
    'Издатель': 'marius-quabeck',
    'Версия': '1.4.5'},
    'monento': {'Описание': 'Cross-platform app for tracking personal finances with encrypted data syncing.',
    'Примечание': '-',
    'Издатель': 'ladnysoft',
    'Версия': '1.2.8'},
    'ramboxpro': {'Описание': 'Rambox Pro',
    'Примечание': '-',
    'Издатель': 'ramboxapp*',
    'Версия': '1.3.1'}}
    >>> parse_table_with_columns(t, key_lower=True)
    {'telegram-desktop': {'описание': 'Official desktop client for the Telegram messenger',
    'примечание': '-',
    'издатель': 'telegram.desktop',
    'версия': '2.1.7'},
    'smartscreen': {'описание': 'Social Screen Interaction',
    'примечание': '-',
    'издатель': 'ypcloud',
    'версия': '1.0.1'},
    'telegram-cli': {'описание': 'Command-line interface for Telegram. Uses the readline interface.',
    'примечание': '-',
    'издатель': 'marius-quabeck',
    'версия': '1.4.5'},
    'monento': {'описание': 'Cross-platform app for tracking personal finances with encrypted data syncing.',
    'примечание': '-',
    'издатель': 'ladnysoft',
    'версия': '1.2.8'},
    'ramboxpro': {'описание': 'Rambox Pro',
    'примечание': '-',
    'издатель': 'ramboxapp*',
    'версия': '1.3.1'}}
    '''
    if delimiter:
        string = string.replace(delimiter, "") # TODO: something...
    li = not_nan_split(string)
    head = li[0]
    head_list = []
    for m in re.finditer("(\w+)", head):
        key = head[m.start(0): m.end(0)]
        if key_lower:
            key = key.lower()
        head_list.append(
            (m.start(0), key)
        )
    name_key = head_list[name_column_num][1]
    head_list.reverse()
    data = {}
    
    for line in li[1:]:
        line_data = {}
        name = ''
        for start, key in head_list:
            val = line[start::]
            val = remove_multiple_spaces(val)
            val = val.strip()
            line = line[:start]
            if key != name_key:
                line_data[key] = val
            else:
                name = val
        data[name] = line_data
    return data
