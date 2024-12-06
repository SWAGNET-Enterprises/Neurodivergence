FROM --platform=$BUILDPLATFORM python:3.12 AS build
RUN mkdir /data
WORKDIR /data
COPY . /data
RUN pip install -r /data/requirements.txt
