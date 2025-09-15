import click

from toolfront.models.database import Database, Query, Table


@click.group()
def database() -> None:
    """Database commands"""
    pass


@database.command()
@click.argument("url", type=click.STRING, required=True)
@click.option("--csv", is_flag=True, help="Output as csv.")
def list_tables(url, csv) -> None:
    db = Database(url)

    data = db.tables
    if csv:
        click.echo(data.to_csv(index=False))
    else:
        click.echo(data.to_markdown(index=False))


@database.command()
@click.argument("url", type=click.STRING, required=True)
@click.argument("path", type=click.STRING, required=True)
@click.option("--csv", is_flag=True, help="Output as csv.")
def inspect_table(url, path, csv) -> None:
    db = Database(url)
    data = db.inspect_table(Table(path=path))
    if csv:
        click.echo(data.to_csv(index=False))
    else:
        click.echo(data.to_markdown(index=False))


@database.command()
@click.argument("url", type=click.STRING, required=True)
@click.argument("code", type=click.STRING, required=True)
@click.option("--csv", is_flag=True, help="Output as csv.")
def query(url, code, csv) -> None:
    db = Database(url)
    data = db.query(Query(code=code))
    if csv:
        click.echo(data.to_csv(index=False))
    else:
        click.echo(data.to_markdown(index=False))
