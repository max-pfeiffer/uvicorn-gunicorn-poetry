# References:
# https://hub.docker.com/_/python
FROM python:3.9.7-alpine3.14

# References:
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# https://pip.pypa.io/en/stable/topics/caching/#avoiding-caching
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_NO_CACHE_DIR#cmdoption-no-cache-dir
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_DISABLE_PIP_VERSION_CHECK#cmdoption-disable-pip-version-check
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_DEFAULT_TIMEOUT#cmdoption-timeout
# https://pip.pypa.io/en/stable/topics/configuration/#environment-variables
# https://python-poetry.org/docs/#installation

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.8 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    VIRTUAL_ENVIRONMENT_PATH="/application_root/.venv"

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"

# https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions
RUN apk add --no-cache \
        curl \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && apk del \
        curl \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev

COPY gunicorn_configuration.py ./scripts/start_gunicorn.sh /application_server/
RUN chmod +x /application_server/start_gunicorn.sh

COPY ./scripts/pytest_entrypoint.sh ./scripts/black_entrypoint.sh /entrypoints/
RUN chmod +x /entrypoints/pytest_entrypoint.sh
RUN chmod +x /entrypoints/black_entrypoint.sh

EXPOSE 80

CMD ["/application_server/start_gunicorn.sh"]
