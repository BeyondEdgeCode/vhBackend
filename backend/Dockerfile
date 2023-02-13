FROM python:3.11.0-slim-buster

WORKDIR /usr/src/app

ENV FLASK_APP=vapehookah
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt
CMD ["python3.11", "-m", "flask", "db", "init"]
CMD ["python3.11", "-m", "flask", "db", "upgrade"]
CMD ["python3.11", "-m", "flask", "db", "migrate"]
COPY . /usr/src/app