import argparse

import docker
from docker.models.containers import Container
from docker.models.images import Image

from tests.containers import UvicornGunicornPoetryContainer
from images import UvicornGunicornPoetryImage, FastApiMultistageImage

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
        base_image: Image = UvicornGunicornPoetryImage(docker_client)\
            .build(args.target_architecture)
        example_image_development: Image = FastApiMultistageImage()\
            .build(args.target_architecture, 'development-image')
    else:
        UvicornGunicornPoetryImage(docker_client) \
            .build('python3.8.12-slim-bullseye')
        example_image_production: Image = \
            FastApiMultistageImage(docker_client) \
                .build('python3.8.12-slim-bullseye', 'production-image')

        example_container: Container = \
            docker_client.containers.run(example_image_production.tags[0],
                                              detach=True)
        uvicorn_gunicorn_container: UvicornGunicornPoetryContainer = \
            UvicornGunicornPoetryContainer(example_container)
        process_names = uvicorn_gunicorn_container.get_process_names()
        print('process_names')
        print(str(process_names))
        gunicorn_config = uvicorn_gunicorn_container.get_config()
        print('gunicorn_config')
        print(str(gunicorn_config))

        # base_image: Image = UvicornGunicornPoetryImage(docker_client)\
        #    .build(args.target_architecture)
    print(str(args))


if __name__ == "__main__":
    main()
