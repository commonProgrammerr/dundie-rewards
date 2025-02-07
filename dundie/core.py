"""Core module for dundie package"""

from csv import reader
from typing import Any, Dict, List

from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person
from dundie.settings import DATEFMT
from dundie.utils.auth import requires_auth
from dundie.utils.db import add_movement, add_person, gen_filter_query
from dundie.utils.exchange import get_exchange_rate
from dundie.utils.log import get_logger

log = get_logger()
Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


def load(filepath: str) -> List[Person]:
    """Load a file from filepath and loads to the database."""
    try:
        csv_data = reader(open(filepath))
    except FileNotFoundError as e:
        log.error(str(e))
        raise e

    with get_session() as session:
        peoples = []
        headers = ["name", "dept", "role", "email", "currency"]
        for row in csv_data:
            person_data = dict(zip(headers, [str.strip(k) for k in row]))
            person = Person(**person_data)
            person, created = add_person(session, person)

            peoples.append(
                {
                    "name": person.name,
                    "dept": person.dept,
                    "role": person.role,
                    "created": created,
                    "email": person.email,
                    "currency": person.currency,
                }
            )

        session.commit()
        return peoples


def read(**query: Query) -> ResultDict:
    """Read data from db and filters using queries."""
    with get_session() as session:
        currencies = session.exec(select(Person.currency).distinct()).all()
        rates = get_exchange_rate([currency for currency in currencies])
        sql = gen_filter_query(Person, **query)

        return [
            (
                {
                    "email": person.email,
                    "balance": person.balance[0].value,
                    "last_movement": person.movement[-1].date.strftime(DATEFMT),
                    **person.dict(exclude={"id"}),
                    "value": (person.balance[0].value * rates[person.currency].value),
                }
            )
            for person in session.exec(sql)
        ]


@requires_auth
def add(value: int, from_person: Person, **query: Query):
    """Add value to each record on query."""
    sql = gen_filter_query(Person, **query)

    with get_session() as session:
        results = session.exec(sql).all()
        transfer_value = len(results) * value
        if not results:
            raise RuntimeError("No records found")
        elif transfer_value > from_person.balance[0].value:
            raise RuntimeError("Insufficient funds")

        for person in results:
            add_movement(session, person, value, from_person.email)

        person = session.exec(select(Person).where(Person.email == from_person.email)).first()
        add_movement(session, person, -transfer_value, from_person.email)

        session.commit()
