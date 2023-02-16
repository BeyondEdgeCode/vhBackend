FROM python:3.11.0-alpine

WORKDIR /usr/src/app

COPY backend/requirements.txt /usr/src/app/requirements.txt
RUN apk update
RUN apk add git
RUN pip3 install -r requirements.txt
COPY backend /usr/src/app
COPY .git /usr/src/app/