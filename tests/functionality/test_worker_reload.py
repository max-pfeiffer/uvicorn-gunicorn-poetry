import time

from build.images import UvicornGunicornPoetryImage, FastApiMultistageImage
from tests.constants import TEST_CONTAINER_NAME, SLEEP_TIME
from docker.models.containers import Container
from docker.models.images import Image


def test_worker_reload(docker_client) -> None:
    UvicornGunicornPoetryImage(docker_client) \
        .build('python3.8.12-slim-bullseye')
    test_image: Image = FastApiMultistageImage(docker_client) \
        .build('python3.8.12-slim-bullseye', 'development-image')

    test_container: Container = \
        docker_client.containers.run(test_image.tags[0],
                                     name=TEST_CONTAINER_NAME,
                                     ports={"80": "8000"},
                                     detach=True)
    time.sleep(SLEEP_TIME)

    (exit_code, output) = test_container.exec_run([
        'touch',
        '/application_root/app/main.py'
    ])
    assert exit_code == 0
    assert output.decode("utf-8") == ''
    time.sleep(SLEEP_TIME)
    logs: str = test_container.logs().decode("utf-8")
    assert 'Worker reloading: /application_root/app/main.py modified' in logs
