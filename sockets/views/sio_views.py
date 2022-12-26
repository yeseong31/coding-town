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


to_client = dict()


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
    """Socket Connect 이벤트 감지"""
    print(f'[{sid}] Client connected')
    sio.emit('my_response', {'data': 'Connected', 'count': 0})
    

@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)
    
    
@sio.event
def disconnect(sid):
    """Socket Disconnect 이벤트 감지"""
    print(f'[{sid}] Client disconnected')
    sio.emit('my_response', {'data': 'Disconnected'})
    
    
@sio.event
def message(sid, msg):
    """Socket 메시지 송수신 이벤트 감지"""
    if msg == 'New Connect!':
        to_client['message'] = 'welcome!'
        to_client['type'] = 'connect'
        sio.emit('status', {'msg': 'connect'})
    elif msg == 'Disconnect':
        to_client['message'] = 'bye bye'
        to_client['type'] = 'disconnect'
        sio.emit('status', {'msg': 'disconnect'})
    else:
        to_client['message'] = msg
        to_client['type'] = 'normal'
        sio.emit('status', {'msg': f'message: {msg}'})
    sio.send(to_client, broadcast=True)
    
    
def test(request):
    return render(request, 'chat.html')
