FROM python:3.11-slim
WORKDIR /root/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libc-dev \
    libffi-dev \
    python3-dev \
    g++ \
    swig \
    bash \
    netcat-traditional \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip

COPY . src
RUN pip install poetry

WORKDIR /root/src/src
RUN POETRY_VIRTUALENVS_CREATE=false poetry install && rm -rf /root/.cache/pypoetry/*

EXPOSE 9090

RUN chmod +x /root/src/src/bin/start-app.sh
ENTRYPOINT ["/root/src/src/bin/start-app.sh"]
