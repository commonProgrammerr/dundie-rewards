""" Core module for dundie package """

from csv import reader
from dundie.utils.log import get_logger
from dundie.database import connect, commit, add_person

log = get_logger()


def load(filepath):
    """Load a file from filepath and loads to the database."""
    try:
        csv_data = reader(open(filepath))
    except FileNotFoundError as e:
        log.error(str(e))
        raise e

    db = connect()
    peoples = []
    headers = ["name", "dept", "role", "email"]
    for row in csv_data:
        person_data = dict(zip(headers, [str.strip(k) for k in row]))
        pk = person_data.pop("email")
        person, created = add_person(db, pk, person_data)

        return_data = person.copy()
        return_data["created"] = created
        return_data["email"] = pk
        peoples.append(return_data)

    commit(db)
    return peoples
