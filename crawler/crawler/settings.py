# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# DJANGO INTEGRATION
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'base.settings'
django.setup()
# DJANGO INTEGRATION

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = os.environ.get('OPDSPROXY_SCRAPY_USER_AGENT', 'OPDS-Proxy-Crawler (+http://dev.example.com)')

# Obey robots.txt rules
ROBOTSTXT_OBEY = bool(os.environ.get('OPDSPROXY_SCRAPY_ROBOTSTXT_OBEY', True))

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = int(os.environ.get('OPDSPROXY_SCRAPY_CONCURRENT_REQUESTS', 2))

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = int(os.environ.get('OPDSPROXY_SCRAPY_DOWNLOAD_DELAY', 3))

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = int(os.environ.get('OPDSPROXY_SCRAPY_CONCURRENT_REQUESTS_PER_DOMAIN', 4))
#CONCURRENT_REQUESTS_PER_IP = int(os.environ.get('OPDSPROXY_SCRAPY_CONCURRENT_REQUESTS_PER_IP', 4)

# Disable cookies (enabled by default)
COOKIES_ENABLED = bool(os.environ.get('OPDSPROXY_SCRAPY_COOKIES_ENABLED', False))

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = bool(os.environ.get('OPDSPROXY_SCRAPY_TELNETCONSOLE_ENABLED', False))

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawler.pipelines.CrawlerPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = bool(os.environ.get('OPDSPROXY_SCRAPY_AUTOTHROTTLE_ENABLED', True))
# The initial download delay
AUTOTHROTTLE_START_DELAY = int(os.environ.get('OPDSPROXY_SCRAPY_AUTOTHROTTLE_START_DELAY', 3))
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = int(os.environ.get('OPDSPROXY_SCRAPY_AUTOTHROTTLE_MAX_DELAY', 30))
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = float(os.environ.get('OPDSPROXY_SCRAPY_AUTOTHROTTLE_TARGET_CONCURRENCY', 1.0))
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = bool(os.environ.get('OPDSPROXY_SCRAPY_AUTOTHROTTLE_DEBUG', False))

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = bool(os.environ.get('OPDSPROXY_SCRAPY_HTTPCACHE_ENABLED', True))
HTTPCACHE_EXPIRATION_SECS = int(os.environ.get('OPDSPROXY_SCRAPY_HTTPCACHE_EXPIRATION_SECS', 21600))
HTTPCACHE_DIR = os.environ.get('OPDSPROXY_SCRAPY_HTTPCACHE_DIR', 'httpcache')
HTTPCACHE_IGNORE_HTTP_CODES = [] #os.environ.get('OPDSPROXY_SCRAPY_HTTPCACHE_IGNORE_HTTP_CODES', '').split(',')
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


LOG_ENABLED = bool(os.environ.get('OPDSPROXY_SCRAPY_LOG_ENABLED', True))
LOG_FILE = os.environ.get('OPDSPROXY_SCRAPY_LOG_FILE', 'scrapy.log')

