from typing import List

DOCKER_REPOSITORY = "pfeiffermax/uvicorn-gunicorn-poetry"
TARGET_ARCHITECTURE: List[str] = [
    "python3.9.7-bullseye",
    "python3.9.7-slim-bullseye",
    "python3.9.8-bullseye",
    "python3.9.8-slim-bullseye",
]
