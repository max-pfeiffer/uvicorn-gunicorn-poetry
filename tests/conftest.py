import pytest
import docker
from docker.errors import NotFound

from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME


@pytest.fixture(scope="module")
def docker_client() -> docker.client:
    return docker.client.from_env()


@pytest.fixture(autouse=True)
def prepare_docker_env(docker_client) -> None:
    # Remove old container
    try:
        old_container = docker_client.containers.get(TEST_CONTAINER_NAME)
        old_container.stop()
        old_container.remove()
    except NotFound:
        pass
    # Delete old existing images
    uvicorn_gunicorn_poetry_image: UvicornGunicornPoetryImage = (
        UvicornGunicornPoetryImage(docker_client)
    )
    for old_image in docker_client.images.list(
            uvicorn_gunicorn_poetry_image.image_name
    ):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
    fast_api_multistage_image: FastApiMultistageImage = (
        FastApiMultistageImage(docker_client)
    )
    for old_image in docker_client.images.list(
            fast_api_multistage_image.image_name
    ):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)

    yield None

    # Remove old container
    try:
        old_container = docker_client.containers.get(TEST_CONTAINER_NAME)
        old_container.stop()
        old_container.remove()
    except NotFound:
        pass
    # Delete old existing images
    uvicorn_gunicorn_poetry_image: UvicornGunicornPoetryImage = (
        UvicornGunicornPoetryImage(docker_client)
    )
    for old_image in docker_client.images.list(
            uvicorn_gunicorn_poetry_image.image_name
    ):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
    fast_api_multistage_image: FastApiMultistageImage = (
        FastApiMultistageImage(docker_client)
    )
    for old_image in docker_client.images.list(
            fast_api_multistage_image.image_name
    ):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
