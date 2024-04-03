FROM python:3.10

WORKDIR /app

COPY /my_application/requirements.dev.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY /my_application .
