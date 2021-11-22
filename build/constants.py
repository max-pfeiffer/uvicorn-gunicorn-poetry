from typing import List

DOCKER_IMAGE_NAME = "pfeiffermax/uvicorn-gunicorn-poetry"
TARGET_ARCHITECTURES: List[str] = [
    "python3.9.8-bullseye",
    "python3.9.8-slim-bullseye",
]
BASE_IMAGES = {
    TARGET_ARCHITECTURES[0]: "python:3.9.8-bullseye",
    TARGET_ARCHITECTURES[1]: "python:3.9.8-slim-bullseye",
}
