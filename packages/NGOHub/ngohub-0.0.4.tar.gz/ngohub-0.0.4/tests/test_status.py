import pytest

from ngohub.core import NGOHub
from tests.schemas import VERSION_REVISION_SCHEMA


def test_health_returns_ok():
    hub = NGOHub(pytest.ngohub_api_url)
    assert hub.is_healthy()


def test_version_returns_version_revision():
    hub = NGOHub(pytest.ngohub_api_url)
    response = hub.get_version()

    assert VERSION_REVISION_SCHEMA.validate(response)


def test_file_returns_path():
    hub = NGOHub(pytest.ngohub_api_url)
    file_path = "test.txt"
    response = hub.get_file_url(file_path)

    assert f"amazonaws.com/{file_path}?AWSAccessKeyId=" in response
