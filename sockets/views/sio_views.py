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


@sio.on('create')
def create(sid, data):
    """
    Room 입장에 필요한 정보를 확인한 뒤 입장 코드 반환
    :param sid:
        - SocketIO ID
    :param data:
        - nickName: Room 생성자 닉네임
        - roomCode: Room 코드
    :return(emit):
        - isSuccess: Room 생성 성공 여부
    """
    owner = data['nickName']
    code = data['roomCode']

    sio.enter_room(sid, code)
    response_data = {
        'message': f"{owner} has entered the room.",
        'isSuccess': True
    }

    sio.emit('create', response_data, room=code)
    sio.send(response_data)
    print(f'[Server] {response_data}')


@sio.on('join')
def join(sid, data):
    """
    새로운 참여자의 Room 참여 정보를 기존 Room 참여자들에게 전달
    :param sid:
        - SocketIO ID
    :param data:
        - nickName: Room 생성자 닉네임
        - roomCode: Room 코드
    :return(emit):
        - message: emit 설명
        - isSuccess: 이벤트 수행 결과
        - nickName: 참여자 닉네임
    """
    nickname = data['nickName']
    code = data['roomCode']

    response_data = {
        'message': "The room exists.",
        'nickName': nickname,
    }

    sio.emit('join', response_data, room=code, skip_sid=sid)
    sio.send(response_data)
    print(f'[Server] {response_data}')


@sio.on('offer')
def offer(sid, data):
    """
    기존 참여자들의 정보를 새로운 참여자에게 전달
    :param sid:
        - SocketIO ID
    :param data:
        - roomCode: Room 코드
        - sdp: 참여자 peer 정보
    :return(emit):
        - message: emit 설명
        - sdp: 기존 참여자 peer 정보
        - isSuccess: 이벤트 수행 결과
    """
    code = data['roomCode']
    sdp = data['sdp']

    response_data = {
        'message': 'The information of the user currently in the room.',
        'roomCode': code,
        'sdp': sdp,
        'isSuccess': True
    }

    sio.emit('offer', response_data, room=code, skip_sid=sid)
    sio.send(response_data)
    print(f'[Server] {response_data}')


@sio.on('answer')
def answer(sid, data):
    """
    새로운 참여자의 정보를 서버로 전달
    :param sid:
        - SocketIO ID
    :param data:
        - roomCode: Room 코드
        - sdp: 참여자 peer 정보
    :return(emit):
        - message: emit 설명
        - sdp: 참여자 peer 정보
        - isSuccess: 이벤트 수행 결과
    """
    code = data['roomCode']
    sdp = data['sdp']

    response_data = {
        'message': 'The information of the user currently in the room.',
        'roomCode': code,
        'sdp': sdp,
        'isSuccess': True
    }

    sio.emit('answer', response_data, room=code, skip_sid=sid)
    sio.send(response_data)
    print(f'[Server] {response_data}')


@sio.on('bye')
def bye(sid, data):
    """
    Room 퇴장 이벤트
    :param sid:
        - SocketIO ID
    :param data:
        - roomCode: 퇴장한 Room 코드
        - nickName: 퇴장한 참여자 닉네임
    :return:
        - message: emit 설명
        - isSuccess: 이벤트 수행 결과
    """
    code = data['roomCode']
    nickname = data['nickName']

    response_data = {
        'message': f'[{sid}] {nickname} has left.',
        'isSuccess': True
    }

    sio.emit('answer', response_data, room=code, skip_sid=sid)
    sio.send(response_data)
    print(f'[Server] {response_data}')


def test(request):
    return render(request, 'chat.html')
