import os

import socketio
from django.http import HttpResponse
from django.shortcuts import render

from config.settings.base import BASE_DIR

# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = 'eventlet'

sio = socketio.Server(async_mode=async_mode)
thread = None


def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return HttpResponse(open(os.path.join(BASE_DIR, 'chat.html')))


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'}, namespace='/test')


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)
    

@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)
    
    
@sio.event
def disconnect(sid):
    print('Client disconnected')
    
    
def test(request):
    return render(request, 'chat.html')
