FROM python:3.13.0-alpine3.20

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
COPY ./app /app
COPY ./start.sh /start.sh
COPY ./populate_db.py /populate_db.py

RUN chmod +x /start.sh

RUN adduser -D user
USER user