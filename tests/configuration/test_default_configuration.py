import json
from time import sleep
from uuid import uuid4

import pytest
import requests
from docker.models.containers import Container

from build.constants import APPLICATION_SERVER_PORT
from build.gunicorn_configuration import DEFAULT_GUNICORN_CONFIG
from tests.constants import SLEEP_TIME, HELLO_WORLD, EXPOSED_CONTAINER_PORT
from tests.utils import UvicornGunicornPoetryContainerConfig


def verify_container_config(
    container: UvicornGunicornPoetryContainerConfig,
) -> None:
    response = requests.get(f"http://127.0.0.1:{EXPOSED_CONTAINER_PORT}")
    assert json.loads(response.text) == HELLO_WORLD

    config_data = container.get_config()
    assert config_data["bind"] == DEFAULT_GUNICORN_CONFIG["bind"]
    assert config_data["workers"] == DEFAULT_GUNICORN_CONFIG["workers"]
    assert config_data["timeout"] == DEFAULT_GUNICORN_CONFIG["timeout"]
    assert (
        config_data["graceful_timeout"]
        == DEFAULT_GUNICORN_CONFIG["graceful_timeout"]
    )
    assert config_data["keepalive"] == DEFAULT_GUNICORN_CONFIG["keepalive"]
    assert config_data["loglevel"] == DEFAULT_GUNICORN_CONFIG["loglevel"]
    assert config_data["accesslog"] == DEFAULT_GUNICORN_CONFIG["accesslog"]
    assert config_data["errorlog"] == DEFAULT_GUNICORN_CONFIG["errorlog"]
    #   assert config_data["reload"] == DEFAULT_GUNICORN_CONFIG["reload"]
    assert (
        config_data["worker_tmp_dir"]
        == DEFAULT_GUNICORN_CONFIG["worker_tmp_dir"]
    )


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_multistage_stage_image(
    docker_client,
    fast_api_multistage_production_image,
    cleaned_up_test_container,
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_multistage_production_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
        detach=True,
    )
    uvicorn_gunicorn_container: UvicornGunicornPoetryContainerConfig = (
        UvicornGunicornPoetryContainerConfig(test_container)
    )
    sleep(SLEEP_TIME)
    verify_container_config(uvicorn_gunicorn_container)
    test_container.stop()

    # Test restarting the container
    test_container.start()
    sleep(SLEEP_TIME)
    verify_container_config(uvicorn_gunicorn_container)


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_single_stage_image(
    docker_client,
    fast_api_singlestage_image,
    cleaned_up_test_container,
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_singlestage_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
        detach=True,
    )
    uvicorn_gunicorn_container_config: UvicornGunicornPoetryContainerConfig = (
        UvicornGunicornPoetryContainerConfig(test_container)
    )
    sleep(SLEEP_TIME)
    verify_container_config(uvicorn_gunicorn_container_config)
    test_container.stop()

    # Test restarting the container
    test_container.start()
    sleep(SLEEP_TIME)
    verify_container_config(uvicorn_gunicorn_container_config)
