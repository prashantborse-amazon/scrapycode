import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
from io import BytesIO
import boto3
from urllib.parse import urlparse
from tld import get_tld
from datetime import datetime
from scrapy.http import Request

s3Client = boto3.client('s3')
# Versionning
__version__ = "0.1.0"


class CrawlerSpider(CrawlSpider):
    name = 'crawler'

    def __init__(self, *args, **kwargs):
        # settings.overrides['DEPTH_LIMIT'] = 3
        # super(CrawlerSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('url', '')]
        # self.allowed_domains = kwargs.get('allowed_domains', '').split('|')
        hostname = self.getHostName(self.start_urls[0])
        self.allowed_domains = [hostname]
        self.s3 = boto3.client('s3')
        self.S3HtmlBucket = os.getenv('S3_HTML_BUCKET', 'scraped-data-abvin-1')
        # self.loadEnvironmentVars(**kwargs)
        # self.loadUrls()

        # self.downloadfolder = os.path.join(kwargs.get('downloadfolder', 'c:\\temp\\downloads'),
        #                                    self.allowed_domains[0])
        # self.downloadfolder = os.path.join(os.path.join(os.getcwd(), "files"))
        # if not os.path.exists(self.downloadfolder):
        #     os.makedirs(self.downloadfolder)

        print(self.allowed_domains)
        self.rules = []
        self.rules.append(
            Rule(LinkExtractor(allow=r'.+\.(html|htm)$', allow_domains=[hostname]), callback='download', follow=True))

        # self.rules = [Rule(LinkExtractor(),
        #                    callback='download', follow=True)]
        super().__init__()

    def parse(self, response):
        print ("request self.start_urls[0] = ", self.start_urls[0])
        yield Request(
            'http://abc.xyz',
            method='GET',
            headers={'Content-Type': response.headers['Content-Type']},
            body=response.body,
            callback=self.download(response)
        )

    def download(self, response):
        print ("-------> response.url =>", response.request.url)
        # check if it's an html document
        if b'text/html' in response.headers.get('Content-Type', ''):
            # # unable to save file if filename length exceeds the limit
            filename = response.request.url.replace(
                "/", "_2F").replace(":", "_3A").replace("?", "_")
            # unable to save file if filename length exceeds the limit
            if len(filename) > 1000:
                filename = filename[:1000]

            # Get the root as an object
            hostname = self.getHostName(response.request.url)

            if hostname not in self.allowed_domains:
                print(f'Hostname {hostname} does not exist in allowed domains')
                return

            # write file
            if is_in_aws():
                # write to S3 bucket
                folderSuffix = datetime.today().strftime('%Y%m%d')
                s3Path = f'CRAWLED_{folderSuffix}/{hostname}/{filename}'
                self.writeToS3(response, s3Path)
                self.logger.info(
                    f'Downloading url {response.url} to S3: {s3Path}')
            else:
                folderPath = os.path.join(
                    os.getcwd(), 'lambdaScraper/files', f'{hostname}')
                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)
                filePath = os.path.join(folderPath, f'{filename}.html')
                with open(filePath, 'wb') as f:
                    f.write(response.body)
                    self.logger.info(
                        f'Downloading url {response.url} to local:{filePath}')

    def writeToS3(self, response, filename):
        buf = BytesIO(response.body)
        self.s3.put_object(
            Body=buf, Bucket=self.S3HtmlBucket, Key=f'{filename}.html')

    # def loadEnvironmentVars(self, **kwargs):
    #     self.S3HtmlBucket = os.getenv('S3_HTML_BUCKET', 'scraped-data-abvin-1')
        # self.S3UrlFileBucket = os.getenv(
        #     'S3_URL_FILE_BUCKET', 'scrapy-url-load')
        # self.S3UrlFileKey = os.getenv('S3_URL_FILE_KEY', 'urls.txt')

    # def loadUrls(self):
    #     if is_in_aws():
    #         s3 = boto3.resource('s3')
    #         obj = s3.Object(self.S3UrlFileBucket, self.S3UrlFileKey)
    #         self.start_urls = obj.get()['Body'].read().decode(
    #             'utf-8').splitlines()
    #     else:
    #         with open(os.path.join(os.getcwd(), "lambdaScraper/spiders/urls.txt")) as f:
    #             self.start_urls = f.read().splitlines()
    #     allowedDomains = []
    #     for url in self.start_urls:
    #         allowedDomains.append(self.getHostName(url))
    #     self.allowed_domains = allowedDomains
    #     print(allowedDomains)

    # def getHostName(self, url):
    #     hostname = urlparse(url).hostname
    #     if hostname is None:
    #         print(f'No hostname for {url}')
    #     if hostname is not None and hostname.startswith('www.'):
    #         hostname = hostname.replace('www.', '')
    #     return hostname

    def getHostName(self, url):
        res = get_tld(url, as_object=True)
        self.logger.info(f'Hostname: {res.fld}')
        hostname = res.fld
        return hostname


def is_in_aws():
    return os.getenv('AWS_EXECUTION_ENV') is not None
