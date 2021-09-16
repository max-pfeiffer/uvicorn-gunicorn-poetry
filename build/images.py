import os
from typing import Dict

import docker
from docker.models.images import Image


class DockerImage:

    def __init__(self):
        self.docker_client: docker.client = docker.from_env()

        absolute_package_directory_path: str = \
            os.path.dirname(os.path.abspath(__file__))
        absolute_project_root_directory: str = \
            os.path.split(absolute_package_directory_path)[0]
        self.absolute_docker_image_directory_path: str = \
            os.path.join(absolute_project_root_directory, 'docker-image')


class UvicornGunicornPoetryImage(DockerImage):

    def __init__(self):
        super().__init__()
        self.image_name: str = 'uvicorn-gunicorn-poetry'

    def build(self, target_architecture: str) -> Image:
        dockerfile: str = '{}.dockerfile'.format(target_architecture)
        tag: str = '{}:{}'.format(self.image_name, target_architecture)

        image: Image = self.docker_client.images.build(
            path=self.absolute_docker_image_directory_path,
            dockerfile=dockerfile,
            tag=tag
        )[0]
        return image


class FastApiMultistageImage(DockerImage):

    def __init__(self):
        super().__init__()
        self.image_name: str = 'fast-api-multistage-build'

    def build(self,
              target_architecture: str,
              target: str) -> Image:
        tag: str = '{}:{}'.format(self.image_name, target_architecture)
        buildargs: Dict[str, str] = \
            {'BASE_IMAGE_NAME_AND_TAG': 'uvicorn-gunicorn-poetry:{}'
                .format(target_architecture)}

        image: Image = self.docker_client.images.build(
            path=self.absolute_docker_image_directory_path,
            dockerfile='Dockerfile',
            tag=tag,
            target=target,
            buildargs=buildargs
        )[0]
        return image
