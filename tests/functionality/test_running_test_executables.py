import time
from typing import Dict

from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME
from docker.models.containers import Container
from docker.models.images import Image


def test_worker_reload(docker_client) -> None:
    UvicornGunicornPoetryImage(docker_client) \
        .build('python3.8.12-slim-bullseye')
    test_image: Image = FastApiMultistageImage(docker_client) \
        .build('python3.8.12-slim-bullseye', 'unit-test-image')

    api_response: Dict = \
        docker_client.containers.run(test_image.tags[0],
                                     name=TEST_CONTAINER_NAME,
                                     ports={"80": "8000"},
                                     detach=True).wait()
    assert api_response['StatusCode'] == 0
