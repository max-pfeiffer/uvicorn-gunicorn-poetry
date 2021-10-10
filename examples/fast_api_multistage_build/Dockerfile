ARG BASE_IMAGE_NAME_AND_TAG=uvicorn-gunicorn-poetry:python3.8.12-slim-bullseye
FROM ${BASE_IMAGE_NAME_AND_TAG} as base-image

WORKDIR /application_root

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-dev --no-root --no-interaction

FROM base-image as development-image
ENV WORKERS="1" \
    RELOAD="True" \
    LOG_LEVEL="debug"

COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH

# install [tool.poetry.dev-dependencies]
RUN poetry install --no-root --no-interaction

COPY . /application_root/

FROM base-image as production-image

COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH

COPY /app /application_root/app/
