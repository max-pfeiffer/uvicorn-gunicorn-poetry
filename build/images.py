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
    def __init__(
        self,
        docker_client: DockerClient,
        target_architecture: str,
        version: str,
    ):
        self.docker_client: DockerClient = docker_client
        self.dockerfile_name: str = "Dockerfile"
        self.dockerfile_directory: Optional[Path] = None
        self.image_name: Optional[str] = None
        self.image_tag: Optional[str] = None
        self.version: Optional[str] = version
        self.target_architecture: str = target_architecture


class UvicornGunicornPoetryImage(DockerImage):
    def __init__(
        self,
        docker_client: DockerClient,
        target_architecture: str,
        version: str,
    ):
        super().__init__(docker_client, target_architecture, version)
        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name = UVICORN_GUNICORN_POETRY_IMAGE_NAME
        self.dockerfile_directory: Path = Path(__file__).parent.resolve()

    def build(self) -> Image:
        self.image_tag: str = f"{self.version}-{self.target_architecture}"

        buildargs: dict[str, str] = {
            "BASE_IMAGE": BASE_IMAGES[self.target_architecture],
            "APPLICATION_SERVER_PORT": APPLICATION_SERVER_PORT,
        }

        image: Image = self.docker_client.images.build(
            path=str(self.dockerfile_directory),
            dockerfile=self.dockerfile_name,
            tag=f"{self.image_name}:{self.image_tag}",
            buildargs=buildargs,
        )[0]
        return image


class ExampleApplicationImage(DockerImage):
    def build(
        self,
        target: str,
        base_image_tag: str,
    ) -> Image:
        self.image_tag = f"{self.version}-{self.target_architecture}"

        buildargs: dict[str, str] = {
            "BASE_IMAGE_NAME_AND_TAG": base_image_tag,
        }
        image: Image = self.docker_client.images.build(
            path=str(self.dockerfile_directory),
            dockerfile=self.dockerfile_name,
            tag=f"{self.image_name}:{self.image_tag}",
            target=target,
            buildargs=buildargs,
        )[0]
        return image


class FastApiSinglestageImage(ExampleApplicationImage):
    def __init__(
        self,
        docker_client: DockerClient,
        target_architecture: str,
        version: str,
    ):
        super().__init__(docker_client, target_architecture, version)
        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = FAST_API_SINGLESTAGE_IMAGE_NAME
        self.dockerfile_directory: Path = (
            Path(__file__).parent.parent.resolve()
            / "examples"
            / "fast_api_singlestage_build"
        )


class FastApiMultistageImage(ExampleApplicationImage):
    def __init__(
        self,
        docker_client: DockerClient,
        target_architecture: str,
        version: str,
    ):
        super().__init__(docker_client, target_architecture, version)
        # An image name is made up of slash-separated name components, optionally prefixed by a registry hostname.
        # see: https://docs.docker.com/engine/reference/commandline/tag/
        self.image_name: str = FAST_API_MULTISTAGE_IMAGE_NAME
        self.dockerfile_directory: Path = (
            Path(__file__).parent.parent.resolve()
            / "examples"
            / "fast_api_multistage_build"
        )
