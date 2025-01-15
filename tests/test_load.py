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
def test_load():
    """Test load function."""
    assert len(load(PEOPLE_FILE)) == 2
    assert load(PEOPLE_FILE)[0][0] == "J"
