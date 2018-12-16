# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from catalog import settings
from crawler.items import BookItem, AuthorItem, CategoryItem, LinkItem
from crawler.loaders import BookItemLoader, AuthorItemLoader, CategoryItemLoader, LinkItemLoader
from catalog.models import Book
from scrapy.exceptions import CloseSpider

class AllitebooksComSpider(CrawlSpider):
    name = 'allitebooks_com'
    allowed_domains = settings.CRAWLER_ALLOWED_DOMAINS
    start_urls = settings.CRAWLER_START_URLS
    existing_counter = 0
    
    def parse(self, response):
        for url in response.css('article .entry-title a::attr(href)').extract():
            try:
                if Book.objects.filter(url = url).exists():
                    self.logger.info('Skip existing URL: %s' % url)
                    self.existing_counter += 1
                    if self.existing_counter == settings.CRAWLER_EXISTING_THRESHOLD:
                        raise CloseSpider('Existing item threshold reached, aborting')
                else:
                    yield scrapy.Request(url, callback = self.parse_details, errback = self.handle_error)
            except Book.DoesNotExist:
                yield scrapy.Request(url, callback = self.parse_details, errback = self.handle_error)

        next_url = response.css('link[rel="next"]::attr(href)').extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url, callback = self.parse, errback = self.handle_error)

    def parse_details(self, response):
        b = BookItemLoader(BookItem(), response)
        b.add_value('url', response.url)
        b.add_css('title', '.entry-header h1::text')
        b.add_css('summary', '.entry-header h4::text')
        b.add_css('summary', 'meta[name="description"]::attr(content)')
        b.add_css('description', 'article .entry-content *')
        b.add_css('isbn', 'article .book-detail dd:nth-child(4)::text')
        b.add_css('language', 'article .book-detail dd:nth-child(10)::text')
        b.add_css('year', 'article .book-detail dd:nth-child(6)::text')
        b.add_css('pages', 'article .book-detail dd:nth-child(8)::text')
        b.add_css('image', 'article .entry-body-thumbnail img::attr(src)')

        for author in response.css('article .book-detail dd:nth-child(2) a[rel="tag"]'):
            a = AuthorItemLoader(AuthorItem(), author)
            a.add_css('name', '::text')
            a.add_css('url', '::attr(href)')
            b.add_value('authors', a.load_item())

        for category in response.css('article .book-detail dd:last-child a'):
            c = CategoryItemLoader(CategoryItem(), category)
            c.add_css('name', '::text')
            c.add_css('url', '::attr(href)')
            b.add_value('categories', c.load_item())

        for link in response.css('article .download-links a'):
            l = LinkItemLoader(LinkItem(), link)
            l.add_css('url', '::attr(href)')
            l.add_css('format', '::attr(href)')
            b.add_value('links', l.load_item())

        yield b.load_item()

    def handle_error(self, failure):
        self.logger.error(repr(failure))
        
