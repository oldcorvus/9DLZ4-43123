FROM python:3.10-slim
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/core


RUN apt-get update && \
    apt-get install -y gettext

    COPY core/requirements.txt .
RUN pip install -r requirements.txt

COPY core/ .
