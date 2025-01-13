""" Core module for dundie package """

from dundie.utils.log import get_logger

log = get_logger()


def load(filepath):
    """Load a file from filepath and loads to the database."""
    try:
        with open(filepath) as file_:
            return file_.readlines()
    except FileNotFoundError as e:
        print(f"File not found {e}")
