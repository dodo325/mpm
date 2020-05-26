# Ядро проекта



## Алгоритмы работы некоторых комманд:

### Подготовка known_packages
1. Парситим settings.json, перезаписываем его в соответствии с $HOME/.mpm/settings.json
2. Из known_packages_url получаем known_packages, если возникла ошибка, то смотрим локальный known_packages
3. перезаписываем known_packages в соответствии с $HOME/.mpm/known_packages.json
### mpm install [package_name]
