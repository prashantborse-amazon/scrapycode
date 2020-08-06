import sys
import imp
import os
import logging
import boto3
from urllib.parse import urlparse

from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Need to "mock" sqlite for the process to not crash in AWS Lambda / Amazon Linux
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")


def is_in_aws():
    return os.getenv('AWS_EXECUTION_ENV') is not None


def crawl(**spider_kwargs):
    spiderName = "crawler"
    settings = {}
    project_settings = get_project_settings()
    spiderLoader = SpiderLoader(project_settings)

    spider_cls = spiderLoader.load(spiderName)

    try:
        spider_key = urlparse(spider_kwargs.get("start_urls")[0]).hostname if spider_kwargs.get(
            "start_urls") else urlparse(spider_cls.start_urls[0]).hostname
    except Exception:
        logging.exception("Spider or kwargs need start_urls.")

    if is_in_aws():
        # Lambda can only write to the /tmp folder.
        settings['HTTPCACHE_DIR'] = "/tmp"
    # else:
    #     feed_uri = "file://{}/%(name)s-{}-%(time)s.json".format(
    #         os.path.join(os.getcwd(), "feed"),
    #         spider_key,
    #     )

    # settings['FEED_URI'] = feed_uri
    # settings['FEED_FORMAT'] = feed_format

    # set depth limit parameter here
    settings['DEPTH_LIMIT'] = 0

    S3UrlFileBucket = os.getenv('S3_URL_FILE_BUCKET', 'scrapy-url-load')
    S3UrlFileKey = os.getenv('S3_URL_FILE_KEY', 'urls.txt')

    start_urls = []
    if is_in_aws():
        s3 = boto3.resource('s3')
        obj = s3.Object(S3UrlFileBucket, S3UrlFileKey)
        start_urls = obj.get()['Body'].read().decode(
            'utf-8').splitlines()
    else:
        with open(os.path.join(os.getcwd(), "lambdaScraper/urls/load-urls_8.txt")) as f:
            start_urls = f.read().splitlines()

    process = CrawlerProcess({**project_settings, **settings})
    for url in start_urls:
        print(f'Processing url: {url}')
        process.crawl(spider_cls, url=url)

    process.start()
