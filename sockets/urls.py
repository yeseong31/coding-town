from django.urls import path

from sockets.views import sio_views, room_views
from sockets.views.room_views import RoomsAPI, CreateRoomAPI, JoinRoomAPI

app_name = 'sockets'

urlpatterns = [
    # ----- SocketIO -----
    path('', sio_views.test, name='test'),

    # ----- Room -----
    # Room 생성
    path('room/create/', CreateRoomAPI.as_view(), name='room_post'),
    # Room 참가
    path('room/join/', JoinRoomAPI.as_view(), name='room_join'),
    # Room 리스트 조회 및 검색
    path('lobby/', RoomsAPI.as_view(), name='room_search'),
]
