import os
from datetime import datetime
from typing import Dict

import docker
from docker.models.images import Image


class DockerImage:

    def __init__(self, docker_client: docker.client):
        self.docker_client: docker.client = docker_client
        self.absolute_package_directory_path: str = \
            os.path.dirname(os.path.abspath(__file__))
        self.version_tag: str = datetime.today().strftime('%Y-%m-%d')


class UvicornGunicornPoetryImage(DockerImage):

    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        self.absolute_docker_image_directory_path: str = \
            self.absolute_package_directory_path
        self.image_name: str = 'pfeiffermax/uvicorn-gunicorn-poetry'

    def build(self, target_architecture: str) -> Image:
        dockerfile: str = f'{target_architecture}.dockerfile'
        tag: str = f'{self.image_name}:{target_architecture}-{self.version_tag}'

        image: Image = self.docker_client.images.build(
            path=self.absolute_docker_image_directory_path,
            dockerfile=dockerfile,
            tag=tag
        )[0]
        return image


class FastApiMultistageImage(DockerImage):

    def __init__(self, docker_client: docker.client):
        super().__init__(docker_client)
        absolute_project_root_directory: str = \
            os.path.split(self.absolute_package_directory_path)[0]
        self.absolute_docker_image_directory_path: str = \
            os.path.join(absolute_project_root_directory,
                         'examples/fast_api_multistage_build')
        self.image_name: str = 'fast-api-multistage-build'

    def build(self,
              target_architecture: str,
              target: str) -> Image:
        tag: str = \
            f'{self.image_name}:{target_architecture}-{self.version_tag}'
        buildargs: Dict[str, str] = \
            {'BASE_IMAGE_NAME_AND_TAG': f'uvicorn-gunicorn-poetry:{target_architecture}-{self.version_tag}'}

        image: Image = self.docker_client.images.build(
            path=self.absolute_docker_image_directory_path,
            dockerfile='Dockerfile',
            tag=tag,
            target=target,
            buildargs=buildargs
        )[0]
        return image
