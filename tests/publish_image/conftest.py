import pytest
from click.testing import CliRunner
from docker.client import DockerClient

from build.constants import UVICORN_GUNICORN_POETRY_IMAGE_NAME


@pytest.fixture(scope="package")
def cli_runner() -> CliRunner:
    runner = CliRunner()
    return runner


@pytest.fixture(scope="package")
def cleanup_images(docker_client: DockerClient):
    yield
    for old_image in docker_client.images.list(
        UVICORN_GUNICORN_POETRY_IMAGE_NAME
    ):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)
