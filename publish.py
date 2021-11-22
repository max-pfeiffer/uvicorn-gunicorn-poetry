import argparse
import os

import docker
from dotenv import load_dotenv

from build.constants import TARGET_ARCHITECTURES, DOCKER_IMAGE_NAME
from build.images import UvicornGunicornPoetryImage

environment_variables_loaded: bool = load_dotenv()

docker_hub_username: str = os.getenv("DOCKER_HUB_USERNAME")
docker_hub_password: str = os.getenv("DOCKER_HUB_PASSWORD")
version_tag: str = os.getenv("VERSION_TAG")


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(usage="%(prog)s [OPTION]", description="")
    parser.add_argument(
        "--username",
        required=False,
        default="pfeiffermax",
        help="Username for public Docker repository",
    )
    parser.add_argument(
        "--password",
        required=False,
        help="Password for public Docker repository",
    )
    parser.add_argument(
        "--target-architecture",
        required=False,
        choices=TARGET_ARCHITECTURES,
        default=TARGET_ARCHITECTURES[0],
        help="Target build architecture",
    )
    return parser


def main() -> None:
    docker_client: docker.client = docker.from_env()

    for target_architecture in TARGET_ARCHITECTURES:
        new_uvicorn_gunicorn_poetry_image: UvicornGunicornPoetryImage = (
            UvicornGunicornPoetryImage(docker_client)
        )

        # Delete old existing images
        for old_image in docker_client.images.list(
            new_uvicorn_gunicorn_poetry_image.image_name
        ):
            print("Old tags:")
            print(str(old_image.tags))
            for tag in old_image.tags:
                docker_client.images.remove(tag, force=True)

        new_uvicorn_gunicorn_poetry_image.build(target_architecture)

        # https://docs.docker.com/engine/reference/commandline/push/
        # https://docs.docker.com/engine/reference/commandline/tag/
        # https://docs.docker.com/engine/reference/commandline/image_tag/
        docker_client.login(username=docker_hub_username,
                            password=docker_hub_password)
        for line in docker_client.images.push(
            DOCKER_IMAGE_NAME,
            tag=new_uvicorn_gunicorn_poetry_image.image_tag,
            stream=True,
            decode=True,
        ):
            print(line)
    docker_client.close()


if __name__ == "__main__":
    main()
