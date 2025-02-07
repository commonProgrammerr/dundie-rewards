import pytest
from sqlmodel import select

from dundie import core
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person


@pytest.mark.unit
def test_movement():
    with get_session() as session:
        p1, created = add_person(
            session,
            Person(
                email="joe@doe.com",
                role="salesman",
                dept="Sales",
                name="Joe Doe",
            ),
        )
        assert created is True

        p2, created = add_person(
            session,
            Person(
                email="jim@doe.com",
                role="Manager",
                dept="Management",
                name="Jim Doe",
            ),
        )
        assert created is True
        session.commit()

    core.add(-30, email="joe@doe.com")
    core.add(90, dept="Management")

    with get_session() as session:
        p1 = session.exec(select(Person).where(Person.email == "joe@doe.com")).first()
        p2 = session.exec(select(Person).where(Person.email == "jim@doe.com")).first()

        assert p1.balance[0].value == 470
        assert p2.balance[0].value == 190
