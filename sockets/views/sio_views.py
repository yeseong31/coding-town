import os

import socketio
from django.http import HttpResponse
from django.shortcuts import render

from config.settings.base import BASE_DIR

# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's installed
async_mode = 'eventlet'

sio = socketio.Server(
    async_mode=async_mode,
    cors_allowed_origins='*',
    logger=True,
    async_handlers=True,
    pingTimeout=900
)
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
        sio.emit('my_response', {'data': '[Server] Server generated event'}, namespace='/test')


@sio.event
def on_connect(sid, environ):
    """
    SocketIO Connect 이벤트
    
    :param sid:
    - SocketIO ID
    
    :return(emit):
    - message: emit 설명
    - sid: SocketIO ID
    """
    sio.emit('connect', {'message': '[Server] Connected', 'sid': sid})


@sio.event
def on_disconnect(sid):
    """
    SocketIO Disconnect 이벤트
    
    :param sid:
    - SocketIO ID
    
    :return(emit):
    - message: emit 설명
    """
    sio.emit('disconnect', {'message': '[Server] Disconnected'})


@sio.event
def on_message(sid, msg):
    """
    Socket Message 이벤트
    
    :param sid:
    - SocketIO ID
    
    :param msg:
    - 메시지 내용
    
    :return(emit):
    - msg: 메시지 내용
    """
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


@sio.on('create')
def on_create(sid, data):
    """
    Room 입장에 필요한 정보를 확인한 뒤 입장 코드 반환
    
    :param sid:
    - SocketIO ID
    
    :param data:
    - nickName: Room 생성자 닉네임
    - roomCode: Room 코드
    
    :return(emit):
    - message: emit 설명
    - isSuccess: Room 생성 성공 여부
    """
    owner = data['nickName']
    code = data['roomCode']

    sio.enter_room(sid, code)
    response_data = {
        'message': f"[Server] {owner} has entered the room.",
        'isSuccess': True
    }

    sio.emit('create', response_data, room=code)


@sio.on('join')
def on_join(sid, data):
    """
    새로운 참여자의 Room 참여 정보를 기존 Room 참여자들에게 전달
    
    :param sid:
    - SocketIO ID
    
    :param data:
    - nickName: Room 생성자 닉네임
    - roomCode: Room 코드
    
    :return(emit):
    - message: emit 설명
    - nickName: 참여자 닉네임
    - sid: SocketIO ID
    """
    nickname = data['nickName']
    code = data['roomCode']

    response_data = {
        'message': "[Server] The room exists.",
        'nickName': nickname,
        'sid': sid
    }

    sio.emit('join', response_data, room=code, skip_sid=sid)
    
    
@sio.on('handshake')
def on_handshake(sid, data):
    """
    WebRTC의 offer, answer 이벤트 전에 실행되는 SocketIO Handshake
    
    :param sid:
    - SocketIO ID
    
    :param data:
    - roomCode: Room 코드
    - sid: SocketIO ID (새로운 참여자)
    
    :return(emit):
    - message: emit 설명
    - sid: SocketIO ID
    """
    target = data['sid']
    code = data['roomCode']

    response_data = {
        'message': "[Server] SocketIO handshake event.",
        'sid': sid
    }
    
    if sid == target:
        sio.emit('handshake', response_data, room=code)
    else:
        sio.emit('handshake', response_data, to=target)


@sio.on('offer')
def on_offer(sid, data):
    """
    기존 참여자들의 정보를 새로운 참여자에게 전달
    
    :param sid:
    - SocketIO ID
    
    :param data:
    - roomCode: Room 코드
    - sdp: 참여자 peer 정보
    
    :return(emit):
    - message: emit 설명
    - roomCode: Room 코드
    - sdp: 기존 참여자 peer 정보
    - sid: SocketIO ID (새로운 참여자)
    - isSuccess: 이벤트 수행 결과
    """
    code = data['roomCode']
    sdp = data['sdp']
    target = data['sid']

    response_data = {
        'message': '[Server] The information of the user currently in the room.',
        'roomCode': code,
        'sdp': sdp,
        'sid': sid,
        'isSuccess': True
    }

    sio.emit('offer', response_data, to=target)


@sio.on('answer')
def on_answer(sid, data):
    """
    새로운 참여자의 정보를 서버로 전달
    
    :param sid:
    - SocketIO ID
    
    :param data:
    - roomCode: Room 코드
    - sdp: 참여자 peer 정보
    - sid: SocketIO ID (새로운 참여자)
    
    :return(emit):
    - message: emit 설명
    - roomCode: Room 코드
    - sdp: 참여자 peer 정보
    - isSuccess: 이벤트 수행 결과
    """
    code = data['roomCode']
    sdp = data['sdp']
    target = data['sid']

    response_data = {
        'message': '[Server] The information of the user currently in the room.',
        'roomCode': code,
        'sdp': sdp,
        'isSuccess': True
    }

    sio.emit('answer', response_data, to=target,  skip_sid=sid)


@sio.on('bye')
def on_bye(sid, data):
    """
    Room 퇴장 이벤트
    
    :param sid:
    - SocketIO ID
    
    :param data:
    - roomCode: 퇴장한 Room 코드
    - nickName: 퇴장한 참여자 닉네임
    
    :return(emit):
    - message: emit 설명
    - isSuccess: 이벤트 수행 결과
    """
    code = data['roomCode']
    nickname = data['nickName']

    response_data = {
        'message': f'[Server] <<{sid}>> {nickname} has left.',
        'isSuccess': True
    }

    sio.emit('bye', response_data, room=code, skip_sid=sid)


@sio.on('icecandidate')
def on_icecandidate(sid, data):
    """
    IceCandidate 이벤트
    
    :param sid:
    - SocketIO ID
    
    :param data:
    - sid: SocketIO ID(새로운 참여자)
    - roomCode: Room 코드
    - candidate: IceCandidate 객체
    
    :return(emit):
    - candidate: IceCandidate 객체
    """
    target = data['sid']
    code = data['roomCode']
    candidate = data['candidate']

    response_data = {
        'candidate': candidate
    }

    if sid == target:
        sio.emit('icecandidate', response_data, room=code)
    else:
        sio.emit('icecandidate', response_data, to=target)


def test(request):
    return render(request, 'chat.html')
