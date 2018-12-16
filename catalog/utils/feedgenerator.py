
from django.utils.feedgenerator import Atom1Feed, rfc3339_date, get_tag_uri
from django.utils.translation import gettext as _


class OpdsFeed(Atom1Feed):
    # Spec: http://opds-spec.org/
    content_type = 'application/atom+xml;type=feed;profile=opds-catalog'
    ns = "http://www.w3.org/2005/Atom"
    page = None
    kind = 'navigation'
    
    def root_attributes(self):
        attrs = super().root_attributes()
        attrs['xmlns:dc'] = 'http://purl.org/dc/terms/'
        return attrs

    def add_root_elements(self, handler):
        handler.addQuickElement("title", self.feed['title'])
        if self.feed['subtitle'] is not None:
            handler.addQuickElement("subtitle", self.feed['subtitle'])
        handler.addQuickElement("id", self.feed['id'])
        handler.addQuickElement("updated", rfc3339_date(self.latest_post_date()))
        if self.feed['feed_url'] is not None:
            self.__add_link_element(handler, 
                self.feed['feed_url'], 
                'self', 
                self.__get_link_type(self.kind))
        if 'root_url' in self.feed and self.feed['root_url'] is not None:
            self.__add_link_element(handler, 
                self.feed['root_url'], 
                'start', 
                self.__get_link_type('navigation'))
        if 'search_url' in self.feed and self.feed['search_url'] is not None:
            self.__add_link_element(handler, 
                self.feed['search_url'], 
                'search', 
                'application/atom+xml',
                _('Search'))
        if self.page is not None:
            if 'up_url' in self.feed and self.feed['up_url']:
                self.__add_link_element(handler, 
                    self.feed['up_url'], 
                    'up', 
                    self.__get_link_type(self.kind),
                     _('Up'))
            self.__add_link_element(handler, 
                self.feed['feed_url'], 
                'first', 
                self.__get_link_type(self.kind),
                 _('First Page'))
            if self.page.has_previous():
                self.__add_link_element(handler, 
                    self.feed['feed_url'] + '?page=' + str(self.page.previous_page_number()), 
                    'previous', 
                    self.__get_link_type(self.kind),
                     _('Previous Page'))
            if self.page.has_next():
                self.__add_link_element(handler, 
                    self.feed['feed_url'] + '?page=' + str(self.page.paginator.num_pages), 
                    'last', 
                    self.__get_link_type(self.kind),
                     _('Last Page'))
                self.__add_link_element(handler, 
                    self.feed['feed_url'] + '?page=' + str(self.page.next_page_number()), 
                    'next', 
                    self.__get_link_type(self.kind),
                     _('Next Page'))
        if self.feed['author_name'] is not None:
            handler.startElement("author", {})
            handler.addQuickElement("name", self.feed['author_name'])
            if self.feed['author_email'] is not None:
                handler.addQuickElement("email", self.feed['author_email'])
            if self.feed['author_link'] is not None:
                handler.addQuickElement("uri", self.feed['author_link'])
            handler.endElement("author")
        for cat in self.feed['categories']:
            handler.addQuickElement("category", "", {"term": cat})
        if self.feed['feed_rights'] is not None:
            handler.addQuickElement("rights", self.feed['feed_copyright'])
        if self.feed['feed_icon'] is not None:
            handler.addQuickElement("icon", self.feed['feed_icon'])

    def add_item_elements(self, handler, item):
        handler.addQuickElement("title", item['title'])
        if 'summary' in item and item['summary'] is not None:
            handler.addQuickElement('summary', item['summary'], {"type": "text"})
            
        self.__add_link_element(handler, 
            item['link'], 
            '', 
            self.__get_link_type(item['link_type']))
        
        if item['pubdate'] is not None:
            handler.addQuickElement('published', rfc3339_date(item['pubdate']))

        if item['updateddate'] is not None:
            handler.addQuickElement('updated', rfc3339_date(item['updateddate']))

        # Author information.
        if item['author_name'] is not None:
            handler.startElement("author", {})
            handler.addQuickElement("name", item['author_name'])
            if item['author_email'] is not None:
                handler.addQuickElement("email", item['author_email'])
            if item['author_link'] is not None:
                handler.addQuickElement("uri", item['author_link'])
            handler.endElement("author")

        # Unique ID.
        if item['unique_id'] is not None:
            unique_id = item['unique_id']
        else:
            unique_id = get_tag_uri(item['link'], item['pubdate'])
        handler.addQuickElement("id", unique_id)

        # Summary.
        if item['description'] is not None:
            handler.addQuickElement("content", item['description'], {"type": "text"})

        # Categories.
        for cat in item['categories']:
            handler.addQuickElement("category", "", {"term": cat})

        # Rights.
        if item['item_copyright'] is not None:
            handler.addQuickElement("rights", item['item_copyright'])
            
        if 'download_links' in item and item['download_links'] is not None:
            for link in item['download_links']:
                self.__add_link_element(handler, link['href'], 'http://opds-spec.org/acquisition', link['type'])
                
        if 'authors' in item and item['authors'] is not None:
            for author in item['authors']:
                handler.startElement("author", {})
                handler.addQuickElement("name", author['name'])
                if author['url'] is not None:
                    handler.addQuickElement("uri", author['url'])
                handler.endElement("author")
        if 'image' in item and item['image'] is not None and 'image_type' in item and item['image_type'] is not None:
            self.__add_link_element(handler, item['image'], 'http://opds-spec.org/image', item['image_type'])
            
        if 'isbn' in item and item['isbn'] is not None:
            handler.addQuickElement('dc:identifier', 'urn:isbn:' + item['isbn'])
            
        if 'year' in item and item['year'] is not None:
            handler.addQuickElement('dc:issued', item['year'])
        if 'language' in item and item['language'] is not None:
            handler.addQuickElement('dc:language', item['language'])
            
            
    def __get_link_type(self, linktype):
        if linktype is 'alternate':
            return linktype
        return self.content_type + ';kind=' + linktype
        
    def __add_link_element(self, handler, url, rel = '', linktype = '', title = ''):
        args = {
            'href': url,
        }
        if title:
            args['title'] = title
        if rel:
            args['rel'] = rel
        if linktype:
            args['type'] = linktype
        handler.addQuickElement("link", "", args)


class OpdsNavigationFeed(OpdsFeed):
    kind = 'navigation'


class OpdsAcquisitionFeed(OpdsFeed):
    kind = 'acquisition'
