FROM python:3.11-slim-buster

# stream output to console
ENV PYTHONUNBUFFERED=1

# install poetry inside container
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

# run app
CMD ["poetry", "run", "python", "/app/src/main.py"]