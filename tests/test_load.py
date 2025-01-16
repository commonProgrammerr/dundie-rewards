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
def test_load_positive_2_people():
    """Test load function."""
    assert len(load(PEOPLE_FILE)) == 2


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_name_starts_with_j():
    """Test load function."""
    assert load(PEOPLE_FILE)[0]["name"] == "Jin Halpert"
