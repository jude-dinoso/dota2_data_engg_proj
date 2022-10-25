# syntax=docker/dockerfile:1

FROM python:3.10.8-slim-buster as base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps
#RUN useradd --create-home appuser
#USER appuser
#WORKDIR /app

#RUN pip install pipenv
#RUN apt-get update && apt-get install -y --no-install-recommends gcc

WORKDIR /app
COPY . ./
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Copy virtual env from python-deps stage
#COPY  /venv /venv
#ENV PATH="/venv/bin:$PATH"

# Create and switch to a new user
RUN file="$(ls -1 /app)" && echo $file

# Install application into container
CMD ["python3", "test.py"]
