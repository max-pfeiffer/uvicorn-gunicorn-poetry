TEST_CONTAINER_NAME: str = "uvicorn-gunicorn-poetry-test"
SLEEP_TIME: float = 5.0
HELLO_WORLD: str = "Hello World!"
DEVELOPMENT_GUNICORN_CONFIG: dict[str, str] = {
    "bind": "0.0.0.0:80",
    "workers": 1,
    "timeout": 30,
    "graceful_timeout": 30,
    "keepalive": 2,
    "loglevel": "debug",
    "accesslog": "-",
    "errorlog": "-",
    "reload": True,
    "worker_tmp_dir": "/dev/shm",
}
VERSIONS: list[str] = ["1.0.0", "3.74.4", "21.4.10"]
