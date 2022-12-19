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


@sio.on('create')
def on_create(data):
    """Socket Rooms 입장 이벤트

    :parameter
    - nickName: 사용자 닉네임
    - roomCode: 입장하고자 하는 방 코드
    """
    from app.models import Room
    from app import db

    nickname = data['nickName']
    room_code = data['roomCode']

    room = Room.query.filter_by(room_code=room_code).first()
    # 해당 코드를 가지는 방이 없는 경우
    if room is None:
        response_data = {'message': 'Invalid code entered.', 'status_code': 400, 'isSuccess': False}
        emit('join', response_data)
        # send(response_data)
    # 더 이상 참석이 불가능한 경우
    elif room.current_user == room.total_user:
        response_data = {'message': 'The room is full.', 'status_code': 400, 'isSuccess': False}
        emit('join', response_data)
        # send(response_data)
    # 방 입장
    else:
        room.current_user += 1
        db.session.commit()
        join_room(room_code)  # 자동으로 빈 방을 만듦
        response_data = {'isSuccess': True}
        emit('join', response_data)
        # send(f'{nickname} has entered the room.', to=room_code)
    

@sio.on('leave')
def on_leave(data):
    """Socket Rooms 퇴장 이벤트 감지

    :parameter
    - nickName: 사용자 닉네임
    - roomCode: 퇴장하고자 하는 방 코드
    """
    from app.models import Room
    from app import db
    
    nickname = data['nickName']
    room_code = data['roomCode']
    
    room = Room.query.filter_by(room_code=room_code).first()
    # 해당 코드를 가지는 방이 없는 경우
    if room is None:
        to_client['message'] = 'Invalid code entered.'
        to_client['type'] = 'error'
        response_data = {'message': to_client["message"], 'status_code': 400}
        emit('status', response_data)
    # 더 이상 퇴장이 불가능한 경우
    elif room.current_user == 0:
        to_client['message'] = 'The room is already empty.'
        to_client['type'] = 'error'
        response_data = {'message': to_client["message"], 'status_code': 400}
        emit('status', response_data)
    # 방 퇴장
    else:
        room.current_user -= 1
        db.session.commit()
        leave_room(room_code)
        send(f'{nickname} has left the room.', to=room_code)
    
