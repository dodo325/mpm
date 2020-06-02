# Shell
Обёртка над командными оболосками системы

## get_installed_shells
Return all installed shells

Example:
```python
>>> get_installed_shells()
[mpm.shell.shells.ZSH, mpm.shell.shells.Bash]
```
## AutoShell
Returns one of the installed shells. Or by 'name'

Example:
```python
>>> AutoShell()
<mpm.shell.shells.ZSH at 0x7f5d3dcb9e90>

>>> AutoShell('bash')
<mpm.shell.shells.Bash at 0x7f5d3ddcc910>
```