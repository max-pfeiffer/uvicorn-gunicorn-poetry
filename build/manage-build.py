import argparse
from images import UvicornGunicornPoetryImage, FastApiMultistageImage

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


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if args.test:
        base_image: Image = UvicornGunicornPoetryImage().build(args.target_architecture)
        example_image_development: Image = FastApiMultistageImage().build(args.target_architecture, 'development-image')
    else:
        base_image: Image = UvicornGunicornPoetryImage().build(args.target_architecture)
    print(str(args))


if __name__ == "__main__":
    main()
