import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import docker
from docker.models.containers import Container
from docker_image import reference


class UvicornGunicornPoetryContainerConfig:
    def __init__(self, container_id: str):
        self.container: Container = docker.from_env().containers.get(
            container_id
        )

    def get_process_names(self) -> List[str]:
        top = self.container.top()
        process_commands = [p[7] for p in top["Processes"]]
        gunicorn_processes = [p for p in process_commands if "gunicorn" in p]
        return gunicorn_processes

    def get_gunicorn_conf_path(self) -> str:
        gunicorn_processes = self.get_process_names()
        first_process = gunicorn_processes[0]
        first_part, partition, last_part = first_process.partition("-c")
        gunicorn_conf = last_part.strip().split()[0]
        return gunicorn_conf

    def get_config(self) -> Dict[str, Any]:
        gunicorn_conf = self.get_gunicorn_conf_path()
        result = self.container.exec_run(f"python {gunicorn_conf}")
        return json.loads(result.output.decode())


@dataclass
class ImageTagComponents:
    """Class for parsing and providing image tag components."""

    registry: str
    image_name: str
    tag: str
    version: str
    python_version: str
    os_variant: str

    @classmethod
    def create_from_reference(cls, tag: str):
        """Instantiate a class using an image tag.

        :param tag:
        :return:
        """
        ref = reference.Reference.parse(tag)
        registry: str = ref.repository["domain"]
        image_name: str = ref.repository["path"]
        tag: str = ref["tag"]

        tag_parts: list[str] = tag.split("-")
        version: str = tag_parts[0]
        python_version: str = tag_parts[1].lstrip("python")
        os_variant: str = "-".join(tag_parts[2:])
        return cls(
            registry=registry,
            image_name=image_name,
            tag=tag,
            version=version,
            python_version=python_version,
            os_variant=os_variant,
        )


def get_fast_api_singlestage_context() -> Path:
    """Return Docker build context for single stage example app.

    :return:
    """
    context: Path = (
        Path(__file__).parent.parent.resolve()
        / "examples"
        / "fast_api_singlestage_build"
    )
    return context


def get_fast_api_singlestage_image_reference(
    registry: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> str:
    """Return image reference for single stage example app.

    :param registry:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    reference: str = (
        f"{registry}/fast-api-singlestage-build:{image_version}"
        f"-python{python_version}-{os_variant}"
    )
    return reference


def get_fast_api_multistage_context() -> Path:
    """Return Docker build context for multi-stage example app.

    :return:
    """
    context: Path = (
        Path(__file__).parent.parent.resolve()
        / "examples"
        / "fast_api_multistage_build"
    )
    return context


def get_fast_api_multistage_image_reference(
    registry: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> str:
    """Return image reference for multi-stage example app.

    :param registry:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    reference: str = (
        f"{registry}/fast-api-multistage-build:{image_version}"
        f"-python{python_version}-{os_variant}"
    )
    return reference


def get_fast_api_multistage_with_json_logging_context() -> Path:
    """Return Docker build context for multi-stage example app with JSON logging.

    :return:
    """
    context: Path = (
        Path(__file__).parent.parent.resolve()
        / "examples"
        / "fast_api_multistage_build_with_json_logging"
    )
    return context


def get_fast_api_multistage_with_json_logging_image_reference(
    registry: str,
    image_version: str,
    python_version: str,
    os_variant: str,
) -> str:
    """Return image reference for multi-stage example app with JSON logging.

    :param registry:
    :param image_version:
    :param python_version:
    :param os_variant:
    :return:
    """
    reference: str = (
        f"{registry}/fast_api_multistage_build_with_json_logging:{image_version}"
        f"-python{python_version}-{os_variant}"
    )
    return reference
