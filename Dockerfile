# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /vhBackend

ENV FLASK_APP = vapehookah
ENV FLASK_ENV = development
ENV FLASK_DEBUG = 1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3.11", "-m" , "flask", "run", "--host=0.0.0.0", "-p 8001"]