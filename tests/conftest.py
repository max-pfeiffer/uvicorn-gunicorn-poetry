import pytest
import docker
from docker.errors import NotFound

from tests.constants import TEST_CONTAINER_NAME


@pytest.fixture(scope="module")
def docker_client() -> docker.client:
    return docker.client.from_env()


@pytest.fixture(autouse=True)
def prepare_docker_env(docker_client) -> None:
    try:
        old_container = docker_client.containers.get(TEST_CONTAINER_NAME)
        old_container.stop()
        old_container.remove()
    except NotFound:
        pass
    yield None
    try:
        old_container = docker_client.containers.get(TEST_CONTAINER_NAME)
        old_container.stop()
        old_container.remove()
    except NotFound:
        pass
