FROM python:3.11-alpine
WORKDIR /root/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache bash && rm -rf /var/cache/apk/*
RUN python -m pip install --upgrade pip

COPY . src
RUN pip install poetry

WORKDIR /root/src/src
RUN POETRY_VIRTUALENVS_CREATE=false poetry install && rm -rf /root/.cache/pypoetry/*

EXPOSE 9090

RUN chmod +x /root/src/src/bin/start-app.sh
ENTRYPOINT ["/root/src/src/bin/start-app.sh"]
