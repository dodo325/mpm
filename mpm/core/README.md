# Ядро проекта



## Алгоритмы работы некоторых комманд:

* loging files: $HOME/.mpm/logs/*.log
### Подготовка known_packages [+]
1. Парситим settings.json, перезаписываем его в соответствии с $HOME/.mpm/configs/settings.json
2. Из known_packages_url получаем known_packages, если возникла ошибка, то смотрим локальный known_packages
3. перезаписываем known_packages в соответствии с $HOME/.mpm/configs/known_packages.json
   
### mpm install [package_name]
1. Подготовка known_packages [+]
   1. если в аргуметне есть ссылка на дополнительый known_packages.json (на файл или URL), то перезаписываем known_packages в соответствии с ним [+]
2. Проверяем список доступных менеджеров [+]
3. проверяем установвлен ли в них паект (в соответствии с коныигом, но не обязательно только с ним... [аргумент --only-known-packages]) [+]
   1. если установлен, то пишем информацию о нём пользователю [+]
   2. если его нет в known_packages, но он установлен, то записываем это соответственно в $HOME/.mpm/configs/known_packages.json [+]
4. Устанавливаем пакет
   1. в соответствии с known_packages # сложна!
   2. находим его в других пакетных менаджарах, даём пользователю выбрать один из них

### mpm remove [package_name]
1. Подготовка known_packages
   1. если в аргуметне есть ссылка на дополнительый known_packages.json (на файл или URL), то перезаписываем known_packages в соответствии с ним
2. Проверяем список доступных менеджеров
3. проверяем установвлен ли в них паект (в соответствии с коныигом, но не обязательно только с ним... [аргумент --only-known-packages])
4. Определяем PM 
   1. если их несколько, то даём пользователю выбрать несеолько из них, или все
5. Удаляем

### mpm reinstall [package_name]
1.  mpm remove [package_name]
2.  mpm install [package_name]

### mpm update [package_name]
1. Подготовка known_packages
   1. если в аргуметне есть ссылка на дополнительый known_packages.json (на файл или URL), то перезаписываем known_packages в соответствии с ним
2. Проверяем список доступных менеджеров
3. проверяем установвлен ли в них паект (в соответствии с коныигом, но не обязательно только с ним... [аргумент --only-known-packages])
4. Определяем PM 
5. Обновляем в соответсвии с конфигом, или везде и всюду

### mpm show [package_name] [+]
1. Подготовка known_packages
   1. если в аргуметне есть ссылка на дополнительый known_packages.json (на файл или URL), то перезаписываем known_packages в соответствии с ним
2. Проверяем список доступных менеджеров (в соответствии с коныигом, но не обязательно только с ним... [аргумент --only-known-packages])
3. Выводим всю инфу... # TODO: красиво!

### mpm list 
1. Подготовка known_packages
   1. если в аргуметне есть ссылка на дополнительый known_packages.json (на файл или URL), то перезаписываем known_packages в соответствии с ним
2. по умолчанию выводит список всех установленных пакетов (из known_packages) их версии, способ установки, и список плагинов
3. всё настраивается 
4. можно экспортировать 

### mpm search []
хз
