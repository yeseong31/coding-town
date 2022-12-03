# 데코레이터 함수 기반 Namespace
from flask import session
from flask_socketio import join_room, emit, leave_room, Namespace


class ChatNamepsace(Namespace):
    
    def on_connect(self):
        pass
    
    def on_disconnect(self):
        pass
    
    def on_joined(self, data):
        room = session.get('room')
        join_room(room)
        emit('status', {'msg': session.get('name') + '님이 입장하셨습니다'}, room=room)
    
    def on_text(self, data):
        room = session.get('room')
        emit('message', {'msg': session.get('name') + ':' + data['msg']}, room=room)
    
    def on_left(self, data):
        room = session.get('room')
        leave_room(room)
        emit('status', {'msg': session.get('name') + '님이 퇴장하셨습니다'}, room=room)


def socketio_init(sio):
    @sio.on('joined', namespace='/chat')
    def joined(message):
        room = session.get('room')
        join_room(room)
        emit('status', {'msg': session.get('name') + '님이 입장하셨습니다'}, room=room)
    
    @sio.on('text', namespace='/chat')
    def text(message):
        room = session.get('room')
        emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)
    
    @sio.on('left', namespace='/chat')
    def left(message):
        room = session.get('room')
        leave_room(room)
        emit('status', {'msg': session.get('name') + '님이 퇴장하셨습니다'}, room=room)
