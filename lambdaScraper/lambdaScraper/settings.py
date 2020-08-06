# Scrapy settings for lambdaScraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lambdaScraper'

SPIDER_MODULES = ['lambdaScraper.spiders']
NEWSPIDER_MODULE = 'lambdaScraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'lambdaScraper (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'lambdaScraper.middlewares.LambdascraperSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'lambdaScraper.middlewares.LambdascraperDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'lambdaScraper.pipelines.S3Pipeline': 1,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

HTTPCACHE_ENABLED = False
# HTTPCACHE_EXPIRATION_SECS = 60 * 60 * 24 * 1
# HTTPCACHE_DIR = 'httpcache'
# CLOSESPIDER_PAGECOUNT = 32
# HTTPCACHE_IGNORE_HTTP_CODES = [301, 302]

SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'
CONCURRENT_REQUESTS = 32
# REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'DEBUG'
COOKIES_ENABLED = False
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 30
REDIRECT_ENABLED = Trueut
#REDIRECT_MAX_TIMES = 1to
# AJAXCRAWL_ENABLED = True

# # Configure a delay for requests for the same website(default: 0)
# # See https: // docs.scrapy.org/en/latest/topics/settings.html  # download-delay
# # See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# # The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 5

# DEPTH_LIMIT = 3
AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 2
# AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 3
# AUTOTHROTTLE_DEBUG = True
REACTOR_THREADPOOL_MAXSIZE = 32
RANDOMIZE_DOWNLOAD_DELAY = True
TELNETCONSOLE_ENABLED=False
REDIRECT_PRIORITY_ADJUST = -1
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
DOWNLOAD_MAXSIZE = 1048576
DOWNLOAD_WARNSIZE = 0