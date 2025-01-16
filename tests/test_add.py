import pytest
from dundie.database import add_person, commit, connect
from dundie import core


@pytest.mark.unit
def test_movement():
    pk = "joe@doe.com"
    data = {"role": "salesman", "dept": "Sales", "name": "Joe Doe"}
    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True

    pk = "jim@doe.com"
    data = {"role": "Manager", "dept": "Management", "name": "Jim Doe"}
    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)

    core.add(-30, email="joe@doe.com")
    core.add(90, dept="Management")

    db = connect()

    assert db["balance"]["joe@doe.com"] == 470
    assert db["balance"]["jim@doe.com"] == 190
