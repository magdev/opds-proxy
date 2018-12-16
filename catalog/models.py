import os
import urllib
import uuid
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.db.models.fields import SmallIntegerField


class Author(models.Model):
    name = models.CharField(
        max_length = 128, 
        default = 'Unknown Author', 
        db_index = True,
        unique = True,
        verbose_name = _('Name'),
    )
    url = models.URLField(
        max_length = 255, 
        default = '', 
        db_index = True,
        unique = True,
        verbose_name = _('Original-URL'),
    )
    uuid = models.UUIDField(
        default = uuid.uuid1(), 
        verbose_name = _('UUID'),
    )
    
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
    
    def count_books(self):
        return Book.objects.filter(authors = self.pk).count()
    
    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(
        max_length = 128, 
        default = 'None', 
        db_index = True,
        verbose_name = _('Name'),
    )
    url = models.URLField(
        max_length = 255, 
        default = '', 
        db_index = True,
        unique = True,
        verbose_name = _('Original-URL'),
    )
    uuid = models.UUIDField(
        default = uuid.uuid1(), 
        verbose_name = _('UUID'),
    )
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def count_books(self):
        return Book.objects.filter(categories = self.pk).count()
    
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    title = models.CharField(
        max_length = 200, 
        db_index = True,
        verbose_name = _('Title'),
    )
    year = models.PositiveSmallIntegerField(
        db_index = True,
        verbose_name = _('Year'),
    )
    isbn = models.CharField(
        max_length = 13, 
        db_index = True,
        verbose_name = _('ISBN'),
    )
    pages = models.PositiveSmallIntegerField(
        verbose_name = _('Pages'),
    )
    summary = models.TextField(
        default = '', 
        db_index = True,
        null = True,
        blank = True,
        verbose_name = _('Summary'),
    )
    description = models.TextField(
        default = '', 
        db_index = True,
        null = True,
        blank = True,
        verbose_name = _('Description'),
    )
    uuid = models.UUIDField(
        default = '', 
        unique = True,
        verbose_name = _('UUID'),
    )
    url = models.URLField(
        max_length = 255, 
        default = '', 
        db_index = True, 
        unique = True,
        verbose_name = _('Original-URL'),
    )
    image = models.URLField(
        max_length = 255, 
        default = '',
        verbose_name = _('Image-URL'),
    )
    language = models.CharField(
        max_length = 2, 
        default = 'en',
        verbose_name = _('Language-Code'),
    )
    created_at = models.DateTimeField(
        editable = False, 
        null = True,
        blank = True,
        auto_now = False, 
        auto_now_add = True,
        verbose_name = _('Created at'),
    )
    updated_at = models.DateTimeField(
        null = True,
        blank = True,
        auto_now = True, 
        verbose_name = _('Updated at'),
    )

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        get_latest_by = "-updated_at"
        ordering = ['-updated_at']
        
    def origin(self):
        return format_html('<a href="' + self.url + '" target="_blank">' + _('Origin') + '</a>')
        
    def get_image_mimetype(self):
        if self.image:
            ext = os.path.splitext(self.image)[1].strip(' .').upper()
            switcher = {
                'JPEG': 'image/jpeg',
                'JPG': 'image/jpeg',
                'PNG': 'image/png',
                'WEBP': 'image/webp',
                'GIF': 'image/gif'
            }
            return switcher.get(ext, None)
        
    def get_links(self):
        return Link.objects.filter(book_id = self.pk)
    
    def google_search(self):
        return format_html('<a href="https://www.google.com/search?q=' + urllib.parse.quote(self.title) + '" target="_blank">' + _('Search on Google') + '</a>')
    
    def __str__(self):
        return self.title

    
class Link(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    url = models.URLField(
        max_length = 255, 
        db_index = True, 
        unique = True, 
        verbose_name = _('Download-URL'),
    )
    format = models.CharField(
        max_length = 4, 
        db_index = True, 
        verbose_name = _('Format'),
    )
    
    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def get_mimetype(self):
        switcher = {
            'EPUB': 'application/epub+zip',
            'PDF': 'application/pdf',
            'RAR': 'application/x-rar-compressed',
            'ZIP': 'application/zip',
            'AZW3': 'application/vnd.amazon.ebook',
            'MOBI': 'application/x-mobipocket-ebook',
        }
        return switcher.get(self.format, 'application/octet-stream')
        
    def __str__(self):
        return self.url
    
    
class FeedUuid(models.Model):
    feed = models.CharField(
        max_length = 255,
        db_index = True,
        unique = True, 
        verbose_name = _('Feed-ID'),
    )
    uuid = models.CharField(
        max_length = 36,
        db_index = True,
        unique = True, 
        verbose_name = _('UUID'),
    )
    
    class Meta:
        verbose_name = _('Feed-UUID')
        verbose_name_plural = _('Feed-UUIDs')
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()
        super(FeedUuid, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.feed
    
    
class BookStats(models.Model):
    id = models.SmallIntegerField(primary_key = True)
    categories = SmallIntegerField()
    books = SmallIntegerField()
    authors = SmallIntegerField()
    links = SmallIntegerField()
    
    class Meta:
        managed = False
        db_table = 'book_stats'


