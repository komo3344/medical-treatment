FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app/
RUN python3 -m pip install -r requirements.txt