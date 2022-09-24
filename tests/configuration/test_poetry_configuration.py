import time
from uuid import uuid4

import pytest
from docker.models.containers import Container

from build.constants import POETRY_VERSION
from tests.constants import SLEEP_TIME


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_poetry_configuration(
    docker_client,
    fast_api_multistage_development_image,
    cleaned_up_test_container,
) -> None:
    test_container: Container = docker_client.containers.run(
        fast_api_multistage_development_image,
        name=cleaned_up_test_container,
        ports={"80": "8000"},
        detach=True,
    )
    time.sleep(SLEEP_TIME)

    (exit_code, output) = test_container.exec_run(["poetry", "--version"])
    assert exit_code == 0
    assert f"Poetry (version {POETRY_VERSION})" in output.decode("utf-8")

    (exit_code, output) = test_container.exec_run(
        ["poetry", "config", "--list"]
    )
    assert exit_code == 0
    assert "virtualenvs.in-project = true" in output.decode("utf-8")
