import pytest

from dundie.core import load

from .constants import PEOPLE_FILE


def setup_module():
    # executed before module's tests are run
    pass


def teardown_module():
    # executed after module's tests are run
    pass


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_3_people():
    """Test load function."""
    assert len(load(PEOPLE_FILE)) == 3


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_name_is_jim():
    """Test load function."""
    assert load(PEOPLE_FILE)[0]["name"] == "Jim Halpert"
