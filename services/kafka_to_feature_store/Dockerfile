FROM python:3.11-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry==1.8.3

# Set the working directory
WORKDIR /app

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# Copy pyproject.toml and poetry.lock into container
COPY pyproject.toml poetry.lock /app/

# Install python dependencies from pyproject.toml
RUN poetry install

# Copy current dir contents into container at /app
COPY src/*.py /app/src/

# Run app
CMD ["poetry", "run", "python", "/app/src/main.py"]