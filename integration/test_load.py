from click.testing import CliRunner
from dundie.cli import main, load
from tests.constants import PEOPLE_FILE
import pytest

cmd = CliRunner()


@pytest.mark.integration
def test_load_positive_call_load_command():
    """Test that the load command works."""
    out = cmd.invoke(load, PEOPLE_FILE)

    table_title = "Dundie Miffin Associates"

    assert table_title in out.output


@pytest.mark.integration
@pytest.mark.parametrize("wrong_command", ["loady", "start", "carrega"])
def test_load_negative_call_load_command_with_wrong_params(wrong_command):
    """Test command load."""

    out = cmd.invoke(main, wrong_command, PEOPLE_FILE)

    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output
