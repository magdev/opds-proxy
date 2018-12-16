# -*- coding: utf-8 -*-
import uuid
from django.conf import settings
from django.utils import timezone
from scrapy.exceptions import DropItem
from catalog.models import Book, Link, Author, Category

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    
        
    def close_spider(self, spider):
        fh = open(settings.BASE_DIR + '/scrapy-lastrun.txt', 'w+')
        fh.write(str(timezone.now()))
        fh.close()
        
    def process_item(self, item, spider):
        if item['url'] is None:
            raise DropItem("Missing URL in %s, skipping" % item)
        if not item['links']:
            raise DropItem("Item has no downloadable links: %s, skipping" % item)
        
        if Book.objects.filter(url = item['url']).exists() is False:
            book = Book()
            book.uuid = uuid.uuid1()
            book.title = item['title']
            book.isbn = item['isbn']
            book.pages = item['pages']
            book.year = item['year']
            book.url = item['url']
            book.image = item['image']
            book.language = item['language']
            book.summary = item['summary']
            book.description = item['description']
            book.save();
            
            for author in item['authors']:
                a = Author.objects.get_or_create(
                    name = author['name'],
                    url = author['url']
                )[0]
                a.save()
                book.authors.add(a)
            
            for category in item['categories']:
                c = Category.objects.get_or_create(
                    name = category['name'],
                    url = category['url']
                )[0]
                c.save()
                book.categories.add(c)
            
            for link in item['links']:
                l = Link.objects.get_or_create(
                    book = book,
                    url = link['url'],
                    format = link['format']
                )[0]
                l.save()
            book.save();
        return item
    