import pytest
from dundie.database import add_person, commit, connect
from dundie.core import read


@pytest.mark.unit
def test_read_with_query():
    pk = "joe@doe.com"
    data = {"role": "salesman", "dept": "Sales", "name": "Joe Doe"}
    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)

    pk = "jim@doe.com"
    data = {"role": "salesman", "dept": "Management", "name": "Jim Doe"}
    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)

    response = read(dept="Management")
    assert len(response) == 1
    assert response[0]["name"] == "Jim Doe"

    response = read(email="joe@doe.com")
    assert len(response) == 1
    assert response[0]["name"] == "Joe Doe"
