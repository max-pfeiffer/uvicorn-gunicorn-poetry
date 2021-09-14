import argparse
import subprocess
import sys
from typing import Tuple, Dict

import docker
from docker.models.images import Image

docker_client: docker.client = docker.from_env()


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description=""
    )
    parser.add_argument(
        "--target-architecture",
        required=False,
        choices=['python3.8.12-slim-bullseye', 'python3.8-alpine3.14'],
        default='python3.8.12-slim-bullseye',
        help='Target build architecture'
    )
    parser.add_argument(
        "--test",
        required=False,
        action='store_true',
        default=False,
        help='Builds images for running the tests'
    )
    return parser


def build_image(target_architecture: str) -> Image:
    dockerfile: str = '{}.dockerfile'.format(target_architecture)
    tag: str = 'uvicorn-gunicorn-poetry:{}'.format(target_architecture)

    image: Image = docker_client.images.build(
        path='docker-image/',
        dockerfile=dockerfile,
        tag=tag
    )[0]
    return image


def build_example__image_fast_api_multistage_build(target_architecture: str,
                                                   target: str) -> Image:
    tag: str = 'fast-api-multistage-build:{}'.format(target_architecture)
    buildargs: Dict[str, str] = \
        {'TAG': 'uvicorn-gunicorn-poetry:{}'.format(target_architecture)}

    image: Image = docker_client.images.build(
        path='examples/fast_api_multistage_build',
        dockerfile='Dockerfile',
        tag=tag,
        target=target,
        buildargs=buildargs
    )[0]
    return image


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if args.test:
        base_image: Image = build_image(args.target_architecture)
        example_image_development: Image = build_example__image_fast_api_multistage_build(args.target_architecture, 'development-image')
    else:
        base_image: Image = build_image(args.target_architecture)
    print(str(args))


if __name__ == "__main__":
    main()
