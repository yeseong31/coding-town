from flask import Flask, render_template
from flask_cors import CORS
from flask_restx import Api

from app.sockets import sio

app = Flask(__name__, static_url_path='/static')


def page_not_found(e):
    return render_template('404.html'), 404


def create_app():
    app.config.from_envvar('APP_CONFIG_FILE')
    CORS(app)
    
    # ----- Error Page -----
    app.register_error_handler(404, page_not_found)
    
    # ----- Api -----
    from .views import chat_views
    api = Api(
        app,
        version='0.1',
        title='Coding Town API Server',
        description="YS's Coding Town API Server",
        terms_url='/',
        contact_email='yeseong31@naver.com',
        license='MIT'
    )
    api.add_namespace(chat_views.ns, '/chat')
    
    # --- WebRTC ---
    sio.init_app(app)
    
    # ----- Blueprint -----
    app.register_blueprint(chat_views.bp)
    
    return app
