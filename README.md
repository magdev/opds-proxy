# All IT-Ebooks.com OPDS-Proxy

Browse http://www.allitebooks.com using your favourite OPDS-capable Ebook-Reader.

## Installation

```bash
git clone git@github.com:magdev/allitebooks.com-opds-proxy.git
pip install -r requirements.txt
bower install
./manage migrate
./manage collectstatic
./manage runserver
```

### Using Docker

```bash
docker run -d --name="opds-proxy" -v opds_data:/app/data -p 8008:80 -p 6800:6800 magdev3/opds-proxy:latest
```

## Crawling

```bash
cd crawler/
scrapy crawl bookcrawler
```

## Configuration

OPDS-Proxy and Scrapy are highly configurable using Environment-Variables.

### Crawler configuration

```bash
OPDSPROXY_CRAWLER_ALLOWED_DOMAINS="www.allitebooks.com" 
OPDSPROXY_CRAWLER_START_URLS="http://www.allitebooks.com" 
```

### Django configuration

```bash
OPDSPROXY_DEBUG=True
OPDSPROXY_SECRET_KEY="!yourverysecretkey-change-it!"
OPDSPROXY_ALLOWED_HOSTS="127.0.0.1,0.0.0.0"
OPDSPROXY_DB_ENGINE="django.db.backends.sqlite3"
OPDSPROXY_DB_NAME="${BASE_DIR}/db.sqlite3"
OPDSPROXY_DB_USER=""
OPDSPROXY_DB_PASS=""
OPDSPROXY_DB_HOST=""
OPDSPROXY_DB_PORT=""
OPDSPROXY_LANGUAGE_CODE="en-US"
OPDSPROXY_TIME_ZONE="UTC"
```

### Scrapy configuration

```bash
OPDSPROXY_SCRAPY_USER_AGENT="OPDS-Proxy-Crawler (+http://dev.example.com)"
OPDSPROXY_SCRAPY_ROBOTSTXT_OBEY=True
OPDSPROXY_SCRAPY_CONCURRENT_REQUESTS=2
OPDSPROXY_SCRAPY_DOWNLOAD_DELAY=3
OPDSPROXY_SCRAPY_CONCURRENT_REQUESTS_PER_DOMAIN=4
OPDSPROXY_SCRAPY_COOKIES_ENABLED=False
OPDSPROXY_SCRAPY_TELNETCONSOLE_ENABLED=False
OPDSPROXY_SCRAPY_AUTOTHROTTLE_ENABLED=True
OPDSPROXY_SCRAPY_AUTOTHROTTLE_START_DELAY=3
OPDSPROXY_SCRAPY_AUTOTHROTTLE_MAX_DELAY=30
OPDSPROXY_SCRAPY_AUTOTHROTTLE_TARGET_CONCURRENCY=2.0
OPDSPROXY_SCRAPY_AUTOTHROTTLE_DEBUG=False
OPDSPROXY_SCRAPY_HTTPCACHE_ENABLED=True
OPDSPROXY_SCRAPY_HTTPCACHE_EXPIRATION_SECS=86400
OPDSPROXY_SCRAPY_HTTPCACHE_IGNORE_HTTP_CODES=""
OPDSPROXY_SCRAPY_LOG_ENABLED=True
```

### Docker only configuration

```bash
OPDSPROXY_HTTP_PORT=80
```

## To-Do

 * Write full README
 + Add Docker
