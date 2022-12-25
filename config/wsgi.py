"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

import eventlet.wsgi
import socketio
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_application = get_wsgi_application()
sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*', cors_credentials=True)
application = socketio.WSGIApp(sio, django_application)
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
