from django.urls import path
from catalog.views import html, opds, api

urlpatterns = [
    path('', html.index, name='index'),
    
    path('opds', opds.root),
    path('opds/', opds.root),
    path('opds/root.xml', opds.root, name='root'),
    path('opds/catalog.xml', opds.catalog, name='catalog'),
    path('opds/authors.xml', opds.authors, name='authors'),
    path('opds/author/<int:author_id>.xml', opds.author, name='author'),
    path('opds/categories.xml', opds.categories, name='categories'),
    path('opds/category/<int:category_id>.xml', opds.category, name='category'),
    path('opds/books.xml', opds.books, name='books'),
    path('opds/book/<int:book_id>.xml', opds.book, name='book'),
    path('opds/search.xml', opds.search, name='search'),
    
    path('api/stats/', api.stats, name='api_stats'),
    path('api/search/', api.search, name='api_search'),
    path('api/recent/', api.recent, name='api_recent'),
]