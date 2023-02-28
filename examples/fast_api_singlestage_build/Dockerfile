# Be aware that you need to specify these arguments before the first FROM
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-gunicorn-poetry:2.0.0-python3.9.16-slim-bullseye@sha256:acc1c6a87b5f12001f7e75703572669c71b1bd299b85c4b4fdf1c9b5d804012f
FROM ${BASE_IMAGE_NAME_AND_TAG}

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY --chown=python_application:python_application ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root

# Copy application files
COPY --chown=python_application:python_application /app /application_root/app/
