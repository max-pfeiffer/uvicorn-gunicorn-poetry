UVICORN_GUNICORN_POETRY_IMAGE_NAME = "pfeiffermax/uvicorn-gunicorn-poetry"
FAST_API_MULTISTAGE_IMAGE_NAME = "fast-api-multistage-build"
TARGET_ARCHITECTURES: list[str] = [
    "python3.9.14-bullseye",
    "python3.9.14-slim-bullseye",
    "python3.10.7-bullseye",
    "python3.10.7-slim-bullseye",
]
BASE_IMAGES: dict = {
    TARGET_ARCHITECTURES[
        0
    ]: "pfeiffermax/python-poetry:1.0.0-poetry1.2.2-python3.9.14-bullseye",
    TARGET_ARCHITECTURES[
        1
    ]: "pfeiffermax/python-poetry:1.0.0-poetry1.2.2-python3.9.14-slim-bullseye",
    TARGET_ARCHITECTURES[
        2
    ]: "pfeiffermax/python-poetry:1.0.0-poetry1.2.2-python3.10.7-bullseye",
    TARGET_ARCHITECTURES[
        3
    ]: "pfeiffermax/python-poetry:1.0.0-poetry1.2.2-python3.10.7-slim-bullseye",
}
PYTHON_VERSIONS: dict = {
    TARGET_ARCHITECTURES[0]: "3.9.14",
    TARGET_ARCHITECTURES[1]: "3.9.14",
    TARGET_ARCHITECTURES[2]: "3.10.7",
    TARGET_ARCHITECTURES[3]: "3.10.7",
}
APPLICATION_SERVER_PORT: str = "80"
