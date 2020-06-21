[![Downloads](https://pepy.tech/badge/mpm-core)](https://pepy.tech/project/mpm-core)
[![Codecov](https://codecov.io/github/dodo325/mpm/coverage.svg?branch=master)](https://codecov.io/github/dodo325/mpm?branch=master)
[![Build-Status](https://travis-ci.org/dodo325/mpm.svg?branch=master)](https://travis-ci.org/dodo325/mpm)
[![LICENCE](https://img.shields.io/cran/l/mpm?logo=ddd)](https://github.com/dodo325/mpm/blob/master/LICENSE)

![](./logo1_mpm.png)

Main Package Manager - Unites all package managers in themselves!
  - [Install](#install)
    - [pip](#pip)
    - [Sourse](#sourse)
  - [CLI](#cli)
  - [Examples](#examples)
    - [Install](#install-1)
    - [Search](#search)
    - [Info](#info)
  - [API](#api)
    - [Shell](#shell)
      - [get_installed_shells](#get_installed_shells)
      - [AutoShell](#autoshell)
    - [Package Manager](#package-manager)

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
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  info       Показать дополнительные данные о пакете
  install    Установить пакет
  list       Список пакетов
  reinstall  Переустановить пакет
  remove     Удалить пакет
  search     Найти пакет
  update     Обновить пакет
```

## Examples
### Install
```bash
    # mpm install deepkit   
[INFO](2020-06-02 02:42:41) mpm.shell.shells.ZSH is_installed - installed! ver: zsh 5.8 (x86_64-ubuntu-linux-gnu)
[INFO](2020-06-02 02:42:42) mpm.pm.package_managers get_installed_pms - Installed packege managers: ['snap', 'apt-get', 'conda', 'apt', 'pip', 'npm']
[INFO](2020-06-02 02:42:44) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in npm!
[INFO](2020-06-02 02:42:45) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in snap!
[INFO](2020-06-02 02:42:46) mpm.pm.package_managers.Pip get_all_packages - Detect 265 packages
[INFO](2020-06-02 02:42:46) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in pip!
[WARNING](2020-06-02 02:42:47) mpm.pm.packages.UniversalePackage get_info - Package deepkit Does Not found in 'apt' package manager
[ERROR](2020-06-02 02:42:49) mpm.pm.package_managers.Conda search - Nothing found for deepkit!
subprocess.CalledProcessError: Command '['/bin/bash', '-c', 'conda search deepkit --json']' returned non-zero exit status 1.
[WARNING](2020-06-02 02:42:49) mpm.pm.packages.UniversalePackage get_info - Package deepkit Does Not found in 'conda' package manager
[INFO](2020-06-02 02:42:51) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in npm!
[INFO](2020-06-02 02:42:51) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in snap!
[INFO](2020-06-02 02:42:53) mpm.pm.package_managers.Pip get_all_packages - Detect 265 packages
[INFO](2020-06-02 02:42:53) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in pip!
[INFO](2020-06-02 02:42:55) mpm.pm.package_managers.NPM get_all_packages - Detect 1 packages
[INFO](2020-06-02 02:42:55) mpm.pm.package_managers.Snap get_all_packages - Detect 19 packages
[INFO](2020-06-02 02:42:55) mpm.pm.package_managers.Pip get_all_packages - Detect 265 packages
Package Managers:
0 : npm
1 : snap
2 : pip

Select a package manager:
2

You have chosen pip
[INFO](2020-06-02 02:43:01) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in pip!
[INFO](2020-06-02 02:43:01) mpm.pm.package_managers.Pip get_all_packages - Detect 265 packages
[INFO](2020-06-02 02:43:01) mpm.pm.packages.PipPackage install - Installing deepkit ({'version': '1.0.5', 'description': 'Python SDK for Deepkit'})...
[INFO](2020-06-02 02:43:03) mpm.pm.package_managers.Pip get_all_packages - Detect 266 packages
[SUCCESS](2020-06-02 02:43:03) mpm.pm.packages.PipPackage install - Package installed!
```
### Search
```bash
    # mpm search 123 -pm apt -pm pip
[INFO](2020-06-02 03:00:16) mpm.shell.shells.Bash is_installed - installed! ver: 5.0.16(1)-release (x86_64-pc-linux-gnu)
[INFO](2020-06-02 03:00:16) mpm.pm.package_managers get_installed_pms - Installed packege managers: ['apt', 'pip', 'npm', 'snap', 'conda', 'apt-get']

	apt:
- libmpg123-0: {'description': 'MPEG layer 1/2/3 audio decoder (shared library)'}
- libmpg123-dev: {'description': 'MPEG layer 1/2/3 audio decoder (development files)'}
- libout123-0: {'description': 'MPEG layer 1/2/3 audio decoder (libout123 shared library)'}
- cutmp3: {'description': 'small and fast command line MP3 editor'}
- flashrom: {'description': 'раcпознавание, чтение, запись, очистка и проверка BIOS/ПЗУ/flash-чипов'}
- gst123: {'description': 'Основанный на GStreamer медиапроигрыватель для командной строки'}
- irssi-scripts: {'description': 'Набор сценариев для irssi'}
- libghc-tree-monad-dev: {'description': 'Non-Determinism Monad for Tree Search'}
- libnxml0: {'description': 'C library for parsing, writing and creating xml 1.0/1.1 files or streams'}
- mpc123: {'description': 'аудиопроигрыватель файлов Musepack для командной строки'}
- mpg123: {'description': 'аудиоплеер MPEG уровней 1/2/3'}
- mpg321: {'description': 'простой и легковесный проигрыватель MP3 для командной строки'}
- music123: {'description': 'Command-line shell for sound-file players'}
- tcs: {'description': 'перевод текстов в другие кодировки'}
- xmms2-plugin-mpg123: {'description': 'XMMS2 — основанный на libmpg123 декодер MP3'}
- dict-freedict-fin-swe: {'description': 'Finnish-Swedish dictionary for the dict server/client'}
- ftp-proxy: {'description': 'application level proxy for the FTP protocol'}
- golang-github-alecthomas-repr-dev: {'description': "Python's repr() for Go"}
- golang-github-jinzhu-now-dev: {'description': 'time toolkit for golang'}
- jack-stdio: {'description': 'program to pipe audio-data from and to JACK'}
- libdata-methodproxy-perl: {'description': 'module to inject dynamic data into static data'}
- libghc-tree-monad-prof: {'description': 'Non-Determinism Monad for Tree Search; profiling libraries'}
- liblexical-var-perl: {'description': 'Perl module for using static variables without namespace pollution'}
- libmath-bigint-perl: {'description': 'arbitrary size integer/float math package'}
- libmath-nocarry-perl: {'description': 'Perl module for no carry arithmetic'}
- libnxml0-dev: {'description': 'static library and C header files for libnxml0'}
- librandom123-dev: {'description': 'parallel random numbers library'}
- librandom123-doc: {'description': 'documentation and examples of parallel random numbers library'}
- libscalar-properties-perl: {'description': 'perl module to add run-time properties on scalar variables'}
- libyangrpc-dev: {'description': 'NETCONF/YANG simple client applications development files'}
- libyangrpc2: {'description': 'NETCONF/YANG library for simple client applications'}
- libyuma-dev: {'description': 'NETCONF/YANG application development files'}
- libyuma2: {'description': 'NETCONF/YANG library'}
- modem-cmd: {'description': 'send arbitrary AT commands to your modem'}
- mpg123-el: {'description': 'front-end to mpg321/ogg321 media players for Emacs'}
- netconfd: {'description': 'NETCONF (RFC-6241) agent'}
- netconfd-module-ietf-interfaces: {'description': 'SIL module for netconfd implementing ietf-interfaces.yang'}
- netconfd-module-ietf-system: {'description': 'SIL module for netconfd implementing ietf-system.yang'}
- openmpt123: {'description': 'module music library based on OpenMPT -- music player'}
- plymouth-disabler: {'description': 'disable plymouth by installing .override files'}
- postgresql-12-prefix: {'description': 'Prefix Range module for PostgreSQL'}
- ruby-htmlentities: {'description': 'Ruby library for handling HTML entities'}
- texlive-latex-extra: {'description': 'TeX Live: LaTeX additional packages'}
- trscripts: {'description': 'Scripts for reencoding text files and BDF-fonts'}
- upse123: {'description': 'commandline player based on libupse'}
- vorbis-tools: {'description': 'several Ogg Vorbis tools'}
- yangcli: {'description': 'NETCONF/YANG command line client application'}
- brother-cups-wrapper-laser1: {'description': 'Cups Wrapper drivers for laser1 brother printers'}
- brother-lpr-drivers-laser1: {'description': 'Драйверы LPR для лазерных принтеров Brother'}

	pip:
- pkg-example-123: {'version': '0.0.3', 'description': 'A small example package'}
- topper-123-engarde: {'version': '0.3.4', 'description': 'A python package for defensive data analysis.'}
- ml-automated-123: {'version': '1.0', 'description': 'Automated machine learning'}
- odoo8-addon-l10n-es-aeat-mod123: {'version': '8.0.1.1.0', 'description': 'AEAT modelo 123'}
- odoo12-addon-l10n-es-aeat-mod123: {'version': '12.0.1.3.0', 'description': 'AEAT modelo 123'}
- odoo11-addon-l10n-es-aeat-mod123: {'version': '11.0.1.1.0', 'description': 'AEAT modelo 123'}
```

### Info
```bash
    # mpm info 123                  
[INFO](2020-06-02 03:02:06) mpm.shell.shells.Bash is_installed - installed! ver: 5.0.16(1)-release (x86_64-pc-linux-gnu)
[INFO](2020-06-02 03:02:06) mpm.pm.package_managers get_installed_pms - Installed packege managers: ['conda', 'apt-get', 'apt', 'pip', 'npm', 'snap']
[WARNING](2020-06-02 03:02:07) mpm.pm.packages.UniversalePackage get_info - Package 123 Does Not found in 'conda' package manager
[INFO](2020-06-02 03:02:12) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in npm!
[WARNING](2020-06-02 03:02:13) mpm.pm.packages.UniversalePackage get_info - Package 123 Does Not found in 'snap' package manager
[WARNING](2020-06-02 03:02:15) mpm.pm.packages.UniversalePackage get_info - Package 123 Does Not found in 'pip' package manager
[WARNING](2020-06-02 03:02:16) mpm.pm.packages.UniversalePackage get_info - Package 123 Does Not found in 'apt' package manager
[INFO](2020-06-02 03:02:18) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in npm!

	npm:
- keywords: ['123']
- version: 0.0.1
- date: 2013-12-20
- author: 123
- description: 123
- _id: 123@0.0.1
- _rev: 3-a7050df47889a35997c6a305b7162e8c
- dist-tags: {'latest': '0.0.1'}
- versions: ['0.0.1']
- maintainers: ['feitian <799504343@qq.com>']
- time: {'modified': '2013-12-20T08:25:02.552Z', 'created': '2013-12-20T08:24:49.019Z', '0.0.1': '2013-12-20T08:25:02.552Z'}
- repository: {'type': 'git', 'url': '123'}
- _attachments: {}
- _cached: True
- _contentLength: 0
- main: helloworld.js
- scripts: {'test': '123'}
- license: 123
- readme: ERROR: No README data found!
- dist: {'shasum': '3351ea3950963c3539e396ce51a441f97111991f', 'tarball': 'https://registry.npmjs.org/123/-/123-0.0.1.tgz'}
- _from: .
- _npmVersion: 1.3.17
- _npmUser: feitian <799504343@qq.com>
- directories: {}
[INFO](2020-06-02 03:02:18) mpm.core.configs update_user_known_package - Update user known package. Package 123
```

## API
### Shell
read more in [this](mpm/shell/README.md)
#### get_installed_shells
Return all installed shells

Example:
```python
>>> get_installed_shells()
[mpm.shell.shells.ZSH, mpm.shell.shells.Bash]
```
#### AutoShell
Returns one of the installed shells. Or by 'name'

Example:
```python
>>> AutoShell()
<mpm.shell.shells.ZSH at 0x7f5d3dcb9e90>

>>> AutoShell('bash')
<mpm.shell.shells.Bash at 0x7f5d3ddcc910>
```

### Package Manager
Read more in [this file](mpm/pm/README.md)
Example:
```python
>>> from mpm.pm import get_installed_pms, UniversalePackage
>>> get_installed_pms()
[mpm.pm.package_managers.Conda,
 mpm.pm.package_managers.AptGet,
 mpm.pm.package_managers.Apt,
 mpm.pm.package_managers.Pip,
 mpm.pm.package_managers.NPM,
 mpm.pm.package_managers.Snap]

 >>> pkg = UniversalePackage("deepkit")
 >>> pkg.is_installed()
 False
 
 >>> pkg.pm_packages
 [<mpm.pm.packages.NPMPackage at 0x7f5d3dba4d90>,
 <mpm.pm.packages.SnapPackage at 0x7f5d3dba4f50>,
 <mpm.pm.packages.PipPackage at 0x7f5d3dba4f90>]
 
 >>> pkg.config
 {'package_managers': {'npm': {}, 'snap': {}, 'pip': {}}}
 
 >>> pkg.install()
 [INFO](2020-06-02 02:39:49) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in npm!
[INFO](2020-06-02 02:39:50) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in snap!
[INFO](2020-06-02 02:39:52) mpm.pm.package_managers.Pip get_all_packages - Detect 262 packages
[INFO](2020-06-02 02:39:52) mpm.pm.packages.UniversalePackage add_package_manager_in_config - Detected in pip!
[INFO](2020-06-02 02:39:53) mpm.pm.package_managers.NPM get_all_packages - Detect 1 packages
[INFO](2020-06-02 02:39:53) mpm.pm.package_managers.Snap get_all_packages - Detect 19 packages
[INFO](2020-06-02 02:39:53) mpm.pm.package_managers.Pip get_all_packages - Detect 262 packages
Package Managers:
0 : npm
1 : snap
2 : pip

Select a package manager:
 2

You have chosen pip
[INFO](2020-06-02 02:40:03) mpm.pm.package_managers.Pip get_all_packages - Detect 262 packages
[INFO](2020-06-02 02:40:03) mpm.pm.packages.PipPackage install - Installing deepkit ({'version': '1.0.5', 'description': 'Python SDK for Deepkit'})...
[INFO](2020-06-02 02:40:13) mpm.pm.package_managers.Pip get_all_packages - Detect 266 packages
[SUCCESS](2020-06-02 02:40:14) mpm.pm.packages.PipPackage install - Package installed!
[INFO](2020-06-02 02:40:15) mpm.pm.package_managers.NPM get_all_packages - Detect 1 packages
[INFO](2020-06-02 02:40:15) mpm.pm.package_managers.Snap get_all_packages - Detect 19 packages
[INFO](2020-06-02 02:40:15) mpm.pm.package_managers.Pip get_all_packages - Detect 266 packages
[SUCCESS](2020-06-02 02:40:15) mpm.pm.packages.UniversalePackage install - Package installed!

 >>> pkg.info
 {'npm': {'keywords': '',
  'version': '1.1.0',
  'date': '2019-07-30',
  'author': 'Elmer Bulthuis',
  'description': 'NEVER commit something that breaks the build! If you do, you suck. You can easily prevent this by linking the `test.sh` script as a git `pre-push` or `pre-commit` hook!',
  '_id': 'deepkit@1.1.0',
  '_rev': '7-6326c8ba7449d66c7bfc47fc345842da',
  'dist-tags': {'latest': '1.1.0'},
  'versions': ['0.0.1', '0.1.0', '0.1.1', '0.2.0', '1.0.0', '1.0.1', '1.1.0'],
  'maintainers': ['elmerbulthuis <elmerbulthuis@gmail.com>'],
  'time': {'modified': '2019-07-30T10:40:28.579Z',
   'created': '2018-02-05T09:24:34.339Z',
   '0.0.1': '2018-02-05T09:24:34.339Z',
   '0.1.0': '2018-02-26T20:23:21.047Z',
   '0.1.1': '2018-04-10T08:55:28.590Z',
   '0.2.0': '2019-07-14T20:14:02.530Z',
   '1.0.0': '2019-07-14T21:16:56.758Z',
   '1.0.1': '2019-07-14T21:29:27.008Z',
   '1.1.0': '2019-07-30T10:40:25.749Z'},
  'license': 'ISC',
  'readmeFilename': 'readme.markdown',
  'homepage': 'https://github.com/LuvDaSun/deepkit#readme',
  'repository': {'type': 'git',
   'url': 'git+https://github.com/LuvDaSun/deepkit.git'},
  'bugs': {'url': 'https://github.com/LuvDaSun/deepkit/issues'},
  '_cached': True,
  '_contentLength': 0,
  'main': './node/main.js',
  'module': './module/main.js',
  'types': './types/main.d.ts',
  'sideEffects': False,
  'scripts': {'prepare': 'npm run compile',
   'compile': 'tsc && tsc --project tsconfig.module.json',
   'clean': 'rm -rf node types module',
   'test': 'npm run spec-all',
   'lint': 'tslint "src/**/*.ts"',
   'spec': 'tape --require "ts-node/register"',
   'spec-all': 'npm run spec "src/**/*.spec.ts"',
   'coverage': 'nyc --report-dir report --reporter text-summary --reporter lcov --include "src/**/*.ts" --exclude "src/**/*.spec.ts" --extension ".ts" npm test'},
  'devDependencies': {'@types/blue-tape': '^0.1.33',
   '@types/tape': '^4.2.33',
   'blue-tape': '^1.0.0',
   'nyc': '^14.1.1',
   'tape': '^4.11.0',
   'ts-node': '^8.3.0',
   'tslint': '^5.18.0',
   'typescript': '^3.5.3'},
  'dependencies': {'tslib': '^1.10.0'},
  'gitHead': 'aa2b80d57637b9af1c0f0a6efffa18102c38ed4e',
  '_nodeVersion': '12.6.0',
  '_npmVersion': '6.9.0',
  'dist': {'integrity': 'sha512-RqtQVTjlp7pOwUto5LNwHctGkDRcbDCwIiocwP1Pfdoe3AiVD971KrhgXIXumP91PwIk69xjMO4x1triaz5msg==',
   'shasum': 'f18c6671fe981297b890a85e022188ab75e5123b',
   'tarball': 'https://registry.npmjs.org/deepkit/-/deepkit-1.1.0.tgz',
   'fileCount': 36,
   'unpackedSize': 62848,
   'npm-signature': '-----BEGIN PGP SIGNATURE-----\r\nVersion: OpenPGP.js v3.0.4\r\nComment: https://openpgpjs.org\r\n\r\nwsFcBAEBCAAQBQJdQB6aCRA9TVsSAnZWagAAYjQQAKUYONQIlo6oW23sbPHO\nEDGEZJ8TjnmnktOCgN6avBvZEjUIdm+MrrUqqsMfTP5XoxMmT1lA5co6ooRb\nTd4byv7bKa3tOV5aba23UQnA7YnhPqmOPaON5JUucei28hclHmTxZBxJbXIw\nIpoHBNJoFUvbAHQdGc2DnzGb+aebLe/ueJ5goCq32PIMtQJBvPo19Yy7nwgK\nSN+VfH+3kPbJ/HgZ9lmez3rRZrLa+/xXgAZD3EXmF3ZkqLPPDJGH2hDUoaPb\nMCiXizRhI4dVNN0KPjWa5LTOE2r21GCWpHlkLkqG4IV4ePVc77+h0UM1zHcW\npZiQuYKBptm6T0LN0FSgybbuRDf2DHnIlV8KYKe6GVlePNM2TXCa7Ev1UW3Z\n4AVKLEOwS9mtlTFKgTubrP+zfaCElviAUlTiiuWcQ6Rn2yWSORlBj420WcLH\nY0fs8B86rl5/xrPT6bJOLqCSTXOOpbnm+EksDzga1OrjbW7n8XoGfCzJD/bM\nCl84TMOOAwlg+P/P3v5xCGBvOt3zpQTtpPxrqTiL7D0hE0Vb1SliAn70Mt7F\no3jEbiLI9EPS7O2qPeq8areHkAviUFBeqQbuOywLZd2zW4mfJDRuSoE1atwq\nDMVBxDOBqdxIXKUzqpOBaduObhpqkZ6P0aOUEuLA9wIxNj8ScpDyaH9sMNFU\noSyo\r\n=xu2P\r\n-----END PGP SIGNATURE-----\r\n'},
  '_npmUser': 'elmerbulthuis <elmerbulthuis@gmail.com>',
  'directories': {},
  '_npmOperationalInternal': {'host': 's3://npm-registry-packages',
   'tmp': 'tmp/deepkit_1.1.0_1564483225594_0.4729254376887817'},
  '_hasShrinkwrap': False},
 'snap': {'summary': 'The collaborative and analytical training suite for insightful,\n  fast, and reproducible modern machine learning.',
  'notes': '-',
  'publisher': 'Marc Schmidt (deepkit)',
  'version': '2020.1.5',
  'name': 'deepkit',
  'store-url': 'https://snapcraft.io/deepkit',
  'contact': 'info@deepkit.ai',
  'license': 'Proprietary',
  'description': '|\n  The collaborative and analytical training suite for insightful, fast, and\n  reproducible modern machine learning. All in one cross-platform desktop app\n  for you alone, corporate or open-source teams.\n  \n  Track your experiments, debug your machine learning models, and manage your\n  computation servers. It’s made for you as a single developer working\n  completely offline and teams with real-time collaboration tools out of the\n  box.\n  \n  \n  FEATURES\n  \n  - Experiment execution on your workstation directly or in Docker\n  - Unified experiment definition using YAML\n  - Automatic versioning of your experiment: configs, files, outputs & more\n  - Analytical data of your experiment in real-time\n  - Hardware monitoring of CPUs, memory, GPUs, & more\n  - Tensorflow and Pytorch debugger\n  - Execute your experiments on any Linux server\n  - Issue tracker\n  - Notes\n  \n  \n  FEATURES EXPLAINED\n  \n  - Execute experiments on your workstation in Docker, automatically\n  provisioned.\n  - Automatically track every execution.\n  - Attach custom analytical data (metrics, files, images, logs, numpy\n  arrays) to experiments using the free Python SDK.\n  - Tensorflow and Pytorch model debugger, for debugging the model graph +\n  visualize the output of each layer including histograms of activations,\n  weights, and biases.\n  - Connect any Linux machine via ssh credentials and execute your\n  experiments on team with a simple click or CLI argument.\n  - Mange your project using the integrated issue tracker\n  \n  \n  DO IT IN REAL-TIME WITH FRIENDS\n  \n  Create an account at deepkit.ai (in the app) to share your experiments in\n  real-time with your friend and colleagues. You can switch between your\n  local environment and the deepkit.ai server anytime directly in the app.',
  'snap-id': 'p2eXSHjh57KzwV6j1A1OumY9BKWDnSob',
  'channels': '\n  latest/stable:    --                             \n  latest/candidate: --                             \n  latest/beta:      --                             \n  latest/edge:      2020.1.5 2020-03-30 (12) 113MB -'},
 'pip': {'version': '1.0.5',
  'description': 'Python SDK for Deepkit',
  'installed': '1.0.5 (latest)',
  'name': 'deepkit',
  'summary': 'Python SDK for Deepkit',
  'home-page': 'https://github.com/deepkit/deepkit-python-sdk',
  'author': 'Marc J. Schmidt',
  'author-email': 'marc@marcjschmidt.de',
  'license': 'MIT',
  'location': '/home/dodo/anaconda3/lib/python3.7/site-packages',
  'requires': 'websockets, rx, psutil, PyYAML, typedload, Pillow, numpy',
  'required-by': '',
  'metadata-version': '2.1',
  'installer': 'pip',
  'classifiers': '',
  'entry-points': ''}}
 ```