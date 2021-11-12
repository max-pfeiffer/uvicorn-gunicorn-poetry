ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-gunicorn-poetry:python3.9.8-slim-bullseye-2021-11-08
FROM ${BASE_IMAGE_NAME_AND_TAG} as base-image

WORKDIR /application_root

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-dev --no-root --no-interaction

FROM base-image as test-base-image
ENV WORKERS="1" \
    LOG_LEVEL="debug"

COPY --from=base-image $VIRTUAL_ENVIRONMENT_PATH $VIRTUAL_ENVIRONMENT_PATH

# install [tool.poetry.dev-dependencies]
RUN poetry install --no-root --no-interaction

COPY /app /application_root/app/
COPY /tests /application_root/tests/

# image for running pep8 checks
FROM test-base-image as black-test-image

ENTRYPOINT /entrypoints/black_entrypoint.sh $0 $@

CMD ["--target-version py39", "--check", " --line-length 80", "app"]

# image for running unit tests
FROM test-base-image as unit-test-image

ENTRYPOINT /entrypoints/pytest_entrypoint.sh $0 $@

# You need to use pytest-cov as pytest plugin. Makes life very simple.
# tests directory is configured in pyproject.toml
# https://github.com/pytest-dev/pytest-cov
CMD ["--cov=app", "--cov-report=xml:/test_coverage_reports/unit_tests_coverage.xml"]

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
