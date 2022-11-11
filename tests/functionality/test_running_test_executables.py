from typing import Dict
from uuid import uuid4

import pytest

from build.constants import APPLICATION_SERVER_PORT
from tests.constants import EXPOSED_CONTAINER_PORT


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_running_black_test_image(
    docker_client,
    fast_api_multistage_development_black_test_image,
    cleaned_up_test_container,
) -> None:
    api_response: Dict = docker_client.containers.run(
        fast_api_multistage_development_black_test_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_running_test_image(
    docker_client,
    fast_api_multistage_development_test_image,
    cleaned_up_test_container,
) -> None:
    api_response: Dict = docker_client.containers.run(
        fast_api_multistage_development_test_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
        detach=True,
    ).wait()
    assert api_response["StatusCode"] == 0
