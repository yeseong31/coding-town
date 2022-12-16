from flask_socketio import SocketIO, emit, send, join_room, leave_room

sio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True)

to_client = dict()


@sio.on('connect')
def on_connect(auth):
    """Socket Connect 이벤트 감지"""
    print('Client connected')
    emit('my response', {'data': 'Connected'})


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
        emit('status', {'msg': 'connect'})
    elif msg == 'Disconnect':
        to_client['message'] = 'bye bye'
        to_client['type'] = 'disconnect'
        emit('status', {'msg': 'disconnect'})
    else:
        to_client['message'] = msg
        to_client['type'] = 'normal'
        emit('status', {'msg': f'message: {msg}'})
    send(to_client, broadcast=True)


@sio.on('join')
def on_join(data):
    """Socket Rooms 입장 이벤트 감지"""
    nickname = data['nickName']
    room_code = data['roomCode']
    join_room(room_code)
    send(f'{nickname} has entered the room.', to=room_code)


@sio.on('leave')
def on_leave(data):
    """Socket Rooms 퇴실 이벤트 감지"""
    nickname = data['nickName']
    room_code = data['roomCode']
    leave_room(room_code)
    send(f'{nickname} has left the room.', to=room_code)
