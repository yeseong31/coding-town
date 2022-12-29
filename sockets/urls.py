from django.urls import path
from rest_framework import routers

from sockets.views import sio_views, room_views

app_name = 'sockets'

router = routers.SimpleRouter()

urlpatterns = [
    # ----- SocketIO -----
    path('', sio_views.test, name='test'),
    
    # ----- Room -----
    # Room 생성
    path('room/create/', room_views.room_post, name='room_post'),
]
