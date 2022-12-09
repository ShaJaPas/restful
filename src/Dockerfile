FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN pip install poetry

COPY . /usr/src/app

RUN poetry install

EXPOSE 8000