import pytest

from dundie.core import read
from dundie.database import get_session
from dundie.utils.db import add_person
from dundie.models import Person


@pytest.mark.unit
def test_read_with_query():
    with get_session() as session:
        person = Person(
            email="joe@doe.com", role="salesman", dept="Sales", name="Joe Doe"
        )
        _, created = add_person(session, person)
        assert created is True

        person = Person(
            email="jim@doe.com",
            role="salesman",
            dept="Management",
            name="Jim Doe",
        )
        _, created = add_person(session, person)
        assert created is True

        session.commit()

    response = read(dept="Management")
    assert len(response) == 1
    assert response[0]["name"] == "Jim Doe"

    response = read(email="joe@doe.com")
    assert len(response) == 1
    assert response[0]["name"] == "Joe Doe"
