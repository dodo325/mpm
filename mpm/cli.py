import click
import sys


@click.group()
def main():
    pass


@main.command()
def install():
    '''
    Установить пакет
    '''
    click.echo('Syncing')


@main.command()
def show():
    '''
    Показать дополнительные данные о пакете
    '''
    click.echo('Syncing')

# @main.command()
# def remove():
#     '''
#     Переустановить пакет
#     '''
#     click.echo('Syncing')


# @main.command()
# def reinstall():
#     '''
#     Переустановить пакет
#     '''
#     click.echo('Syncing')

# @main.command()
# def update():
#     '''
#     Обновить пакет
#     '''
#     click.echo('Syncing')

@main.command(name='list')
def list_command():
    '''
    Список пакетов
    '''
    click.echo('Syncing')

if __name__ == "__main__":
    main()
