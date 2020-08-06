FROM python:3.7

WORKDIR /usr/src/app

COPY scrapy.cfg ./
COPY launcher.py ./
COPY lambdaScraper ./lambdaScraper
COPY requirements.txt ./

RUN pip install -r requirements.txt --quiet

CMD ["python3", "./launcher.py"]