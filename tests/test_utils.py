import pytest

from dundie.models import Person
from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_simple_password
from dundie.utils.db import gen_filter_query

# List of Valid Email Addresses
valid_emails = """\
email@example.com
firstname.lastname@example.com
email@subdomain.example.com
firstname+lastname@example.com
email@123.123.123.123
email@[123.123.123.123]
"email"@example.com
1234567890@example.com
email@example-one.com
_______@example.com
email@example.name
email@example.museum
email@example.co.jp
firstname-lastname@example.com"""

# List of Invalid Email Addresses
invalid_emails = """\
plainaddress
#@%^%#$@#$@#.com
@example.com
Joe Smith <email@example.com>
email@example.com (Joe Smith)
email.example.com
email@example@example.com
.email@example.com
email.@example.com
email..email@example.com
あいうえお@example.com
email@example
email@-example.com
email@example..com
Abc..123@example.com"""


@pytest.mark.unit
@pytest.mark.no_test_db
@pytest.mark.parametrize("email", valid_emails.splitlines())
def test_positive_check_valid_email(email: str):
    """Ensure that check_valid_email returns True for valid emails"""
    assert check_valid_email(email) is True


@pytest.mark.unit
@pytest.mark.no_test_db
@pytest.mark.parametrize("email", invalid_emails.splitlines())
def test_negative_check_valid_email(email: str):
    """Ensure that check_valid_email returns True for valid emails"""
    assert check_valid_email(email) is False


@pytest.mark.unit
@pytest.mark.no_test_db
def test_generate_simple_password():
    """Test generation of random simple passwords.

    TODO: Generate hashed complex and encrypted passwords
    """
    passwords = []

    for _ in range(100):
        passwords.append(generate_simple_password())

    assert len(set(passwords)) == len(passwords)


EMAIL_FILTER_QUERY = (
    "SELECT person.id, person.email, person.name, person.dept, person.role \n"
    "FROM person \n"
    "WHERE person.email = :email_1"
)
NAME_FILTER_QUERY = (
    "SELECT person.id, person.email, person.name, person.dept, person.role \n"
    "FROM person \n"
    "WHERE person.name = :name_1"
)
DEPT_FILTER_QUERY = (
    "SELECT person.id, person.email, person.name, person.dept, person.role \n"
    "FROM person \n"
    "WHERE person.dept = :dept_1"
)
ROLE_FILTER_QUERY = (
    "SELECT person.id, person.email, person.name, person.dept, person.role \n"
    "FROM person \n"
    "WHERE person.role = :role_1"
)


@pytest.mark.unit
@pytest.mark.no_test_db
def test_positive_generate_filter_SQL_query_from_filter_dict():
    """Test generation of SQL query from filter dictionary"""

    assert (
        str(gen_filter_query(Person, **{"email": "text"}))
        == EMAIL_FILTER_QUERY
    )
    assert (
        str(gen_filter_query(Person, **{"name": "text"})) == NAME_FILTER_QUERY
    )
    assert (
        str(gen_filter_query(Person, **{"dept": "text"})) == DEPT_FILTER_QUERY
    )
    assert (
        str(gen_filter_query(Person, **{"role": "text"})) == ROLE_FILTER_QUERY
    )


@pytest.mark.no_test_db
@pytest.mark.unit
def test_negative_generate_filter_SQL_query_from_filter_dict():
    with pytest.raises(KeyError):
        gen_filter_query(Person, **{"password": "text"})
