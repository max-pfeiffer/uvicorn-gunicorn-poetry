[![codecov](https://codecov.io/gh/max-pfeiffer/uvicorn-gunicorn-poetry/branch/main/graph/badge.svg?token=ZRUKVNP3I5)](https://codecov.io/gh/max-pfeiffer/uvicorn-gunicorn-poetry)
![pipeline workflow](https://github.com/max-pfeiffer/uvicorn-gunicorn-poetry/actions/workflows/pipeline.yml/badge.svg)
![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/pfeiffermax/uvicorn-gunicorn-poetry?sort=semver)
![Docker Pulls](https://img.shields.io/docker/pulls/pfeiffermax/uvicorn-gunicorn-poetry)
# uvicorn-gunicorn-poetry - Docker image for FastAPI
This Docker image provides a platform to run Python applications with [Gunicorn](https://gunicorn.org) as process manager and
[Uvicorn](https://www.uvicorn.org/) workers.
It provides [Poetry](https://python-poetry.org/) for managing dependencies and setting up a virtual environment in the container.

This image aims to follow the best practices for a production grade container image for hosting Python web applications based
on micro frameworks like [FastAPI](https://fastapi.tiangolo.com/).
Therefore, source and documentation contain a lot of references to documentation of dependencies used in this project, so users
of this image can follow up on that.

If you would like to run your Python application with Uvicorn on [Kubernetes](https://kubernetes.io/), please check out my other project which does not use
Gunicorn as process manager: https://github.com/max-pfeiffer/uvicorn-poetry

Any feedback is highly appreciated and will be considered.  

**Docker Hub:** [pfeiffermax/uvicorn-gunicorn-poetry](https://hub.docker.com/r/pfeiffermax/uvicorn-gunicorn-poetry)

**GitHub Repository:** [https://github.com/max-pfeiffer/uvicorn-gunicorn-poetry](https://github.com/max-pfeiffer/uvicorn-gunicorn-poetry)

## Docker Image Features
1. Supported architectures:
   1. Python v3.9, Debian or Debian-slim
   2. Python v3.10, Debian or Debian-slim
   3. Python v3.11, Debian or Debian-slim
2. Poetry is available as Python package dependency management tool
3. A virtual environment for the application and application server
4. The application is run with [Gunicorn](https://gunicorn.org/) and Uvicorn workers

## Usage
It just provides a platform that you can use to build upon your own multistage builds. So it consequently does not contain an
application itself.

Please check out the [example application for multistage builds](https://github.com/max-pfeiffer/uvicorn-gunicorn-poetry/tree/master/examples/fast_api_multistage_build)
on how to use that image and build containers efficiently.

There is also another [sample app demonstrating a very simple single stage build](https://github.com/max-pfeiffer/uvicorn-gunicorn-poetry/tree/main/examples/fast_api_singlestage_build).

Please be aware that your application needs an application layout without src folder which is proposed in
[fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app).
The application and test structure needs to be like that:
```bash
├── Dockerfile
├── app
│   ├── __init__.py
│   └── main.py
├── poetry.lock
├── pyproject.toml
└── tests
    ├── __init__.py
    ├── conftest.py
    └── test_api
        ├── __init__.py
        ├── test_items.py
        └── test_root.py
```
Please be aware that you need to provide a pyproject.toml file to specify your Python package dependencies for Poetry and configure
dependencies like Pytest. Poetry dependencies must at least contain the following to work:
* python = "^3.9"
* gunicorn = "20.1.0"
* uvicorn = "0.18.3"

If your application uses FastAPI framework this needs to be added as well:
* fastapi = "0.85.0"

**IMPORTANT:** make sure you have a [.dockerignore file](https://github.com/max-pfeiffer/uvicorn-gunicorn-poetry/blob/master/examples/fast_api_multistage_build/.dockerignore)
in your application root which excludes your local virtual environment in .venv! Otherwise, you will have an issue activating that virtual
environment when running the container.

## Configuration
Configuration is done through the following environment variables during docker build.
For all the following configuration options please see always the
[official Gunicorn documentation](https://docs.gunicorn.org/en/stable/settings.html)
if you would like to do a deep dive. Following environment variables are supported:

### [Logging](https://docs.gunicorn.org/en/stable/settings.html#logging)
`LOG_LEVEL` : The granularity of Error log outputs. Valid level names are:
* debug
* info
* warning
* error
* critical
 
**default:** `info`

`ACCESS_LOG` : The Access log file to write to.

**default:** `-`

`ERROR_LOG` : The Error log file to write to.  

**default:** `-`

### [Worker processes](https://docs.gunicorn.org/en/stable/settings.html#worker-processes)
`WORKERS` : The number of worker processes for handling requests. By default, this is set to one
worker as this image is meant to be used on a production grade Kubernetes environment. There you
have usually monitoring data exported to Prometheus which will not work properly with multiple workers.   

**default:** `1`

`TIMEOUT` : Workers silent for more than this many seconds are killed and restarted.

**default:** `30`

`GRACEFUL_TIMEOUT` : Timeout for graceful workers restart.

**default:** `30`

`KEEP_ALIVE` : The number of seconds to wait for requests on a Keep-Alive connection.

**default:** `2`

### [Server mechanics](https://docs.gunicorn.org/en/stable/settings.html?highlight=worker_tmp_dir#worker-tmp-dir)
`WORKER_TMP_DIR` : A directory to use for the worker heartbeat temporary file.
By default, this is set to /dev/shm to speed up the startup of workers by using a in memory file system

**default:** `/dev/shm`

### [Server socket](https://docs.gunicorn.org/en/stable/settings.html?highlight=bind#bind)
`BIND` : The socket to bind.

**default:** `0.0.0.0:8000`
