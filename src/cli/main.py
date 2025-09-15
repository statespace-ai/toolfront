import click

from .commands.browser import browser
from .commands.database import database
from .commands.document import document
from .commands.site import site


@click.group()
def cli():
    """ToolFront CLI"""
    pass


cli.add_command(browser)
cli.add_command(database)
cli.add_command(document)
cli.add_command(site)

if __name__ == "__main__":
    cli()
