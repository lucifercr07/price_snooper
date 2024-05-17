import click
from commands.watch_product import watch_product


@click.group()
def snooper():
    """:) Price Snooper :)"""


if __name__ == '__main__':
    snooper.add_command(watch_product)
    snooper()
