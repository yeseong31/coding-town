from flask import request
from flask_socketio import SocketIO, emit, send, join_room, leave_room

sio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True)

to_client = dict()


@sio.on('connect')
def on_connect(auth):
    """Socket Connect 이벤트 감지"""
    print('Client connected')
    emit('connect', {'data': 'Connected'})


@sio.on('disconnect')
def on_disconnect():
    """Socket Disconnect 이벤트 감지"""
    print('Client disconnected')


@sio.on('message')
def on_message(msg):
    """Socket 메시지 송수신 이벤트 감지"""
    if msg == 'New Connect!':
        to_client['message'] = 'welcome!'
        to_client['type'] = 'connect'
        emit('message', {'msg': 'connect'})
    elif msg == 'Disconnect':
        to_client['message'] = 'bye bye'
        to_client['type'] = 'disconnect'
        emit('message', {'msg': 'disconnect'})
    else:
        to_client['message'] = msg
        to_client['type'] = 'normal'
        emit('message', {'msg': f'message: {msg}'})
    send(to_client, broadcast=True)
