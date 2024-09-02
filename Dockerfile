FROM python:3.11-slim
WORKDIR /root/src

# TODO: Название проекта
COPY . bia_incident
RUN pip install poetry

WORKDIR /root/src/bia_incident
RUN POETRY_VIRTUALENVS_CREATE=false poetry install && rm -rf /root/.cache/pypoetry/*

EXPOSE 9090
