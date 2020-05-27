import click
import sys

from mpm.pm import NAMES_TO_PACKAGE_MANAGERS, PACKAGE_MANAGERS_NAMES
from mpm.core.logging import getLogger

logger = getLogger(__name__)

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
    logger.debug(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.info(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.warn(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.success(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.error(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.critical(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    click.echo('0000')


@main.command()
@click.argument('package_name')
@click.option('-pm', '--package-manager',
              'pm_name',
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def show(package_name, pm_name):
    '''
    Показать дополнительные данные о пакете
    '''
    logger.debug(f"package_name = {package_name}, pm_name = {pm_name}")
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
    logger.debug(f"package_name = {package_name}, pm_name = {pm_name}")
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
    logger.debug(f"package_name = {package_name}, pm_name = {pm_name}")
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
    logger.debug(f"package_name = {package_name}, pm_name = {pm_name}")
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
    logger.debug(f"package_name = {package_name}, pm_name = {pm_name}")
    click.echo('Syncing')

@main.command(name='list')
@click.option('-pm', '--package-manager',
              'pm_name',
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def list_command(pm_name):
    '''
    Список пакетов
    '''
    logger.debug(f"pm_name = {pm_name}")
    click.echo('Syncing')

if __name__ == "__main__":
    main()
