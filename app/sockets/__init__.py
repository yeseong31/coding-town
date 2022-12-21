from flask import request
from flask_socketio import SocketIO, emit, send, join_room

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
    """
    Room 입장에 필요한 정보를 확인한 뒤 입장 코드 반환

    :argument
        - nickName: 방 생성자 닉네임
        - roomCode: 입장하려는 방 코드

    :returns
        - isSuccess: 방 생성 성공 여부
    """
    # load packages
    from app.models import Room

    # 데이터 확인
    sid = request.sid
    nickname = data['nickName']
    room_code = data['roomCode']

    # 방 조회
    room = Room.query.filter_by(room_code=room_code).first()
    if not room:
        emit('create', {'isSuccess': False})
    else:
        join_room(room_code)
        emit('create', {'isSuccess': True})
        send(nickname + ' has entered the room.', to=room_code)


@sio.on('join')
def on_join(data):
    """
    새로운 사람이 Room 참여 정보를 기존 Room 참여자들에게 전달

    :argument:
        - nickName: 방 참여자 닉네임
        - roomCode: 입장하려는 방 코드
    """
    # load packages
    from app import db
    from app.models import User, Room

    # 데이터 확인
    sid = request.sid
    nickname = data['nickName']
    room_code = data['roomCode']

    # 참여자 추가
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        user = User(nickname=nickname)
    room = Room.query.filter_by(room_code=room_code).first()
    if not room:
        emit('join', {'message': 'Room does not exist.'})
    else:
        room.room_participant.append(user)
        db.session.add(user)
        db.session.commit()
        emit('join', {'message': 'The room exists.', 'nickName': nickname}, to=room_code)
        send(nickname + ' has entered the room.', to=room_code)


@sio.on('offer')
def on_offer(data):
    """
    기존 참여자들의 정보를 서버로 전달
    
    :argument:
        - roomCode: 입장하려는 방 코드
        - sdp: 참여자의 peer 정보
    """
    sid = request.sid
    room_code = data['roomCode']
    sdp = data['sdp']
    print(sid)
    pass


@sio.on('answer')
def on_answer(data):
    """
    새로운 참여자의 정보를 서버로 전달

    :argument:
        - roomCode: 입장하려는 방 코드
        - sdp: 참여자의 peer 정보
    """
    sid = request.sid
    room_code = data['roomCode']
    sdp = data['sdp']
    pass
