# -*- coding: utf-8 -*-   
from scrapy import Item, Field
from crawler.helpers import ParseHelper


class AuthorItem(Item):
    name = Field()
    url = Field()
    
    
class CategoryItem(Item):
    name = Field()
    url = Field()

    
class LinkItem(Item):
    url = Field()
    format = Field()
    

class BookItem(Item):
    title = Field()
    summary = Field()
    description = Field()
    image = Field()
    url = Field()
    language = Field(
        serializer = ParseHelper.parse_language
    )
    isbn = Field(
        serializer = ParseHelper.parse_isbn
    )
    authors = Field(
        serializer = AuthorItem
    )
    categories = Field(
        serializer = CategoryItem
    )
    links = Field(
        serializer = LinkItem
    )
    year = Field(
        serializer = ParseHelper.parse_year
    )
    pages = Field(
        serializer = ParseHelper.parse_pages
    )
    
    
    
    
    