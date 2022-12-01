from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_socketio import SocketIO, join_room, send, leave_room, emit

users_in_room = {}  # 사용자
rooms_sid = {}  # 방
names_sid = {}  # 사용자 이름


def page_not_found(e):
    return render_template('404.html'), 404


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_envvar('APP_CONFIG_FILE')
    CORS(app)
    
    # ----- Error Page -----
    app.register_error_handler(404, page_not_found)
    
    # ----- Api -----
    from .views.join_views import ns as join
    from .views.auth_views import ns as auth
    from .views.test_views import ns as test
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
    api.add_namespace(auth, '/auth')
    api.add_namespace(test, '/test')
    
    # --- Web RTC ---
    sio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

    @sio.on('connect')
    def message_received(methods=('GET', 'POST')):
        return make_response(jsonify({'message': '메시지 받았음!'}), 200)
    
    return app
