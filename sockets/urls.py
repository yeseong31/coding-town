from django.urls import path

from sockets.views import sio_views

app_name = 'sockets'

urlpatterns = [
    path('', sio_views.test, name='test'),
]
