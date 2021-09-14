# uvicorn-gunicorn-poetry
This image provides a platform to install Gunicorn with Uvicorn workers for running a web application.
It provides [Poetry](https://python-poetry.org/) for managing dependencies and setting up a virtual environment in the container.

This image aims to follow the best practices for a production grade container image for hosting Python web applications based
on micro frameworks like [FastAPI](https://fastapi.tiangolo.com/).
Therefore source and documentation contain a lot of references to documentation of dependencies used in this project, so users
of this image can follow up on that.

Any feedback is highly appreciated and will be considered.  

## Usage
This image just provides a platform that you can use to build upon your own multistage builds. So it consequently does not contain an
application itself. Please check out the example application on how to use that image and how to build a container efficiently.

Please be aware that your application needs an application layout without src folder which is proposed in
[fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app).
The application and test structure needs to be like that:
```bash
├── Dockerfile
├── app
│   ├── __init__.py
│   └── main.py
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

