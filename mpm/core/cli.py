import click
import sys

from mpm.pm import NAMES_TO_PACKAGE_MANAGERS, PACKAGE_MANAGERS_NAMES

@click.group()
def main():
    pass


@main.command()
@click.argument('package_name')
@click.option('-pm', '--package-manager', 
    'pm_name', 
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def install(package_name, pm_name):  # install kit
    '''
    Установить пакет
    '''
    click.echo('Syncing')


@main.command()
@click.argument('package_name')
@click.option('-pm', '--package-manager',
              'pm_name',
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def show(package_name, pm_name):
    '''
    Показать дополнительные данные о пакете
    '''
    click.echo('Syncing')

@main.command()
@click.argument('package_name')
@click.option('-pm', '--package-manager',
              'pm_name',
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def remove(package_name, pm_name):
    '''
    Удалить пакет
    '''
    click.echo('Syncing')


@main.command()
@click.argument('package_name')
@click.option('-pm', '--package-manager',
              'pm_name',
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def search(package_name, pm_name):
    '''
    Найти пакет
    '''
    click.echo('Syncing')

@main.command()
@click.argument('package_name')
@click.option('-pm', '--package-manager',
              'pm_name',
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def reinstall(package_name, pm_name):
    '''
    Переустановить пакет
    '''
    click.echo('Syncing')

@main.command()
@click.argument('package_name')
@click.option('-pm', '--package-manager',
              'pm_name',
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def update(package_name, pm_name):
    '''
    Обновить пакет
    '''
    click.echo('Syncing')

@main.command(name='list')
@click.option('-pm', '--package-manager',
              'pm_name',
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def list_command(pm_name):
    '''
    Список пакетов
    '''
    click.echo('Syncing')

if __name__ == "__main__":
    main()
