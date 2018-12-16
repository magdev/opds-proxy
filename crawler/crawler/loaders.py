# -*- coding: utf-8 -*-   
from html2text import html2text
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from crawler.helpers import ParseHelper
from crawler.processors import List


class AuthorItemLoader(ItemLoader):
    default_input_processor = MapCompose(ParseHelper.trim)
    default_output_processor = TakeFirst()
    
    
class CategoryItemLoader(ItemLoader):
    default_input_processor = MapCompose(ParseHelper.trim)
    default_output_processor = TakeFirst()
    
    
class LinkItemLoader(ItemLoader):
    default_input_processor = MapCompose(ParseHelper.trim)
    default_output_processor = TakeFirst()
    format_in = MapCompose(ParseHelper.parse_dl_format)
    url_in = MapCompose(ParseHelper.urlescape)
    
    
class BookItemLoader(ItemLoader):
    default_input_processor = MapCompose(ParseHelper.trim)
    default_output_processor = TakeFirst()
    description_in = MapCompose(html2text, ParseHelper.trim)
    description_out = Join()
    authors_out = List()
    categories_out = List()
    links_out = List()
    