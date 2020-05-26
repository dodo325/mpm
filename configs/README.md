
## known_packages.json
Это список всех известных пакетов.

### TODO:
* автоматически пополнятся в $HOME/.mpm/known_packages.json
* начала смотреть в [GitHub Raw](https://raw.githubusercontent.com/dodo325/mpm/master/configs/known_packages.json), а потом в локальный файл
* 


### Структура:


### Универсальный пример:
```json
"[package_name]": {
    "package_managers":{
        "[package_manager_name]": {
            "package_name": "[package_name]",
            "install":{
                    "args": ["[arg1]", "[arg2]", "[...]"]
            }
        },
        "script":{
            "file": "[path_to_script]",
            "install": {
                "directory": "[dir]"
            }
        }
    },
    "plugins": {
        "[plugin_name]":{
            "plugin_name" : "[plugin_name]",
            "plugin_id": "[plugin_id]",
            "install":{
                "args": ["[arg1]", "[arg2]", "[...]"]
            }
        }
    },
    "plugins_install": {
        "[package_manager_name]": {
            "template_package_name": "[template_package_name]"
        },
        "shell": {
            "template_cmd": "[template_cmd]",
            "get_all": {
                "cmd": "[cmd]",
                "parser": {
                    "new_line": "\n",
                    "remove_blank": true,
                    "re_inline": "[regex]"
                }
            }
        }
    },
    "requirements":{
            "DE": {
                "{DE_name}":{

                }
            },
            "platform": {

            }
    },
    "dependence":[
        "package1"
    ]
}
```
* template_package_name
  * Например: "remmina-plugin-{plugin_name}"
* path_to_script - это 
  * url на скрипт 
  * path to file (абсолютный путь)
  * scripts/{file} - путь начинающийся с "scripts"
    Ищет скрипты в папке пакета или $HOME/.mpm/scripts/
     
### Примеры:
```json
"django": {
    "package_managers":{"pip":{}},
    "plugins": {
        "guardian":{},
        "extensions":{},
        "cors-headers":{}
    },
    "plugins_install": {
        "pip": {
            "template_package_name": "django-{plugin_name}"
        }
    }
}
```

```json
"qbittorrent": {
    "package_managers":{
        "apt":{}
    }
},
```

```json
"vscode": {
    "package_managers":{
        "snap":{
            "package_name": "code",
            "install":{
                "args": ["--classi"]
            }
        }
    },
    "plugins": {
        "rogalmic.bash-debug":{},
        "robbowen.synthwave-vscode ":{}
    },
    "plugins_install": {
        "shell": {
            "template_cmd": "code --install-extension {plugin_name}",
            "get_all": {
                "cmd": "code --list-extensions",
                "parser": {
                    "new_line": "\n",
                    "remove_blank": true
                }
            }
        }
    },
    "requirements":{
        "DE":{}
    },
}
```

```json
    "gnome-shell-extension-installer": {
        "package_managers":{
            "script":{
                "file": "https://github.com/brunelli/gnome-shell-extension-installer/raw/master/gnome-shell-extension-installer",
                "script_name": "gnome-shell-extension-installer",
                "install": {
                    "directory": "/usr/bin/"
                }
            }
        },
        "plugins": {
            "arc-men": {"plugin_id": 1228},
            "dash-to-panel": {"plugin_id": 1160}
        },
        "plugins_install": {
            "shell": {
                "template_cmd": "{package_name} {plugin_id} --yes",
                "get_all": {
                    "cmd": "ls /usr/share/gnome-shell/extensions/ -1; ls $HOME/.local/share/gnome-shell/extensions -1",
                    "parser": {
                        "new_line": "\n",
                        "remove_blank": true,
                        "re_inline": "^.+(?=@)"
                }
            }
        },
        "requirements":{
            "DE": {
                "GNOME":{}
            }
        }
    },
```