import argparse

import docker

from build.constants import TARGET_ARCHITECTURE, DOCKER_REPOSITORY
from build.images import UvicornGunicornPoetryImage

docker_client: docker.client = docker.from_env()


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
        choices=TARGET_ARCHITECTURE,
        default=TARGET_ARCHITECTURE[0],
        help="Target build architecture",
    )
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

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

    new_uvicorn_gunicorn_poetry_image.build(
        args.target_architecture
    )

    # https://docs.docker.com/engine/reference/commandline/push/
    # https://docs.docker.com/engine/reference/commandline/tag/
    # https://docs.docker.com/engine/reference/commandline/image_tag/
    docker_client.login(username=args.username, password=args.password)
    for line in docker_client.images.push(
        DOCKER_REPOSITORY,
        tag=new_uvicorn_gunicorn_poetry_image.image_tag,
        stream=True,
        decode=True,
    ):
        print(line)
    docker_client.close()


if __name__ == "__main__":
    main()
