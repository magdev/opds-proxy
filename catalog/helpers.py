# -*- coding: utf-8 -*-
import hashlib
import os
import socket
import json
from builtins import ValueError
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.urls.base import reverse
from catalog import settings as appcfg
from catalog.models import FeedUuid
from catalog.utils.feedgenerator import OpdsNavigationFeed


class NavigationHelper():
    __nav = None
    
        
    @classmethod
    def is_dynamic_section(self, section):
        if self.__nav[section] is None:
            raise ValueError('Unknown navigation section: %s' % section)
        return self.__nav['section']['dynamic']
        
    @classmethod
    def get_nav_entries(self, section):
        if self.__nav is None:
            file = settings.BASE_DIR + '/catalog/nav.json'
            with open(file) as json_file:
                self.__nav = json.load(json_file)
                
        if self.__nav[section] is None:
            raise ValueError('Unknown navigation section: %s' % section)
        
        entries = []
        for entry in self.__nav[section]['entries']:
            entry['uuid'] = ViewHelper.get_feed_uuid(entry['uuid_key']),
            entries.append(entry)
        return entries
        
    @staticmethod
    def get_uuid_key(keytext):
        return hashlib.md5(keytext.encode()).hexdigest()
    
    @staticmethod
    def get_navigation_feed(uuid, url, title, subtitle = '', up_url = ''):
        f = OpdsNavigationFeed(
            root_url = reverse('root'),
            search_url = reverse('search') + '?q={searchTerms}',
            feed_icon = 'http://www.allitebooks.com/wp-content/themes/allitebooks/images/favicon.ico',
            updated = ScrapyHelper.get_last_run_iso(),
            link = None,
            description = None,
            feed_rights = None,
            title = title,
            subtitle = subtitle,
            id = uuid,
            feed_url = url,
            up_url = up_url,
        )
        return f
    
class ViewHelper():
    
    @staticmethod
    def get_feed_uuid(name):
        obj = FeedUuid.objects.get_or_create(feed = name)[0];
        return 'urn:uuid:' + str(obj.uuid)

    

class ScrapyHelper():
    last_run = None
    file = settings.BASE_DIR + '/scrapy-lastrun.txt'
    
    @staticmethod
    def is_scrapyd_started():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(appcfg.SCRAPY_SOCKET)
            sock.shutdown(2)
            return True
        except:
            return False
    
    @classmethod
    def get_last_run(self):
        if not self.last_run:
            if os.path.isfile(self.file):
                fh = open(self.file, 'r+')
                self.last_run = fh.read()
                fh.close()
            else:
                self.last_run = timezone.now()
        return self.last_run
    
    @classmethod
    def get_last_run_iso(self):
        lastrun = str(self.get_last_run())
        return datetime.strptime(lastrun.split('+')[0], '%Y-%m-%d %H:%M:%S.%f')
    