import os
import json

# Logging
# https://docs.gunicorn.org/en/stable/settings.html#logging
loglevel = os.getenv("LOG_LEVEL", "info")
accesslog = os.getenv("ACCESS_LOG", "-")
errorlog = os.getenv("ERROR_LOG", "-")

# Debugging
# https://docs.gunicorn.org/en/stable/settings.html#debugging
reload = bool(os.getenv("RELOAD", "False"))

# Worker processes
# https://docs.gunicorn.org/en/stable/settings.html#worker-processes
workers = int(os.getenv("WORKERS", "1"))
timeout = int(os.getenv("TIMEOUT", "30"))
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", "30"))
keepalive = int(os.getenv("KEEP_ALIVE", "2"))

# Server machanics
# https://docs.gunicorn.org/en/stable/settings.html?highlight=worker_tmp_dir#worker-tmp-dir
# This is set to /dev/shm to speed up the startup of workers by using a in memory file system
worker_tmp_dir = "/dev/shm"

# Server socket
# https://docs.gunicorn.org/en/stable/settings.html?highlight=bind#bind
bind = os.getenv("BIND", "0.0.0.0:80")

log_data = {
    "bind": bind,
    "workers": workers,
    "timeout": timeout,
    "graceful_timeout": graceful_timeout,
    "keepalive": keepalive,
    "loglevel": loglevel,
    "errorlog": errorlog,
    "accesslog": accesslog,
    "reload": reload,
    "worker_tmp_dir": worker_tmp_dir,
}
print(json.dumps(log_data))
