# fast-api-multistage-build
This is an example project to demonstrate the use of the uvicorn-gunicorn-poetry image.
It is also used for testing that image.

## Build the image
```shell
docker build --tag fast-api-multistage --target production-image .
```
Build the image with another base image variant:
```shell
docker build --build-arg BASE_IMAGE=pfeiffermax/uvicorn-gunicorn-poetry:3.2.0-python3.10.13-bookworm --tag fast-api-multistage --target production-image .
```

## Run the image
```shell
docker run -it --rm fast-api-multistage
```
