from flask import request
from flask_socketio import SocketIO, emit, send, join_room, leave_room

sio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True)

to_client = dict()

# 참가자
users_in_room = {}
# 방
rooms_sid = {}
# 참가자 이름
names_sid = {}


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
    """
    Socket Rooms 입장 이벤트

    :param data:
        - nickName: 사용자 닉네임
        - roomCode: 입장하고자 하는 방 코드
    :return:
        None
    """
    from app.models import Room
    from app import db

    sid = request.sid
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
        join_room(room_code)

        # 테스트 코드
        rooms_sid[sid] = room_code
        names_sid[sid] = nickname
        # broadcast to others in the room
        print(f'[{room_code}] New member joined: {nickname}<{sid}>')
        emit('join', {'sid': sid, 'nickName': nickname}, broadcast=True, include_self=False, room=room_code)
        # add to user list maintained on server
        if room_code not in users_in_room:
            users_in_room[room_code] = [sid]
            emit('join', {'my_id': sid, 'isSuccess': True})  # send own id only
        else:
            usr_list = {u_id: names_sid[u_id] for u_id in users_in_room[room_code]}
            # send list of existing users to the new member
            emit('join', {'list': usr_list, 'my_id': sid, 'isSuccess': True})
            # add new member to user list maintained on server
            users_in_room[room_code].append(sid)

        print(f'\nusers: {users_in_room}\n')
        # send(f'{nickname} has entered the room.', to=room_code)


@sio.on('offer')
def on_offer(data):
    """
    Socket Rooms Join 이벤트(참가자)

    :param data:
        - type: RTCSessionDescription 타입
        - sdp: 방에 입장하는 사람의 peer 정보
    :return:
        None
    """
    sid = request.sid
    _type = data['type']
    sdp = data['string']
    print(f'[{sid}] received offer event! type: {_type}, sdp: {sdp}')


@sio.on('answer')
def on_answer(data):
    """
    Socket Rooms Join 이벤트(방장)

    :param data:
    :return:
        None
    """
    sid = request.sid
    _type = data['type']
    sdp = data['string']
    print(f'[{sid}] received answer event! type: {_type}, sdp: {sdp}')


@sio.on('leave')
def on_leave(data):
    """Socket Rooms 퇴장 이벤트 감지

    :argument
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
