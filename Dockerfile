FROM python:3.11.0-slim

WORKDIR /usr/src/app

RUN apt update && apt install -y git
COPY backend/requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt
COPY backend /usr/src/app
COPY .git /usr/src/app/.git
RUN flask --app vapehookah db init
RUN flask --app vapehookah db migrate
RUN flask --app vapehookah db upgrade