FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

WORKDIR /

COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

COPY . .

VOLUME /hostpipe

CMD python core.py