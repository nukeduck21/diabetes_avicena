# syntax=docker/dockerfile:1

FROM python:3.9.13-slim-buster

WORKDIR /diabetes-client-docker

ADD api api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "main.py", "--bind=0.0.0.0:8080"]