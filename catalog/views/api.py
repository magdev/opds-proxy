from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from catalog.models import Book, BookStats
from catalog.serializers import BookSerializer, BookStatsSerializer
from catalog import settings as appcfg

@api_view()
def stats(request):
    stats = BookStats.objects.get(pk=1)
    serializer = BookStatsSerializer(stats)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view()
def search(request):
    query = request.GET.get('q', None)
    page = request.GET.get('page', 1)

    if query is not None:
        results = Book.objects.filter(
            Q(title__icontains = query) |
            Q(summary__icontains = query) |
            Q(description__icontains = query)
        ).order_by('-year', 'title')
        
        paginator = Paginator(results, appcfg.CATALOG_PAGE_LIMIT)
        serializer = BookSerializer(paginator.get_page(page), many = True, context = {'request': request})
        result = {
            'page': page,
            'perPage': appcfg.CATALOG_PAGE_LIMIT,
            'pages': paginator.num_pages,
            'query': query,
            'count': int(results.__len__()),
            'results': serializer.data,
        }
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Query parameter (q) is mandatory'
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view()
def recent(request):
    limit = request.GET.get('limit', 10)
    entries = Book.objects.all().order_by('-updated_at')[:int(limit)]
    serializer = BookSerializer(entries, many = True, context = {'request': request})
    result = {
        'limit': limit,
        'results': serializer.data,
    }
    return Response(result, status=status.HTTP_200_OK)
    
