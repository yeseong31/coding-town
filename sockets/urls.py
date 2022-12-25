from django.urls import path

from sockets.views.sio_views import test

app_name ='sockets'

urlpatterns = [
    path('', test, name='test'),
]
