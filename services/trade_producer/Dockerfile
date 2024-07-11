FROM python:3.11-slim-buster

# # add /app/src to PYTHONPATH
# ENV PYTHONPATH=/app

# stream output to console
ENV PYTHONUNBUFFERED=1

# install poetry inside container
RUN pip install poetry==1.8.3

# set the working directory
WORKDIR /app

# copy pyproject.toml and poetry.lock into container
COPY pyproject.toml poetry.lock /app/

# install python dependencies from pyproject.toml
RUN poetry install

CMD ["poetry", "run", "python", "src/main.py"]