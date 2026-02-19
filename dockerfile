FROM alpine:latest

RUN apk add python3

RUN mkdir /app
RUN mkdir /app/files
RUN mkdir /defaults

WORKDIR /app

COPY main.py .
COPY entrypoint.sh .
COPY files/auth.json.example /defaults/

RUN ln -s /app/main.py /usr/local/bin/
RUN ln -s /app/entrypoint.sh /usr/local/bin/
RUN chmod +x /app/entrypoint.sh

ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "entrypoint.sh" ]
