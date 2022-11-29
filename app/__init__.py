from flask import Flask, request, session, render_template
from flask_cors import CORS
from flask_restx import Api
from flask_socketio import SocketIO, emit, join_room

import config

users_in_room = {}  # 사용자
rooms_sid = {}  # 방
names_sid = {}  # 사용자 이름


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)
    
    CORS(app)
    app.secret_key = config.SECRET_KEY
    
    # ----- Api -----
    from .views.join_views import ns as join
    from .views.todo_views import ns as todo
    api = Api(
        app,
        version='0.1',
        title='Coding Town API Server',
        description="YS's Coding Town API Server",
        terms_url='/',
        contact_email='yeseong31@naver.com',
        license='MIT'
    )
    api.add_namespace(join, '/join')
    api.add_namespace(todo, '/todo')
    
    # --- Web RTC ---
    socketio = SocketIO(app)

    # @app.route('/test', methods=('GET',))
    # def test():
    #     display_name = request.args.get('display_name')  # 영상통화 사용자
    #     mute_audio = request.args.get('mute_audio')  # 1 or 0: 오디오 on/off
    #     mute_video = request.args.get('mute_video')  # 1 or 0: 영상 on/off
    #     room_id = request.args.get('room_id')
    #
    #     # 세션은 room_id를 키로 가짐
    #     session[room_id] = {'name': display_name,
    #                         'mute_audio': mute_audio,
    #                         'mute_video': mute_video}
    #
    #     return render_template('join.html',
    #                            room_id=room_id,
    #                            display_name=session[room_id]['name'],
    #                            mute_audio=session[room_id]['mute_audio'],
    #                            mute_video=session[room_id]['mute_video'])

    @socketio.on('connect')
    def on_connect():
        sid = request.sid
        print("New socket connected ", sid)

    @socketio.on('connect')
    def on_connect():
        print(f'New socket connected: {request.sid}')

    @socketio.on('join-room')
    def on_join_room(data):
        sid = request.sid
        room_id = data['room_id']
        display_name = session[room_id]['name']
    
        # register sid to the room
        join_room(room_id)
        rooms_sid[sid] = room_id
        names_sid[sid] = display_name
    
        # broadcast to others in the room
        print(f'[{room_id}] New member joined: {display_name}<{sid}>')
        emit('user-connect',
             {'sid': sid, 'name': display_name},
             broadcast=True,
             include_self=False,
             room=room_id)
    
        # add to user list maintained on server
        if room_id not in users_in_room:
            users_in_room[room_id] = [sid]
            emit('user-list', {'my_id': sid})  # send own id only
        else:
            user_list = {uid: names_sid[uid] for uid in users_in_room[room_id]}
            # send list of existing users to the new member
            emit('user-list', {'list': user_list, 'my_id': sid})
            # add new member to user list maintained on server
            users_in_room[room_id].append(sid)
    
        print(f'\nusers: {users_in_room}\n')

    @socketio.on('disconnect')
    def on_disconnect():
        sid = request.sid
        room_id = rooms_sid[sid]
        display_name = names_sid[sid]
    
        print(f'[{room_id}] Member left: {display_name}<{sid}>')
        emit('user-disconnect',
             {'sid': sid},
             broadcast=True,
             include_self=False,
             room=room_id)
    
        users_in_room[room_id].remove(sid)
        if len(users_in_room[room_id]) == 0:
            users_in_room.pop(room_id)
    
        rooms_sid.pop(sid)
        names_sid.pop(sid)
    
        print(f'\nusers: {users_in_room}\n')

    @socketio.on('data')
    def on_data(data):
        sender_sid = data['sender_id']
        target_sid = data['target_id']
    
        if sender_sid != request.sid:
            print("[Not supposed to happen!] request.sid and sender_id don't match!!!")
    
        if data['type'] != 'new-ice-candidate':
            print(f'{data["type"]} message from {sender_sid} to {target_sid}')
    
        socketio.emit('data', data, room=target_sid)
    
    return app
