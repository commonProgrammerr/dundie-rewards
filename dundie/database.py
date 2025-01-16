import json
from datetime import datetime
from dundie.settings import DATABASE_PATH, EMAIL_FROM
from dundie.utils.email import check_valid_email, send_email
from dundie.utils.log import get_logger
from dundie.utils.user import generate_simple_password


EMPTY_DATABASE = {"people": {}, "balance": {}, "movement": {}, "users": {}}

log = get_logger()


def connect():
    """Connect to the database. Returns the database object."""
    try:
        with open(DATABASE_PATH, "r") as database_file:
            return json.load(database_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return EMPTY_DATABASE


def commit(db):
    """Commit the database to disk."""

    try:
        with open(DATABASE_PATH, "w") as database_file:
            json.dump(db, database_file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        log.error("Error writing database to disk")


def add_person(db, pk, data) -> tuple[dict, bool]:
    """Saves person data to database

    - Email is unique
    - If exists, update, else create
    - Set initial balance  (managers = 100, others = 500)
    """

    if not check_valid_email(pk):
        raise ValueError("Invalid email address '{pk}'")

    table = db["people"]
    person = table.get(pk, {})
    created = not bool(person)
    person.update(data)
    table[pk] = person
    if created:
        set_initial_balance(db, pk, person)
        password = set_initial_password(db, pk)
        send_email(EMAIL_FROM, pk, "Your dundie Your password", password)
        # TODO: encrypt and send only link, not password.

    return person, created


def set_initial_password(db, pk):
    db["users"].setdefault(pk, {})
    db["users"][pk]["password"] = generate_simple_password()
    return db["users"][pk]["password"]


def set_initial_balance(db, pk, person):
    value = 100 if "manager" in str.lower(person["role"]) else 500
    add_movement(db, pk, value)


def add_movement(db: dict, pk: str, value: int | float, actor="system"):
    movements = db["movement"].setdefault(pk, [])
    movements.append(
        {"date": datetime.now().isoformat(), "value": value, "actor": actor}
    )
    db["balance"][pk] = sum([mov["value"] for mov in movements])
