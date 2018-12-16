# -*- coding: utf-8 -*-

# Settings for catalog app
import os
import socket

SCRAPY_SOCKET = ('localhost', 6800)

CATALOG_HOST = os.environ.get('OPDSPROXY_HTTP_HOST', socket.gethostname())
CATALOG_PORT = os.environ.get('OPDSPROXY_HTTP_PORT', '8000')
CATALOG_PROTOCOL = os.environ.get('OPDSPROXY_HTTP_PROTOCOL', 'http')

CATALOG_SOCKET = CATALOG_HOST + ':' + CATALOG_PORT
CATALOG_BASE_URL = CATALOG_PROTOCOL + '://' + CATALOG_HOST + ':' + CATALOG_PORT

CATALOG_PAGE_LIMIT = int(os.environ.get('OPDSPROXY_CATALOG_PAGE_LIMIT', 25))

CRAWLER_ALLOWED_DOMAINS = os.environ.get('OPDSPROXY_CRAWLER_ALLOWED_DOMAINS', 'www.allitebooks.com').split(',')
CRAWLER_START_URLS = os.environ.get('OPDSPROXY_CRAWLER_START_URLS', 'http://www.allitebooks.com').split(',')
CRAWLER_EXISTING_THRESHOLD = 25