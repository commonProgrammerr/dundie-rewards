""" Command Line Interface for Dundie Mifflin Rewards """

import pkg_resources
import rich_click as click
from dundie import core
from rich.table import Table
from rich.console import Console

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
