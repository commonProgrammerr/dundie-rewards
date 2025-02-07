from typing import Any, Dict, Optional

from sqlmodel import Session, select

from dundie.models import Balance, Movement, Person, User
from dundie.settings import EMAIL_FROM
from dundie.utils.email import send_email


def add_person(session: Session, instance: Person):
    """Saves person data to database

    - Email is unique
    - If exists, update, else create
    - Set initial balance  (managers = 100, others = 500)
    """

    existing = session.exec(select(Person).where(Person.email == instance.email)).first()
    created = existing is None

    if created:
        session.add(instance)
        set_initial_balance(session, instance)
        password = set_initial_password(session, instance)
        send_email(EMAIL_FROM, instance.email, "Your dundie Your password", password)
        return instance, created
    else:
        existing.dept = instance.dept
        existing.role = instance.role
        existing.currency = instance.currency
        session.add(existing)
        return existing, created


def set_initial_password(session: Session, person: Person):
    """Set initial password for user and return it."""

    user = User(person=person)
    session.add(user)
    return user.password


def set_initial_balance(session: Session, person: Person):
    """Set initial balance for user."""
    value = 100 if "manager" in str.lower(person.role) else 500
    add_movement(session, person, value)


def add_movement(
    session: Session,
    person: Person,
    value: int,
    actor: Optional[str] = "system",
):
    """Adds movement to user account.

    Example::

        add_movement(db, Person(...), 100, "me")

    """
    movement = Movement(person=person, value=value, actor=actor)
    session.add(movement)

    movements = session.exec(select(Movement).where(Movement.person == person))

    total = sum([mov.value for mov in movements])

    existing_balance = session.exec(select(Balance).where(Balance.person == person)).first()
    if existing_balance:
        existing_balance.value = total
        session.add(existing_balance)
    else:
        session.add(Balance(person=person, value=total))


def gen_filter_query(cls, **query: Dict[str, Any]):
    """Get filter query for db."""
    query_statements = []
    for key, value in query.items():
        if value is None:
            continue
        if key not in cls.__annotations__:
            raise KeyError(f"{key} is not a valid key for {cls}")
        else:
            query_statements.append(cls.__dict__[key] == value)

    sql = select(cls)  # SELECT FROM PERSON
    if query_statements:
        sql = sql.where(*query_statements)  # WHERE ...

    return sql
