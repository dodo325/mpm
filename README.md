[![PyPI-Status](https://img.shields.io/pypi/v/mpm-core.svg)](https://pypi.python.org/pypi/mpm-core)
[![Downloads](https://pepy.tech/badge/mpm-core)](https://pepy.tech/project/mpm-core)
[![Codecov](https://codecov.io/github/dodo325/mpm/coverage.svg?branch=master)](https://codecov.io/github/dodo325/mpm?branch=master)
[![Build-Status](https://travis-ci.org/dodo325/mpm.svg?branch=master)](https://travis-ci.org/dodo325/mpm)
[![LICENCE](https://img.shields.io/cran/l/mpm?logo=ddd)](https://github.com/dodo325/mpm/blob/master/LICENSE)

![](./logo1_mpm.png)

Main Package Manager - Unites all package managers in themselves!
- [Install](#install)
  - [pip](#pip)
  - [Sourse](#sourse)
- [Настройки](#настройки)
- [CLI](#cli)

## Install
### pip
```bash
    pip install mpm-core
```

### Sourse
```bash
    pip uninstall mpm-core -y && pip install ".[test]"
```
## Настройки
Создаются в папке $USER_HOME/.mpm/confgs

В проекте все данные хранятся в [mpm/data/configs](mpm/data/configs/README.md)

## CLI
```bash
mpm 0.2.0

Usage:
    mpm [SWITCHES] [SUBCOMMAND [SWITCHES]] args...

Meta-switches
    -h, --help         Prints this help message and quits
    --help-all         Print help messages of all subcommands and quit
    -v, --version      Prints the program's version and quits

Subcommands:
    info               Показать дополнительные данные о пакете; see 'mpm info --help' for more info
    install            Показать дополнительные данные о пакете; see 'mpm install --help' for more info
    list               List installed packages ; see 'mpm list --help' for more info
    search             Поиск пакета; see 'mpm search --help' for more info

mpm info 0.2.0

Показать дополнительные данные о пакете

Usage:
    mpm info [SWITCHES] package_name

Hidden-switches
    -h, --help                                    Prints this help message and quits
    --help-all                                    Print help messages of all subcommands and quit
    -v, --version                                 Prints the program's version and quits

Switches
    -a, --all                                     Search for information not only the known_packages
    -k, --package-manager VALUE:ExistingFile      known_packages.json file
    --off, --offline                              Search for information not only in local the known_packages
    --pm PM_NAMES:str                             Search in Package Manager: ['apt-get', 'conda', 'snap', 'npm', 'pip', 'apt']; may be given multiple times
    -q, --quiet                                   Disable Logging


mpm install 0.2.0

Показать дополнительные данные о пакете

Usage:
    mpm install [SWITCHES] package_name

Hidden-switches
    -h, --help                                    Prints this help message and quits
    --help-all                                    Print help messages of all subcommands and quit
    -v, --version                                 Prints the program's version and quits

Switches
    -a, --all                                     Search for information not only the known_packages
    -k, --package-manager VALUE:ExistingFile      known_packages.json file
    --no-auto                                     Search for information not only in local the known_packages
    --off, --offline                              Search for information not only in local the known_packages
    --pm PM_NAMES:str                             Search in Package Manager: ['apt-get', 'conda', 'snap', 'npm', 'pip', 'apt']; may be given multiple times
    -q, --quiet                                   Disable Logging


mpm list 0.2.0

List installed packages

Usage:
    mpm list [SWITCHES] 

Hidden-switches
    -h, --help                                    Prints this help message and quits
    --help-all                                    Print help messages of all subcommands and quit
    -v, --version                                 Prints the program's version and quits

Switches
    -a, --all                                     Search for information not only the known_packages
    -k, --package-manager VALUE:ExistingFile      known_packages.json file
    -o, --output VALUE:NonexistentPath            output in YAML file
    --off, --offline                              Search for information not only in local the known_packages
    --pm PM_NAMES:str                             Search in Package Manager: ['apt-get', 'conda', 'snap', 'npm', 'pip', 'apt']; may be given multiple times
    -q, --quiet                                   Disable Logging


mpm search 0.2.0

Поиск пакета

Usage:
    mpm search [SWITCHES] package_name

Hidden-switches
    -h, --help                                    Prints this help message and quits
    --help-all                                    Print help messages of all subcommands and quit
    -v, --version                                 Prints the program's version and quits

Switches
    -a, --all                                     Search for information not only the known_packages
    -k, --package-manager VALUE:ExistingFile      known_packages.json file
    -l, --list                                    List
    --off, --offline                              Search for information not only in local the known_packages
    --pm PM_NAMES:str                             Search in Package Manager: ['apt-get', 'conda', 'snap', 'npm', 'pip', 'apt']; may be given multiple times
    -q, --quiet                                   Disable Logging
```