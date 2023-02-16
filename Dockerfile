FROM python:3.11.0-alpine

WORKDIR /usr/src/app

RUN apk update && apk add git
RUN pip3 install -r requirements.txt
COPY backend/requirements.txt /usr/src/app/requirements.txt
COPY backend /usr/src/app
COPY .git /usr/src/app/.git