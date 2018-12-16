
from catalog.models import Book, Author, Category, Link, BookStats
from rest_framework import serializers


class BookStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookStats
        fields = ('categories', 'books', 'authors', 'links')
        
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'url', 'uuid')
        
class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'url', 'uuid')
        
class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'book', 'url', 'format')
          
class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many = True, read_only = True)
    categories = CategorySerializer(many = True, read_only = True)
    class Meta:
        model = Book
        fields = ('id', 'title', 'isbn', 'year', 'uuid', 'summary', 'language', 'image', 'url', 'authors', 'categories', 'updated_at')
        