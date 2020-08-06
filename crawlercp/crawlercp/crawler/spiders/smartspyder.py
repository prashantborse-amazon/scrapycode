#-*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os

class SmartspyderSpider(CrawlSpider):
    name = "smartspyder"
    def __init__(self, *args, **kwargs):
        """
        simple init to set the default variables
        """

        super(SmartspyderSpider, self).__init__(*args, **kwargs)
        print(kwargs)
        self.start_urls = [kwargs.get('start_urls','')]
        self.allowed_domains = [kwargs.get('allowed_domains', '')]
        self.downloadfolder = os.path.join(kwargs.get('downloadfolder', '/testresults/'),
                                        self.allowed_domains[0])
        if not os.path.exists(self.downloadfolder):
            os.makedirs(self.downloadfolder)
        self.textextract = kwargs.get('textextract', False)
    rules = [Rule(LinkExtractor(), callback='download', follow=True)]

    def download(self, response):
        """
        Download the html files only
        """
        if b'text/html' in response.headers.get('Content-Type',''):
            print(response.url)
            filename = response.url.replace("/","$").replace(":","!").replace("?","_")
            if len(filename)>100 :
                filename = filename[:99]
            with open(os.path.join(self.downloadfolder, str(filename)+'.html'), 'wb') as f:
                f.write(response.body)
            if self.textextract:
                with open(os.path.join(self.downloadfolder, str(filename)+'.dat'), 'w', encoding='utf-8') as f:
                    f.write(response.xpath('//title/text()').get())
                    f.write('\n'.join(response.xpath('//body//text()').extract()))
