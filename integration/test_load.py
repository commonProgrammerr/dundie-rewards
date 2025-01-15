import pytest
from subprocess import check_output


@pytest.mark.integration
def test_load():
    """Test that the load command works."""
    outpupt = (
        check_output(["dundie", "load", "tests/assets/people.csv"])
        .decode("utf-8")
        .splitlines()
    )

    assert len(outpupt) == 2
