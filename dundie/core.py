""" Core module for dundie package """

import os
from csv import reader

from dundie.utils.log import get_logger
from dundie.database import add_movement, connect, commit, add_person

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


def read(**query) -> list[dict]:
    """Read data from db and filters using queries."""
    db = connect()
    return_data = []
    for pk, data in db["people"].items():
        dept = query.get("dept")
        if dept and dept != data["dept"]:
            continue

        # WALRUS / Assignment Expression - a partir do python 3.8
        if (email := query.get("email")) and email != pk:
            continue

        return_data.append(
            {
                "email": pk,
                "balance": db["balance"][pk],
                "last_movement": db["movement"][pk][-1]["date"],
                **data,
            }
        )
    return return_data


def add(value, **query):
    """Add value to each record on query."""
    people = read(**query)

    if not people:
        raise RuntimeError("Not Found")

    db = connect()
    user = os.getenv("USER")
    for person in people:
        add_movement(db, person["email"], value, user)
    commit(db)
