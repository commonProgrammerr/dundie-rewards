import pytest
from dundie.utils.email import check_valid_email

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
@pytest.mark.parametrize("email", valid_emails.splitlines())
def test_positive_check_valid_email(email):
    """Ensure that check_valid_email returns True for valid emails"""
    assert check_valid_email(email) is True


@pytest.mark.unit
@pytest.mark.parametrize("email", invalid_emails.splitlines())
def test_negative_check_valid_email(email):
    """Ensure that check_valid_email returns True for valid emails"""
    assert check_valid_email(email) is False
