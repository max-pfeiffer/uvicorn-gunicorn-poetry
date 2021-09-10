#!/bin/sh

set -e

echo "Activating virtual environment..."
. /application_root/.venv/bin/activate

# Start Gunicorn
exec gunicorn -k uvicorn.workers.UvicornWorker -c /application_server/gunicorn_configuration.py app.main:app
