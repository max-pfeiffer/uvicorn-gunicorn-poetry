import argparse

import docker
from docker.models.images import Image

from constants import DOCKER_REPOSITORY
from images import UvicornGunicornPoetryImage

docker_client: docker.client = docker.from_env()


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description=""
    )
    parser.add_argument(
        "--username",
        required=False,
        help='Username for public Docker repository'
    )
    parser.add_argument(
        "--password",
        required=False,
        help='Password for public Docker repository'
    )
    parser.add_argument(
        "--target-architecture",
        required=False,
        choices=['python3.8.12-slim-bullseye', 'python3.8-alpine3.14'],
        default='python3.8.12-slim-bullseye',
        help='Target build architecture'
    )
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    print(str(args))

    new_uvicorn_gunicorn_poetry_image: UvicornGunicornPoetryImage = UvicornGunicornPoetryImage(docker_client)

    # Delete old existing images
    for old_image in docker_client.images.list(new_uvicorn_gunicorn_poetry_image.image_name):
        print('Old tags:')
        print(str(old_image.tags))
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)

    new_docker_image: Image = new_uvicorn_gunicorn_poetry_image.build(args.target_architecture)
    print('New tags:')
    print(str(new_docker_image.tags))

    docker_client.login(registry='https://index.docker.io/v1/',
                        username=args.username,
                        password=args.password)

    # There seems to be some problem with this call, docker_client is throwing "Internal Server Error ("invalid tag format")"
    for line in docker_client.images.push(DOCKER_REPOSITORY,
                                          tag=new_docker_image.tags[0],
                                          stream=True,
                                          decode=True):
        print(line)


if __name__ == "__main__":
    main()
