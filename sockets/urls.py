from django.urls import path
from rest_framework import routers

from sockets.views import sio_views, room_views
from sockets.views.room_views import RoomsAPI

app_name = 'sockets'

urlpatterns = [
    # ----- SocketIO -----
    path('', sio_views.test, name='test'),

    # ----- Room -----
    # Room 생성
    path('room/create/', room_views.room_post, name='room_post'),
    # Room 참가
    path('room/join/', room_views.room_join, name='room_join'),
    # Room 리스트 조회
    path('lobby/', RoomsAPI.as_view(), name='lobby'),
]
