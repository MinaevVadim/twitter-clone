FROM python:3.10.6

RUN mkdir /my_application

WORKDIR /my_application

ADD requirements.prod.txt /my_application

RUN pip install -r requirements.prod.txt

ADD . /my_application

EXPOSE 5000

ENTRYPOINT ["python", "main.py"]
