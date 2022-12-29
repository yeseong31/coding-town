"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

import eventlet.wsgi
from django.core.wsgi import get_wsgi_application
from socketio import WSGIApp

from sockets.views.sio_views import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_app = get_wsgi_application()
application = WSGIApp(sio, django_app)

eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
