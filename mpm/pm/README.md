# Package Managers
Этот модуль отвечает за работу с пакетными менеджарами 

PackageManager
* есть список всех установленных пакетов
* можкет найти пакет
* имеет имя команды
* можкет влиять на сам пакетный менеджер
  * например, добовлять ригистри
  * или обновлять список пакетов
* Вернуть пакет класс пакета

Package
* провепить установлен ли он
* проверить ли вообще существует ли данный пакет
* show 
  * может паказать информацию, только если пакет установленн
  * может паказать информацию, даже если пакет не установленн

## Про пакетные менеджеры:
### pip
работакт везде. не имеет русского (вроде).
* install
  * не требует превелегий
  *  удаление с помощю uninstall 
  *  есть --force-reinstall
  *  --upgrade
  *  -r --requirement <file>
*  show 
   *  может паказать информацию, только если пакет установленн
   * -vvv - больше инфы
   * 
 * freeze
   * выводит все пакеты через \n
   * {pkg_name}=={version}
 * search
   * ищет пакеты в PyPI
   * Вывод:
      ```bash
      urwid-satext (0.7.0)              - S&#224;T extension widgets for Urwid
      urwid-readline (0.11)             - A textbox edit widget for urwid that
                                          supports readline shortcuts
      urwid-utils (0.1.2)               - A collection of simple, straightforward,
                                          but extensible utilities for the urwid
                                          package.
      ```
   * c -vvv
      ```bash
      >>> pip search urwid -v  
      Getting credentials from keyring for pypi.org
      Starting new HTTPS connection (1): pypi.org:443
      https://pypi.org:443 "POST /pypi HTTP/1.1" 200 1169
      urwid-satext (0.7.0)              - S&#224;T extension widgets for Urwid
      urwid-readline (0.11)             - A textbox edit widget for urwid that supports readline shortcuts
      urwid-utils (0.1.2)               - A collection of simple, straightforward, but extensible utilities for the urwid package.
      urwid-ueberzogen (0.0.3)          - Some widgets which extend urwid with the possibility to use ueberzug.
      urwid (2.1.0)                     - A full-featured console (xterm et al.) user interface library
      ```
### apt
* есть на Unix (Debine)
* есть русский
* list - показать список пакетов на основе указанных имён
  * dpkg-query --list
  * Вывод:
   ```
   zvmcloudconnector-api/focal,focal 2.0.0~b1~git2019062011.4fc9142.really.1.4.1-0ubuntu3 all
   zvmcloudconnector-common/focal,focal 2.0.0~b1~git2019062011.4fc9142.really.1.4.1-0ubuntu3 all
   zynaddsubfx-data/focal,focal 3.0.5-2build1 all
   zynaddsubfx-dssi/focal 3.0.5-2build1 amd64
   zynaddsubfx-lv2/focal 3.0.5-2build1 amd64
   zynaddsubfx-vst/focal 3.0.5-2build1 amd64
   zynaddsubfx/focal 3.0.5-2build1 amd64
   zypper-common/focal,focal 1.14.11-2 all
   zypper-doc/focal,focal 1.14.11-2 all
   zypper/focal 1.14.11-2 amd64
   zytrax/focal 0+git20190810-2build1 amd64
   zziplib-bin/focal 0.13.62-3.2ubuntu1 amd64
   zziplib-bin/focal 0.13.62-3.2ubuntu1 i386
   zzuf/focal 0.15-1 amd64
   zzuf/focal 0.15-1 i386
   ```
* show
  * может паказать информацию, только если пакет установленн
  * apt-cache
* search
  * apt-cache
  * Вывод
   ```
   Sorting... Done
   Full Text Search... Done
   python-urwid-doc/focal,focal 2.0.1-3 all
      curses-based UI/widget library (common documentation)

   uwsgi-plugin-gevent-python3/focal 2.0.18-11ubuntu1 amd64
      gevent plugin for uWSGI (Python 3)

   ```
* install, reinstall, remove, update, purge == apt-get

apt-cache 
* search python-urwid
  * python-urwid-doc - curses-based UI/widget library (common documentation)
  * просто \n
  * Разделитель " - "

### snap
* Есть русский
* snap find - поиск
  * parse_table_with_columns
* info
  * может паказать информацию, даже если пакет не установленн

### npm
сложно парсить
* npm view - информация о пакете 
  * может паказать информацию, даже если пакет не установленн
  * Трудно парсить
* npm search инфо по пакиетам
  * нужен парсер
* npm list -g --depth=0

### Conda
как и pip
* list
* search