from django.conf.urls import url

from ws import consumers

websocket_urlpatterns = [
    url(r'^ws/$', consumers.UpdateConsumer),
]