from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os


class MainSpider(CrawlSpider):
    name = "mainSpider"

    def __init__(self, category=None, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.factset.com"]
        self.allowed_domains = ["factset.com"]
        self.downloadPath = '/c/repo/factset/scrapedData'
        if not os.path.exists(self.downloadPath):
            os.mkdir(self.downloadPath)

        rules = [  # Get all links on start url
            Rule(
                LinkExtractor(),
                follow=True,
                callback="downloadPage",
            )
        ]

    def downloadPage(self, response):
        # if b'text/html' in response.headers.get('Content-Type', ''):
        filename = response.url.replace(
            "/", "$").replace(":", "-").replace("?", "_")
        if len(filename) > 100:
            filename = filename[:99]
        print(f'{filename}.html')

        with open(filename, 'wb') as f:
            f.write(response.body)
            self.log('Saved file %s' % filename)

        with open(os.path.join(self.downloadPath, f'{filename}.html'), 'wb') as d_file:
            d_file.write(response.body)
