FROM python:3.11-slim-buster

# add /app/src to PYTHONPATH
# ENV PYTHONPATH=/app

# set the working directory
WORKDIR /app

# copy pyproject.toml and poetry.lock into container
COPY pyproject.toml poetry.lock /app/

# install poetry inside container
RUN pip install poetry==1.8.3 

# install python dependencies from pyproject.toml
RUN poetry install

# copy current dir contents into container at /app
COPY . /app

# set the PYTHONPATH to include the src directory
ENV PYTHONPATH=/app

# stream output to console
ENV PYTHONUNBUFFERED=1

# run app
CMD ["sh", "-c", "set -a && . /app/.env && poetry run python src/main.py"]