import json
import time

import pytest
import requests
from docker.models.containers import Container
from docker.models.images import Image

from build.constants import TARGET_ARCHITECTURES
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import (
    TEST_CONTAINER_NAME,
    SLEEP_TIME,
    HELLO_WORLD,
    DEVELOPMENT_GUNICORN_CONFIG,
)
from tests.utils import UvicornGunicornPoetryContainerConfig


def verify_container(container: UvicornGunicornPoetryContainerConfig) -> None:
    response = requests.get("http://127.0.0.1:8000")
    assert json.loads(response.text) == HELLO_WORLD

    config_data = container.get_config()
    assert config_data["bind"] == DEVELOPMENT_GUNICORN_CONFIG["bind"]
    assert config_data["workers"] == DEVELOPMENT_GUNICORN_CONFIG["workers"]
    assert config_data["timeout"] == DEVELOPMENT_GUNICORN_CONFIG["timeout"]
    assert (
        config_data["graceful_timeout"]
        == DEVELOPMENT_GUNICORN_CONFIG["graceful_timeout"]
    )
    assert config_data["keepalive"] == DEVELOPMENT_GUNICORN_CONFIG["keepalive"]
    assert config_data["loglevel"] == DEVELOPMENT_GUNICORN_CONFIG["loglevel"]
    assert config_data["accesslog"] == DEVELOPMENT_GUNICORN_CONFIG["accesslog"]
    assert config_data["errorlog"] == DEVELOPMENT_GUNICORN_CONFIG["errorlog"]
    assert config_data["reload"] == DEVELOPMENT_GUNICORN_CONFIG["reload"]
    assert (
        config_data["worker_tmp_dir"]
        == DEVELOPMENT_GUNICORN_CONFIG["worker_tmp_dir"]
    )


@pytest.mark.parametrize("target_architecture", TARGET_ARCHITECTURES)
def test_default_configuration(docker_client, target_architecture) -> None:
    UvicornGunicornPoetryImage(docker_client).build(target_architecture)
    test_image: Image = FastApiMultistageImage(docker_client).build(
        target_architecture, "development-image"
    )

    test_container: Container = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={"80": "8000"},
        detach=True,
    )
    uvicorn_gunicorn_container: UvicornGunicornPoetryContainerConfig = (
        UvicornGunicornPoetryContainerConfig(test_container)
    )
    time.sleep(SLEEP_TIME)
    verify_container(uvicorn_gunicorn_container)
    test_container.stop()

    # Test restarting the container
    test_container.start()
    time.sleep(SLEEP_TIME)
    verify_container(uvicorn_gunicorn_container)
