import os
from datetime import datetime
from typing import Dict

import docker
from docker.models.images import Image

from build.constants import DOCKER_REPOSITORY, BASE_IMAGES


class DockerImage:
    def __init__(self, docker_client: docker.client):
        self.docker_client: docker.client = docker_client
        self.absolute_package_directory_path: str = os.path.dirname(
            os.path.abspath(__file__)
        )
        self.image_name: str = None
        self.image_tag: str = None
        self.dynamic_version_tag: str = datetime.today().strftime("%Y-%m-%d")


class UvicornGunicornPoetryImage(DockerImage):
    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        self.absolute_docker_image_directory_path: str = (
            self.absolute_package_directory_path
        )

        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        # self.image_name = 'pfeiffermax/uvicorn-gunicorn-poetry'
        self.image_name = DOCKER_REPOSITORY

    def build(self, target_architecture: str) -> Image:
        dockerfile: str = "Dockerfile"
        buildargs: Dict[str, str] = {
            "OFFICIAL_PYTHON_IMAGE": BASE_IMAGES[target_architecture]
        }
        tag: str = f"{self.image_name}:{target_architecture}-{self.dynamic_version_tag}"

        image: Image = self.docker_client.images.build(
            path=self.absolute_docker_image_directory_path,
            dockerfile=dockerfile,
            tag=tag,
            buildargs=buildargs,
        )[0]
        return image


class FastApiMultistageImage(DockerImage):
    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        absolute_project_root_directory: str = os.path.split(
            self.absolute_package_directory_path
        )[0]
        self.absolute_docker_image_directory_path: str = os.path.join(
            absolute_project_root_directory,
            "examples/fast_api_multistage_build",
        )

        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = "fast-api-multistage-build"

    def build(self, target_architecture: str, target: str) -> Image:
        self.image_tag = f"{target_architecture}-{self.dynamic_version_tag}"
        buildargs: Dict[str, str] = {
            "BASE_IMAGE_NAME_AND_TAG": f"{DOCKER_REPOSITORY}:{self.image_tag}"
        }
        image: Image = self.docker_client.images.build(
            path=self.absolute_docker_image_directory_path,
            dockerfile="Dockerfile",
            tag=f"{self.image_name}:{self.image_tag}",
            target=target,
            buildargs=buildargs,
        )[0]
        return image
