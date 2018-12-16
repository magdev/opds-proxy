# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*- 
import os
import re


class ParseHelper():
    
    @staticmethod
    def parse_year(year):
        if not re.match('^[0-9-]{4}$', year):
            if re.match('^([a-zA-Z]+)\s([0-9-]+),\s([0-9-]+)$', year):
                year = year.split(',')[-1].strip()
            elif re.match('^[0-9-]{5,}$', year):
                year = year[:4]
            elif re.match('^([0-9-]{2}).([0-9-]{2}).([0-9-]{4})$', year):
                year = re.split('\D', year)[-1].strip()
            else:
                year = 0
        return int(year)
    
    @staticmethod
    def parse_pages(pages):
        if not re.match('^[\d]+$', pages):
            if re.match('^([a-zA-Z]+)[\s\|]+([\d]+)$', pages): 
                pages = pages.split('|')[-1].strip()
            else:
                pages = 0
        return int(pages)
    
    @staticmethod 
    def parse_dl_format(url):
        if url:
            ext = os.path.splitext(url)[1]
            return ext.strip(' .').upper()
        return url
    
    @staticmethod 
    def trim(text):
        if text:
            return str(text).strip()
        return text
    
    @staticmethod 
    def urlescape(url):
        if url:
            return str(url).replace(' ', '%20')
        return url
    
    @staticmethod 
    def parse_isbn(isbn):
        if isbn:
            return str(isbn).replace('-', '')
        return isbn
    
    @staticmethod 
    def parse_language(lang):
        switcher = {
            'english': 'en',
            'german': 'de',
            'french': 'fr',
        }
        return switcher.get(lang.lower(), 'en')
    