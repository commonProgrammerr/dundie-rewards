""" Command Line Interface for Dundie Mifflin Rewards """

import json

import pkg_resources
import rich_click as click
from rich.console import Console
from rich.table import Table

from dundie import core

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()
@click.version_option(pkg_resources.get_distribution("dundie").version)
def main():
    """Dundie Mifflin Rewards CLI.

    Enjoy and use with caution
    """


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
def load(filepath):
    """Loads CSV or JSON file data to the database."""
    header = ["name", "dept", "role", "created", "e-mail"]
    table = Table(title="Dundie Miffin Associates")

    for header in header:
        table.add_column(header)

    for person in core.load(filepath):
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)


@main.command()
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.option("--output", default=None)
def show(output, **query):
    """Shows information about users"""
    result = core.read(**query)

    if output:
        with open(output, "w") as output_file:
            json.dump(result, output_file, indent=4)

    if not result:
        print("Noting to show")
        return

    table = Table(title="Dundie Miffin Report")
    for key in result[0].keys():
        table.add_column(str(key).title(), style="magenta")

    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.pass_context
def add(ctx, value, **query):
    """Add points to a user or department"""

    core.add(value, **query)
    ctx.invoke(show, **query)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.pass_context
def remove(ctx, value, **query):
    """Add points to a user or department"""

    core.add(-value, **query)
    ctx.invoke(show, **query)
