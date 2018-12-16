
from django.core.paginator import Paginator
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.urls.base import reverse
from django.utils.translation import gettext as _
from catalog import settings as appcfg
from catalog.helpers import ScrapyHelper, ViewHelper, NavigationHelper
from catalog.models import Book, Author, Category
from catalog.utils.feedgenerator import OpdsAcquisitionFeed


def root(request):
    updateddate = ScrapyHelper.get_last_run_iso()
    f = NavigationHelper.get_navigation_feed(
        ViewHelper.get_feed_uuid('root'), 
        reverse('root'), 
        _('AllITEbooks.com OPDS-Proxy'), 
        _('Free IT Ebooks Download')
    )
    entries = NavigationHelper.get_nav_entries('root')
    for entry in entries:
        f.add_item(
            title = entry['title'], 
            link = entry['url'], 
            link_type = entry['type'],
            description = entry['content'], 
            unique_id = entry['uuid'][0], 
            updateddate = updateddate,
            categories = [],
        )
    return HttpResponse(f.writeString('UTF-8'))


def catalog(request):
    updateddate = ScrapyHelper.get_last_run_iso()
    f = NavigationHelper.get_navigation_feed(
        ViewHelper.get_feed_uuid('catalog'), 
        reverse('catalog'), 
        _('Catalog'), 
        _('Browse Catalog'),
        reverse('root')
    )
    entries = NavigationHelper.get_nav_entries('catalog')
    for entry in entries:
        f.add_item(
            title = entry['title'], 
            link = entry['url'], 
            link_type = entry['type'],
            description = entry['content'], 
            unique_id = entry['uuid'][0], 
            updateddate = updateddate,
            categories = [],
        )
    return HttpResponse(f.writeString('UTF-8'))


def authors(request):
    page = request.GET.get('page', 1)
    
    entries = Author.objects.all().order_by('name')
    paginator = Paginator(entries, int(appcfg.CATALOG_PAGE_LIMIT))
    
    updateddate = ScrapyHelper.get_last_run_iso()
    f = NavigationHelper.get_navigation_feed(
        ViewHelper.get_feed_uuid('authors'), 
        reverse('authors'), 
        _('Authors'), 
        _('Browse Authors'),
        reverse('root')
    )
    authors = paginator.get_page(page)
    f.page = authors
    for author in authors:
        f.add_item(
            title = author.name, 
            link = reverse('author', kwargs = {'author_id': author.pk}), 
            link_type = 'acquisition',
            description = str(Book.objects.filter(authors = author.pk).count()) + _(' Entries'), 
            unique_id =author.uuid, 
            updateddate = updateddate,
            categories = [],
        )
    return HttpResponse(f.writeString('UTF-8'))


def categories(request):
    page = request.GET.get('page', 1)
    
    entries = Category.objects.all().order_by('name')
    paginator = Paginator(entries, int(appcfg.CATALOG_PAGE_LIMIT))
    
    updateddate = ScrapyHelper.get_last_run_iso()
    f = NavigationHelper.get_navigation_feed(
        ViewHelper.get_feed_uuid('categories'), 
        reverse('categories'), 
        _('Categories'), 
        _('Browse Categories'),
        reverse('root')
    )
    categories = paginator.get_page(page)
    f.page = categories
    for category in categories:
        f.add_item(
            title = category.name, 
            link = reverse('category', kwargs = {'category_id': category.pk}), 
            link_type = 'acquisition',
            description = str(Book.objects.filter(categories = category.pk).count()) + _(' Entries'), 
            unique_id = category.uuid, 
            updateddate = updateddate,
            categories = [],
        )
    return HttpResponse(f.writeString('UTF-8'))


def books(request):
    order_by = request.GET.get('order_by', request.session.get('books_order', 'title'))
    request.session['books_order'] = order_by
    page = request.GET.get('page', 1)
    
    if order_by is '-updated_at':
        entries = Book.objects.all().order_by(order_by)
    else:
        entries = Book.objects.all().order_by(order_by, 'title')
    paginator = Paginator(entries, int(appcfg.CATALOG_PAGE_LIMIT))
    
    f = NavigationHelper.get_navigation_feed(
        ViewHelper.get_feed_uuid('books'), 
        reverse('books'), 
        _('Books'), 
        _('All Books ordered by ') + order_by,
    )
    books = paginator.get_page(page)
    f.page = books
    for book in books:
        __add_book(book, f)
    return HttpResponse(f.writeString('UTF-8'))


def search(request):
    query = request.GET.get('q', None)
    page = request.GET.get('page', 1)
    if query is None:
        query = request.session.get('query', None)

    if query is not None:
        request.session['query'] = query
        results = Book.objects.filter(
            Q(title__icontains = query) |
            Q(summary__icontains = query) |
            Q(description__icontains = query)
        ).order_by('-year', 'title')
        paginator = Paginator(results, int(appcfg.CATALOG_PAGE_LIMIT))
        
        f = NavigationHelper.get_navigation_feed(
            ViewHelper.get_feed_uuid('search_' + NavigationHelper.get_uuid_key(query)), 
            reverse('search'), 
            _('Search-Results'), 
            _('Search-Results for ') + query,
            reverse('root'),
        )
        books = paginator.get_page(page)
        f.page = books
        for book in books:
            __add_book(book, f)
        return HttpResponse(f.writeString('UTF-8'))
    else:
        return HttpResponseBadRequest(content = 'Search-Term (q) is a mandatory parameter')


def author(request, author_id):
    order_by = request.GET.get('order_by', request.session.get('author_order', 'title'))
    request.session['author_order'] = order_by
    page = request.GET.get('page', 1)
    author = Author.objects.get(pk = author_id)
        
    entries = Book.objects.filter(authors = author_id).order_by(order_by, 'title')
    paginator = Paginator(entries, int(appcfg.CATALOG_PAGE_LIMIT))
    
    f = NavigationHelper.get_navigation_feed(
        ViewHelper.get_feed_uuid('author_' + str(author_id)), 
        reverse('author', kwargs = {'author_id': author_id}),
        _('Books from ' + author.name), 
        _('All Books from ') + author.name,
        reverse('authors'),
    )
    books = paginator.get_page(page)
    f.page = books
    for book in books:
        __add_book(book, f)
    return HttpResponse(f.writeString('UTF-8'))


def category(request, category_id):
    order_by = request.GET.get('order_by', request.session.get('category_order', 'title'))
    request.session['category_order'] = order_by
    page = request.GET.get('page', 1)
    category = Category.objects.get(pk = category_id)
    
    entries = Book.objects.filter(categories = category_id).order_by(order_by, 'title')
    paginator = Paginator(entries, int(appcfg.CATALOG_PAGE_LIMIT))
    
    f = NavigationHelper.get_navigation_feed(
        ViewHelper.get_feed_uuid('category_' + str(category_id)), 
        reverse('category', kwargs = {'category_id': category_id}),
        _('Books in ' + category.name), 
        _('All Books in ' + category.name),
        reverse('categories'),
    )
    books = paginator.get_page(page)
    f.page = books
    for book in books:
        __add_book(book, f)
    return HttpResponse(f.writeString('UTF-8'))


def book(request, book_id):
    book = Book.objects.get(pk = book_id)
    links = []
    authors = []
    cats = []
    
    for link in book.get_links():
        links.append({
            'href': link.url,
            'type': link.get_mimetype()
        })

    for author in book.authors.all():
        authors.append({
            'name': author.name,
            'url': author.url
        })
        
    for category in book.categories.all():
        cats.append(category.name)
        
    f = OpdsAcquisitionFeed(
        root_url = reverse('root'),
        search_url = reverse('search') + '?q={searchTerms}',
        feed_icon = 'http://www.allitebooks.com/wp-content/themes/allitebooks/images/favicon.ico',
        updated = book.updated_at,
        link = None,
        description = None,
        feed_rights = None,
        title = _('Book-Details'),
        subtitle = _('Book-Details for ' + book.title),
        id = ViewHelper.get_feed_uuid('books'),
        feed_url = reverse('book', kwargs={'book_id': book.pk}),
    )
    f.add_item(
        title = book.title, 
        summary = book.summary,
        link = book.url,
        link_type = 'alternate',
        description = book.description, 
        unique_id = 'urn:uuid:' + str(book.uuid), 
        updateddate = book.updated_at,
        download_links = links,
        authors = authors,
        isbn = book.isbn,
        year = str(book.year),
        language = book.language,
        image = book.image,
        image_type = book.get_image_mimetype(),
        categories = cats,
    )
    return HttpResponse(f.writeString('UTF-8'))


def __add_book(book, feed):
    links = []
    authors = []
    categories = []
    
    for link in book.get_links():
        links.append({
            'href': link.url,
            'type': link.get_mimetype()
        })

    for author in book.authors.all():
        authors.append({
            'name': author.name,
            'url': author.url
        })
        
    for category in book.categories.all():
        categories.append(category.name)
        
    feed.add_item(
        title = book.title, 
        summary = book.summary,
        link = reverse('book', kwargs={'book_id': book.pk}), 
        link_type = 'acquisition',
        description = book.description, 
        unique_id = 'urn:uuid:' + str(book.uuid), 
        updateddate = book.updated_at,
        download_links = links,
        authors = authors,
        isbn = book.isbn,
        year = str(book.year),
        language = book.language,
        image = book.image,
        image_type = book.get_image_mimetype(),
        categories = categories,
    )
    
    