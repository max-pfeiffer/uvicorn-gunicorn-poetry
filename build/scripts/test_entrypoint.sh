#!/bin/sh
# Please be aware that dash is default shell for Alpine Linux which is used as OS for this image
# http://gondor.apana.org.au/~herbert/dash/

set -e

echo "Activating virtual environment..."
. /application_root/.venv/bin/activate

# Evaluating passed CMD
echo "Running pytest..."
pytest "$@"

# user 'docker run -v' to get /test_coverage_reports/coverage.xml file for exposing this as artifact for GitLab UI, see:
# https://docs.gitlab.com/ee/user/project/merge_requests/test_coverage_visualization.html#python-example
# https://docs.docker.com/engine/reference/commandline/run/#mount-volume--v---read-only

echo "Creating test coverage report..."
coverage xml -o /test_coverage_reports/coverage.xml
