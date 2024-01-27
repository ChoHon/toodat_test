FROM python:3.11
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y install vim && apt-get clean
RUN mkdir /app
ADD . /app

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver"]