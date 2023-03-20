# syntax=docker/dockerfile:1

FROM python:3.10.8-slim-buster as base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

WORKDIR /app
COPY . ./
COPY Pipfile Pipfile.lock ./
RUN curl -sSL https://install.python-poetry.org | python3 - --yes

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser


# Create and switch to a new user
RUN file="$(ls -1 /app)" && echo $file

# Install application into container
CMD ["python3", "test.py"]
