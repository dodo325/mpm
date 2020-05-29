import click
import sys
import json
from mpm.pm import UniversalePackage, NAMES_TO_PACKAGE_MANAGERS, PACKAGE_MANAGERS_NAMES, get_installed_pms
from mpm.core.logging import getLogger
from mpm.shell import AutoShell
from mpm.core.configs import get_known_packages
logger = getLogger(__name__)

@click.group()
def main():
    pass


@main.command()
@click.argument('package_name')
@click.option("-ok", "--only-known-packages", is_flag=True, help="Use packages only from known_packages.json")
@click.option('-pm', '--package-manager', 
    'pm_name', 
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))
def install(package_name, pm_name, only_known_packages):  # install kit
    '''
    Установить пакет
    '''

    click.echo('0000')


@main.command()
@click.argument('package_name')
@click.option("-a", "--all", "all_flag",is_flag=True, help="")
@click.option("-of", "--offline", "offline", is_flag=True, help="Search for information not only in the known_packages")
@click.option("-k", "--known-packages-json", help="known_packages.json file") # TODO: parse URL
@click.option('-pm', '--package-manager',
              'pm_names', multiple=True,
              type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False))  # Возможен мультивызов, например: -pm apt -pm pip
def show(package_name, pm_names, known_packages_json, all_flag, offline):
    '''
    Показать дополнительные данные о пакете
    ''' 
    logger.debug(
        f"Args:\n\tpackage_name = {package_name},\n\tpm_names = {pm_names}\n\tall = {all_flag}\n\toffline = {offline}")
    known_packages = get_known_packages(offline=offline)
    if known_packages_json:
        known_packages.update(json.load(known_packages_json))

    shell = AutoShell()
    PMs = get_installed_pms(shell=shell)
    if len(pm_names) > 0:
        pm_fliter = lambda PM: PM.name in pm_names
        PMs = list(filter(pm_fliter, PMs))
        logger.debug(f"PMs after filtering: {PMs}")

    package = UniversalePackage(
            package_name, 
            shell=shell,
            PMs=PMs
        )

    logger.info(f"Search '{package_name}' in installed Packege Managers")
    info = package.get_info(all_pm=all_flag)
    if info == {}:
        logger.error("Package Does Not Found")
        return
    
    for pm_name, data in info.items():
        click.echo(f"\t{pm_name}:", color='green')
        for key, val in data.items():
            click.echo(f"- {key}: {val}", color='green')


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
    logger.debug(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.info(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.warn(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.success(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.error(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.critical(f"package_name = {package_name}\n\tpm_name = {pm_name}")

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
