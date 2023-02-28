# A multistage build with a dependency build stage has the following advantages:
# dependencies are only build when they actually change. Code changes do not
# trigger the dependency build stage (if dependencies have been built before
# once, build cache)
ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-gunicorn-poetry:2.0.0-python3.9.16-slim-bullseye@sha256:acc1c6a87b5f12001f7e75703572669c71b1bd299b85c4b4fdf1c9b5d804012f
FROM ${BASE_IMAGE_NAME_AND_TAG} as dependencies-build-stage

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY --chown=python_application:python_application ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --without dev

FROM ${BASE_IMAGE_NAME_AND_TAG} as production-image

# Copy virtual environment
COPY --chown=python_application:python_application --from=dependencies-build-stage /application_root/.venv /application_root/.venv

# Copy application files
COPY --chown=python_application:python_application /app /application_root/app/
