from scrapy.exceptions import IgnoreRequest

class FilterRequests():

    def __init__(self):
        self.crawled_urls = set()

    def process_request(self, request, spider):
        if request.url in self.crawled_urls:
            raise IgnoreRequest()
        else:
            return None