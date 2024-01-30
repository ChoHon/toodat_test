FROM python:3.11
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
ADD . /app

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py makemigrations account
RUN python manage.py makemigrations work
RUN python manage.py makemigrations coupon
RUN python manage.py migrate
RUN python manage.py createsuperuser --noinput