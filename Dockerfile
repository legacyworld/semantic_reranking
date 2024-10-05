FROM python:3.11.10-slim
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install curl