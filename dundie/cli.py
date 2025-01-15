""" Command Line Interface for Dundie Mifflin Rewards """

import argparse
from dundie.core import load  # noqa


def main():
    parser = argparse.ArgumentParser(
        description="Dundie Mifflin Rewards CLI",
        epilog="Enjoy and use with caution",
    )

    parser.add_argument(
        "subcommand",
        type=str,
        help="Subcommand to execute",
        choices=("load", "send", "show"),
    )

    parser.add_argument(
        "filepath", type=str, help="Path to the file to load", default=None
    )

    args = parser.parse_args()
    print(*globals()[args.subcommand](args.filepath))
