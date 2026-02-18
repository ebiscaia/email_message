FROM alpine:latest

RUN apk add python

RUN mkdir /app

WORKDIR /app

COPY ./ /app/

RUN ln -s /app/main.py /usr/local/bin/

ENV PYTHONUNBUFFERED=1

CMD [ "main.py" ]
