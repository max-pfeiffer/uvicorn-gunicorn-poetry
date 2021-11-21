from typing import List

DOCKER_REPOSITORY = "pfeiffermax/uvicorn-gunicorn-poetry"
TARGET_ARCHITECTURE: List[str] = [
    "python3.9.8-bullseye",
    "python3.9.8-slim-bullseye",
]
BASE_IMAGES = {
    TARGET_ARCHITECTURE[0]: "python:3.9.8-bullseye",
    TARGET_ARCHITECTURE[1]: "python:3.9.8-slim-bullseye",
}
