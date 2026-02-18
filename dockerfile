FROM alpine:latest

RUN apk add python

RUN mkdir /app

WORKDIR /app

COPY ./ /app/

ENV PYTHONUNBUFFERED=1

CMD ["python" "main.py" ]
