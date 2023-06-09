from pathlib import Path
from typing import Optional

from docker.models.images import Image
from docker.client import DockerClient
from build.constants import (
    UVICORN_GUNICORN_POETRY_IMAGE_NAME,
    BASE_IMAGES,
    FAST_API_MULTISTAGE_IMAGE_NAME,
    APPLICATION_SERVER_PORT,
    FAST_API_SINGLESTAGE_IMAGE_NAME,
)


class DockerImage:
    def __init__(self, docker_client: DockerClient):
        self.docker_client: DockerClient = docker_client
        self.absolute_module_directory_path: Path = Path(
            __file__
        ).parent.resolve()
        self.image_name: Optional[str] = None
        self.image_tag: Optional[str] = None
        self.version_tag: Optional[str] = None
        self.dockerfile_name: str = "Dockerfile"


class UvicornGunicornPoetryImage(DockerImage):
    def __init__(self, docker_client: DockerClient):
        super().__init__(docker_client)
        self.absolute_docker_image_directory_path: Path = (
            self.absolute_module_directory_path
        )

        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        # self.image_name = 'pfeiffermax/uvicorn-gunicorn-poetry'
        self.image_name = UVICORN_GUNICORN_POETRY_IMAGE_NAME

    def build(self, target_architecture: str, version: str = None) -> Image:
        if version is not None:
            self.version_tag = version

        buildargs: dict[str, str] = {
            "BASE_IMAGE": BASE_IMAGES[target_architecture],
            "APPLICATION_SERVER_PORT": APPLICATION_SERVER_PORT,
        }
        tag: str = f"{self.image_name}:{self.version_tag}-{target_architecture}"

        image: Image = self.docker_client.images.build(
            path=str(self.absolute_docker_image_directory_path),
            dockerfile=self.dockerfile_name,
            tag=tag,
            buildargs=buildargs,
        )[0]
        return image


class FastApiSinglestageImage(DockerImage):
    def __init__(self, docker_client: DockerClient):
        super().__init__(docker_client)
        absolute_project_root_directory: Path = (
            self.absolute_module_directory_path.parent.resolve()
        )
        self.absolute_docker_image_directory_path: Path = (
            absolute_project_root_directory
            / "examples"
            / "fast_api_singlestage_build"
        )

        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = FAST_API_SINGLESTAGE_IMAGE_NAME

    def build(
        self, target_architecture: str, version: str, base_image_tag: str
    ) -> Image:
        self.version_tag = version

        self.image_tag = f"{self.version_tag}-{target_architecture}"

        buildargs: dict[str, str] = {
            "BASE_IMAGE_NAME_AND_TAG": base_image_tag,
        }
        image: Image = self.docker_client.images.build(
            path=str(self.absolute_docker_image_directory_path),
            dockerfile=self.dockerfile_name,
            tag=f"{self.image_name}:{self.image_tag}",
            buildargs=buildargs,
        )[0]
        return image


class FastApiMultistageImage(DockerImage):
    def __init__(self, docker_client: DockerClient):
        super().__init__(docker_client)
        absolute_project_root_directory: Path = (
            self.absolute_module_directory_path.parent.resolve()
        )
        self.absolute_docker_image_directory_path: Path = (
            absolute_project_root_directory
            / "examples"
            / "fast_api_multistage_build"
        )

        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = FAST_API_MULTISTAGE_IMAGE_NAME

    def build(
        self,
        target_architecture: str,
        target: str,
        version: str,
        base_image_tag: str,
    ) -> Image:
        self.version_tag = version

        self.image_tag = f"{self.version_tag}-{target_architecture}"

        buildargs: dict[str, str] = {
            "BASE_IMAGE_NAME_AND_TAG": base_image_tag,
        }
        image: Image = self.docker_client.images.build(
            path=str(self.absolute_docker_image_directory_path),
            dockerfile=self.dockerfile_name,
            tag=f"{self.image_name}:{self.image_tag}",
            target=target,
            buildargs=buildargs,
        )[0]
        return image
