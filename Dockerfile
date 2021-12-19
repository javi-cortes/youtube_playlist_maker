FROM python:3.9.5

RUN apt update

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONBUFFERED=1

COPY . /mv_crawler
WORKDIR /mv_crawler/mv_crawler

CMD ["scrapy", "crawl", "mv_spider"]