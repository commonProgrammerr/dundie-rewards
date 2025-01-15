import pytest


@pytest.fixture(autouse=True)
def go_to_tmp_dir(request):
    tmpdir = request.getfixurevalue("tmpdir")
    with tmpdir.as_cwd():
        yield
