import os

import socketio
from django.http import HttpResponse
from django.shortcuts import render

from common.models import MyUser as User
from config.settings.base import BASE_DIR
from sockets.models import Room

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

    :argument
        - nickName: 방 생성자 닉네임
        - roomCode: 입장하려는 방 코드

    :returns
        - isSuccess: 방 생성 성공 여부
    """
    owner = data['nickName']
    code = data['roomCode']
    
    room = Room.objects.get(code=code)
    # 존재하지 않는 Room인 경우
    if not room:
        response_data = {
            'message': "This room doesn't exist.",
            'isSuccess': False
        }
    # 방 생성자가 아닌 경우
    elif room.owner != owner:
        response_data = {
            'message': "The nickname you received is different from the nickname of the room creator.",
            'isSuccess': False
        }
    # 방 생성
    else:
        sio.enter_room(sid, code)
        room.current_num += 1
        response_data = {
            'message': f"{owner} has entered the room.",
            'isSuccess': True
        }
    sio.emit('create', response_data)
    print(f'[Server] {response_data["message"]}')
        

@sio.on('join')
def join(sid, data):
    """
    새로운 사람의 Room 참여 정보를 기존 Room 참여자들에게 전달

    :argument:
        - nickName: 방 참여자 닉네임
        - roomCode: 입장하려는 방 코드
    """
    nickname = data['nickName']
    room_code = data['roomCode']
    print(nickname, room_code)


@sio.on('offer')
def offer(sid, data):
    """
    기존 참여자들의 정보를 새로운 참여자에게 전달

    :argument:
        - roomCode: 입장하려는 방 코드
        - sdp: 참여자의 peer 정보
    """
    room_code = data['roomCode']
    sdp = data['sdp']
    print(room_code, sdp)


@sio.on('answer')
def answer(sid, data):
    """
    새로운 참여자의 정보를 서버로 전달

    :argument:
        - roomCode: 입장하려는 방 코드
        - sdp: 참여자의 peer 정보
    """
    room_code = data['roomCode']
    sdp = data['sdp']
    print(room_code, sdp)


def test(request):
    return render(request, 'chat.html')
