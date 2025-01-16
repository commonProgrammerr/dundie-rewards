import pytest
from dundie.database import EMPTY_DATABASE, add_movement, add_person, commit, connect


@pytest.mark.unit
def test_database_schema():
    db = connect()
    assert db.keys() == EMPTY_DATABASE.keys()


@pytest.mark.unit
def test_commit_to_database():
    db = connect()
    new_user = {
        "name": "Michael Scott",
        "role": "manager",
        "dept": "sales",
    }

    db["people"]["michael@dundie.com"] = new_user
    commit(db)

    db = connect()

    assert db["people"]["michael@dundie.com"] == new_user


@pytest.mark.unit
def test_add_person_for_the_first_time():
    pk = "joe@doe.com"
    data = {"role": "salesman", "dept": "sales", "name": "Joe Doe"}
    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)

    db = connect()
    assert db["people"][pk] == data
    assert db["balance"][pk] == 500
    user_movements = db["movement"][pk]
    assert len(user_movements) > 0
    assert user_movements[0]["value"] == 500


@pytest.mark.unit
def test_negative_add_person_invalid_email():
    with pytest.raises(ValueError):
        add_person(connect(), "joe", {})


@pytest.mark.unit
def test_add_or_remove_point_for_person():
    pk = "joe@doe.com"
    data = {"role": "salesman", "dept": "sales", "name": "Joe Doe"}
    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)

    db = connect()
    before = db["balance"][pk]
    add_movement(db, pk, -100, "manager")
    commit(db)

    db = connect()
    after = db["balance"][pk]

    assert after == before - 100
    assert after == 400
    assert before == 500
