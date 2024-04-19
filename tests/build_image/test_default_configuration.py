import json
from time import sleep

import requests
from python_on_whales import DockerClient

from build.constants import APPLICATION_SERVER_PORT
from build.gunicorn_configuration import DEFAULT_GUNICORN_CONFIG
from tests.constants import SLEEP_TIME, HELLO_WORLD, EXPOSED_CONTAINER_PORT
from tests.utils import UvicornGunicornPoetryContainerConfig


def verify_container_config(
    container_config: UvicornGunicornPoetryContainerConfig,
) -> None:
    response = requests.get(f"http://127.0.0.1:{EXPOSED_CONTAINER_PORT}")
    assert json.loads(response.text) == HELLO_WORLD

    config_data = container_config.get_config()
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
    assert (
        config_data["worker_tmp_dir"]
        == DEFAULT_GUNICORN_CONFIG["worker_tmp_dir"]
    )


def test_fast_api_singlestage_image(
    docker_client: DockerClient,
    fast_api_singlestage_image_reference: str,
) -> None:
    """Test default configuration for single stage image.

    :param docker_client:
    :param fast_api_singlestage_image_reference:
    :return:
    """
    with docker_client.container.run(
        fast_api_singlestage_image_reference,
        detach=True,
        publish=[(EXPOSED_CONTAINER_PORT, APPLICATION_SERVER_PORT)],
    ) as container:
        # Wait for uvicorn to come up
        sleep(SLEEP_TIME)

        uvicorn_gunicorn_container_config: (
            UvicornGunicornPoetryContainerConfig
        ) = UvicornGunicornPoetryContainerConfig(container.id)

        assert (
            f"{APPLICATION_SERVER_PORT}/tcp"
            in container.config.exposed_ports.keys()
        )

        verify_container_config(uvicorn_gunicorn_container_config)


def test_fast_api_multistage_image(
    docker_client: DockerClient,
    fast_api_multistage_image_reference: str,
) -> None:
    """Test default configuration for multi-stage image.

    :param docker_client:
    :param fast_api_multistage_image_reference:
    :return:
    """
    with docker_client.container.run(
        fast_api_multistage_image_reference,
        detach=True,
        publish=[(EXPOSED_CONTAINER_PORT, APPLICATION_SERVER_PORT)],
    ) as container:
        # Wait for uvicorn to come up
        sleep(SLEEP_TIME)

        uvicorn_gunicorn_container_config: (
            UvicornGunicornPoetryContainerConfig
        ) = UvicornGunicornPoetryContainerConfig(container.id)

        assert (
            f"{APPLICATION_SERVER_PORT}/tcp"
            in container.config.exposed_ports.keys()
        )

        verify_container_config(uvicorn_gunicorn_container_config)
