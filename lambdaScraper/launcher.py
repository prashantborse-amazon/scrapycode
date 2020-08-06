import sys
import json

from lambdaScraper.crawl import crawl


def scrape(event={}, context={}):
    crawl(start_urls='https://www.factset.com', allowed_domains='factset.com')


if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
