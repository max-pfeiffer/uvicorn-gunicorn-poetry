FROM uvicorn-gunicorn-poetry:test as base-image

WORKDIR /application_root

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-dev --no-root --no-interaction

FROM base-image as development-image
ENV LOG_LEVEL="debug" \
    WORKERS="1" \
    RELOAD="True"

# install [tool.poetry.dev-dependencies]
COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH
RUN poetry install --no-root --no-interaction

COPY . /application_root/

FROM base-image as production-image
ENV WORKERS="2"

COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH

COPY /app /application_root/app/
