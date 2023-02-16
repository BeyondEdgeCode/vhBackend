FROM python:3.11.0-slim-buster

WORKDIR /usr/src/app

ENV FLASK_APP=vapehookah
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

COPY backend/requirements.txt /usr/src/app/requirements.txt
RUN apk update
RUN apk add git
RUN pip3 install -r requirements.txt
COPY backend /usr/src/app
COPY .git /usr/src/app/.git