from typing import Dict

from docker.models.images import Image

from build.constants import TARGET_ARCHITECTURE
from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME


def test_running_pep8_test_image(docker_client) -> None:
    UvicornGunicornPoetryImage(docker_client).build(TARGET_ARCHITECTURE[0])
    test_image: Image = FastApiMultistageImage(docker_client).build(
        TARGET_ARCHITECTURE[0], "black-test-image"
    )

    api_response: Dict = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={"80": "8000"},
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0


def test_running_unit_test_image(docker_client) -> None:
    UvicornGunicornPoetryImage(docker_client).build(TARGET_ARCHITECTURE[0])
    test_image: Image = FastApiMultistageImage(docker_client).build(
        TARGET_ARCHITECTURE[0], "unit-test-image"
    )

    api_response: Dict = docker_client.containers.run(
        test_image.tags[0],
        name=TEST_CONTAINER_NAME,
        ports={"80": "8000"},
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0
