FROM python:3.11-slim-buster

# install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev

# install poetry
RUN pip install poetry==1.8.3

# set the working directory
WORKDIR /app

# set the PYTHONPATH to include the src directory
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# copy pyproject.toml and poetry.lock into container
COPY pyproject.toml poetry.lock /app/

# install python dependencies from pyproject.toml
RUN poetry install

# copy current dir contents into container at /app
COPY src/*.py /app/src/

# rRun app
CMD ["poetry", "run", "python", "/app/src/main.py"]