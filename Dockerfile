FROM python:3.6.3

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
WORKDIR /code/knowledgebase
USER uwsgi
