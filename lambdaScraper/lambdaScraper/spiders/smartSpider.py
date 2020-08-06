import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class ScraperItem(scrapy.Item):
    # The source URL
    url_from = scrapy.Field()
    # The destination URL
    url_to = scrapy.Field()


class FastScraper(CrawlSpider):
    name = "fscraper"

    def __init__(self, *args, **kwargs):
        super(FastScraper, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', '').split('|')
        self.allowed_domains = kwargs.get('allowed_domains', '').split('|')

    rules = [Rule(LinkExtractor(), callback='parse_items', follow=True)]

    # # Method which starts the requests by visiting all URLs specified in start_urls
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items

    def parse_items(self, response):
        # The list of items that are found on the particular page
        items = []
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(
            canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                item = ScraperItem()
                item['url_from'] = response.url
                item['url_to'] = link.url
                items.append(item)
        # Return all the found items
        return items
