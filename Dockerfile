ARG virtual_env=/venv

FROM python:3.11-slim as base

ENV VIRTUAL_ENV=$virtual_env \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.2 \
    PATH="$virtual_env:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install "poetry==$POETRY_VERSION"
# RUN apt-get update && apt-get install -y ffmpeg
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

COPY entrypoint.sh /entrypoint
COPY timelapse.py .

ENTRYPOINT ["/entrypoint"]
CMD ["timelapse"]
