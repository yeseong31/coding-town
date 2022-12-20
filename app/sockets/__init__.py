from flask import request
from flask_socketio import SocketIO, emit, send

sio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True)

to_client = dict()


@sio.on('connect')
def on_connect(auth):
    """Socket Connect 이벤트 감지"""
    print(f'[{request.sid}] Client connected')
    emit('connect', {'data': 'Connected'})


@sio.on('disconnect')
def on_disconnect():
    """Socket Disconnect 이벤트 감지"""
    print(f'[{request.sid}] Client disconnected')
    emit('disconnect', {'data': 'Disconnected'})


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


@sio.on('create')
def on_create(data):
    """Room 입장에 필요한 정보를 확인한 뒤 입장 코드 반환

    :argument
        - roomName: 생성할 방 이름
        - nickName: 방 생성자 닉네임
        - password: 방 비밀번호

    :returns
        - roomCode: 생성된 방의 고유한 6자리 랜덤 번호
    """
    # load packages
    import random
    from datetime import datetime

    import bcrypt

    from app import db
    from app.models import Room, User

    # 데이터 확인
    room_name = data['roomName']
    password = data['password']
    nickname = data['nickName']

    # 사용자 확인
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        user = User(nickname=nickname)
        db.session.add(user)
        db.session.commit()

    # 랜덤 시드 설정
    random.seed()

    # 방 생성
    room = Room(room_name=room_name,
                room_code=int(random.random() * 10 ** 6),
                is_private=False if password == '' or password is None else True,
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                current_user=0,
                total_user=10,
                room_owner=user.id,
                created_at=datetime.now())
    db.session.add(room)
    # db.session.commit()
    # 방 코드 전달
    emit('create', {'roomCode': room.room_code})


@sio.on('offer')
def on_offer(data):
    pass


@sio.on('answer')
def on_answer(data):
    pass
