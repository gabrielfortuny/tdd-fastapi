# pull official base image
FROM python:3.14-slim-bookworm

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
ENV UV_NO_DEV=1
COPY . .
RUN uv sync --locked
ENV PATH="/usr/src/app/.venv/bin:$PATH"
