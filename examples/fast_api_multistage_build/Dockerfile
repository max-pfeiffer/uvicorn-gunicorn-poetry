ARG BASE_IMAGE_NAME_AND_TAG=pfeiffermax/uvicorn-gunicorn-poetry:1.3.0-python3.9.14-slim-bullseye
ARG OFFICIAL_PYTHON_IMAGE
ARG APPLICATION_SERVER_PORT=80
FROM ${BASE_IMAGE_NAME_AND_TAG} as production-dependencies-build-stage

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --without dev

FROM ${OFFICIAL_PYTHON_IMAGE} as production-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root

WORKDIR /application_root

COPY --from=production-dependencies-build-stage /application_root/.venv /application_root/.venv
COPY --from=production-dependencies-build-stage /application_server/start_gunicorn.sh /application_server/start_gunicorn.sh
COPY --from=production-dependencies-build-stage /application_server/gunicorn_configuration.py /application_server/gunicorn_configuration.py

# Copy application files
COPY /app /application_root/app/

# Activate entrypoint for running the uvicorn application server
CMD ["/application_server/start_gunicorn.sh"]

# Document the exposed port which was configured in start_uvicorn.sh
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE ${APPLICATION_SERVER_PORT}

FROM production-dependencies-build-stage as dev-dependencies-build-stage

# install [tool.poetry.dev-dependencies]
RUN poetry install --no-interaction --no-root

FROM ${OFFICIAL_PYTHON_IMAGE} as development-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    WORKERS="1" \
    LOG_LEVEL="debug"

WORKDIR /application_root

COPY --from=dev-dependencies-build-stage /application_root/.venv /application_root/.venv
COPY --from=dev-dependencies-build-stage /application_server/start_gunicorn.sh /application_server/
COPY --from=dev-dependencies-build-stage /application_server/gunicorn_configuration.py /application_server/gunicorn_configuration.py

COPY . /application_root/

# Activate entrypoint for running the uvicorn application server
CMD ["/application_server/start_gunicorn.sh"]

# Document the exposed port which was configured in start_uvicorn.sh
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE ${APPLICATION_SERVER_PORT}

FROM ${OFFICIAL_PYTHON_IMAGE} as test-base-image

ENV WORKERS="1" \
    LOG_LEVEL="debug"

COPY --from=dev-dependencies-build-stage /application_root/.venv /application_root/.venv

COPY /app /application_root/app/
COPY /tests /application_root/tests/

# Add pyproject.toml because it contains the configuration for black and pytest
COPY /pyproject.toml /application_root/

# image for running pep8 checks
FROM test-base-image as black-test-image

WORKDIR /application_root

COPY --from=dev-dependencies-build-stage /entrypoints/black_entrypoint.sh /entrypoints/

ENTRYPOINT /entrypoints/black_entrypoint.sh $0 $@

CMD ["--check", "."]

# image for running tests
FROM test-base-image as test-image

WORKDIR /application_root

COPY --from=dev-dependencies-build-stage /entrypoints/pytest_entrypoint.sh /entrypoints/

ENTRYPOINT /entrypoints/pytest_entrypoint.sh $0 $@

# You need to use pytest-cov as pytest plugin. Makes life very simple.
# tests directory is configured in pyproject.toml
# https://github.com/pytest-dev/pytest-cov
CMD ["--cov=app", "--cov-report=xml:/test_coverage_reports/unit_tests_coverage.xml"]
