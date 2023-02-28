# Be aware that you need to specify these arguments before the first FROM
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-gunicorn-poetry:1.3.0-python3.9.14-slim-bullseye
FROM ${BASE_IMAGE_NAME_AND_TAG}

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY --chown=python_application:python_application ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root

# Copy application files
COPY --chown=python_application:python_application /app /application_root/app/