import json
from typing import List, Dict, Any

from docker.models.containers import Container
from dataclasses import dataclass


class UvicornGunicornPoetryContainerConfig:
    def __init__(self, container: Container):
        self.container: Container = container

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
    image_name: str
    version: str
    target_architecture: str

    @classmethod
    def create_from_tag(cls, tag: str):
        tag_parts: list[str] = tag.split(":")
        image_name: str = tag_parts[0]
        image_tag: str = tag_parts[1]

        image_tag_parts: list[str] = image_tag.split("-")
        target_architecture_index = [
            index
            for index, tag_part in enumerate(image_tag_parts)
            if tag_part.startswith("python")
        ][0]

        version: str = "-".join(image_tag_parts[:target_architecture_index])
        target_architecture: str = "-".join(
            image_tag_parts[target_architecture_index:]
        )
        return cls(
            image_name=image_name,
            version=version,
            target_architecture=target_architecture,
        )


def create_version_tag_for_example_images(version: str, target: str) -> str:
    version_tag: str = f"{version}-{target}"
    return version_tag
