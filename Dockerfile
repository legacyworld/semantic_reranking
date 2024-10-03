FROM python:3.12.6-bullseye
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt