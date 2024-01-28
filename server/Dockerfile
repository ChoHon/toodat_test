FROM python:3.11
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
ADD . /app

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt