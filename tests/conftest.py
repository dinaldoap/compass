import pytest
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    dir = tempfile.mkdtemp()
    yield dir
    shutil.rmtree(dir)
