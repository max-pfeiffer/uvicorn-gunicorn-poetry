import json
from typing import List, Dict, Any

from docker.models.containers import Container


class UvicornGunicornPoetryContainer:

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
