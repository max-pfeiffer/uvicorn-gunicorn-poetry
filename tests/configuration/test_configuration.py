import json
import time

import docker
import requests
from docker.errors import NotFound
from docker.models.containers import Container
from docker.models.images import Image

from build.containers import UvicornGunicornPoetryContainer
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME, HELLO_WORLD, \
    DEFAULT_GUNICORN_CONFIG

docker_client = docker.client.from_env()


def verify_container(container: UvicornGunicornPoetryContainer) -> None:
    response = requests.get("http://127.0.0.1:8000")
    assert json.loads(response.text) == HELLO_WORLD

    config_data = container.get_config()
    assert config_data['bind'] == DEFAULT_GUNICORN_CONFIG['bind']
    assert config_data['workers'] == DEFAULT_GUNICORN_CONFIG['workers']
    assert config_data['timeout'] == DEFAULT_GUNICORN_CONFIG['timeout']
    assert config_data['graceful_timeout'] == DEFAULT_GUNICORN_CONFIG['graceful_timeout']
    assert config_data['keepalive'] == DEFAULT_GUNICORN_CONFIG['keepalive']
    assert config_data['loglevel'] == DEFAULT_GUNICORN_CONFIG['loglevel']
    assert config_data['accesslog'] == DEFAULT_GUNICORN_CONFIG['accesslog']
    assert config_data['errorlog'] == DEFAULT_GUNICORN_CONFIG['bind']
    assert config_data['reload'] == DEFAULT_GUNICORN_CONFIG['reload']
    assert config_data['worker_tmp_dir'] == DEFAULT_GUNICORN_CONFIG['worker_tmp_dir']


def test_default_configuration() -> None:
    try:
        previous = docker_client.containers.get(TEST_CONTAINER_NAME)
        previous.stop()
        previous.remove()
    except NotFound:
        pass

    UvicornGunicornPoetryImage(docker_client) \
        .build('python3.8.12-slim-bullseye')
    test_image: Image = FastApiMultistageImage(docker_client)\
        .build('python3.8.12-slim-bullseye', 'production-image')

    test_container: Container = \
        docker_client.containers.run(test_image.tags[0],
                                     name=TEST_CONTAINER_NAME,
                                     ports={"80": "8000"},
                                     detach=True)
    uvicorn_gunicorn_container: UvicornGunicornPoetryContainer = \
        UvicornGunicornPoetryContainer(test_container)
    time.sleep(SLEEP_TIME)
    verify_container(uvicorn_gunicorn_container)
    test_container.stop()

    # Test restarting the container
    test_container.start()
    time.sleep(SLEEP_TIME)
    verify_container(uvicorn_gunicorn_container)
    test_container.stop()
    test_container.remove()
