from django.urls import path

from sockets.views import sio_views, room_views, lobby_views

urlpatterns = [
    path('/', sio_views),
    path('room/', room_views),
    path('lobby/', lobby_views),
]