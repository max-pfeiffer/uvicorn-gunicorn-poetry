UVICORN_GUNICORN_POETRY_IMAGE_NAME = "pfeiffermax/uvicorn-gunicorn-poetry"
FAST_API_SINGLESTAGE_IMAGE_NAME: str = "fast-api-singlestage-build"
FAST_API_MULTISTAGE_IMAGE_NAME = "fast-api-multistage-build"
TARGET_ARCHITECTURES: list[str] = [
    "python3.9.16-bullseye",
    "python3.9.16-slim-bullseye",
    "python3.10.11-bullseye",
    "python3.10.11-slim-bullseye",
    "python3.11.3-bullseye",
    "python3.11.3-slim-bullseye",
]
BASE_IMAGES: dict = {
    TARGET_ARCHITECTURES[
        0
    ]: "pfeiffermax/python-poetry:1.3.0-poetry1.5.0-python3.9.16-bullseye@sha256:b5859d3d2308999853db2b14647b0ff155b86bf6b9f5799366c01c465ebb532a",
    TARGET_ARCHITECTURES[
        1
    ]: "pfeiffermax/python-poetry:1.3.0-poetry1.5.0-python3.9.16-slim-bullseye@sha256:9f35b4d878d5a3d421a21e388653e55cce0c09b3736c9b835c0fbbafeb1d1757",
    TARGET_ARCHITECTURES[
        2
    ]: "pfeiffermax/python-poetry:1.3.0-poetry1.5.0-python3.10.11-bullseye@sha256:d789d7e7a386e70da132ee0015dd7ece073a486b5db39a1aad22c1a59270b461",
    TARGET_ARCHITECTURES[
        3
    ]: "pfeiffermax/python-poetry:1.3.0-poetry1.5.0-python3.10.11-slim-bullseye@sha256:4a4b89205389d95f77868e574c796c8335447ad18204f1d041987c710c2ec423",
    TARGET_ARCHITECTURES[
        4
    ]: "pfeiffermax/python-poetry:1.3.0-poetry1.5.0-python3.11.3-bullseye@sha256:42909a19b117146153344ddea0c5332d807d26bb7a63ab5c5fd08a0879a3623c",
    TARGET_ARCHITECTURES[
        5
    ]: "pfeiffermax/python-poetry:1.3.0-poetry1.5.0-python3.11.3-slim-bullseye@sha256:47905681d13ca8c1c044dbdadfbe882f1633f524755406cb50a7bc2a2b80a422",
}
PYTHON_VERSIONS: dict = {
    TARGET_ARCHITECTURES[0]: "3.9.16",
    TARGET_ARCHITECTURES[1]: "3.9.16",
    TARGET_ARCHITECTURES[2]: "3.10.11",
    TARGET_ARCHITECTURES[3]: "3.10.11",
    TARGET_ARCHITECTURES[4]: "3.11.3",
    TARGET_ARCHITECTURES[5]: "3.11.3",
}

# As we are running the server with an unprivileged user, we need to use
# a high port.
APPLICATION_SERVER_PORT: str = "8000"
