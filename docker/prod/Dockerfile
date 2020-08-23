# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

RUN apk update && apk upgrade \
    && apk add musl-dev \
        gcc \
        linux-headers \
        gettext-dev
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/base.txt .
COPY ./requirements/production.txt .

RUN pip install -r production.txt

# copy project
COPY . .

ENTRYPOINT ["/home/app/web/docker/entrypoint.sh"]