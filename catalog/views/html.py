import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404

def index(request):
    return render(request, 'catalog/index.html', {
        'lang': request.LANGUAGE_CODE,
    })

def dldb(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'opds.db')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/x-sqlite3")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
