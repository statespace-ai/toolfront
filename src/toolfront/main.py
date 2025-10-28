import click

from .cli.mcp import mcp
from .cli.serve import serve


@click.group()
def main():
    """ToolFront CLI"""
    pass


main.add_command(serve)
main.add_command(mcp)

if __name__ == "__main__":
    main()
