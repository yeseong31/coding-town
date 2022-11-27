from flask import Flask
from flask_cors import CORS
from flask_restx import Api

import config


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)

    CORS(app)
    app.secret_key = config.SECRET_KEY

    # ----- Blueprint -----
    from .views import todo_views, meet_views
    app.register_blueprint(todo_views.bp)
    app.register_blueprint(meet_views.bp)

    # ----- Api -----
    from .views.meet_views import Meet
    from .views.todo_views import Todos
    api = Api(
        app,
        version='0.1',
        title='Coding Town API Server',
        description="YS's Coding Town API Server",
        terms_url='/',
        contact_email='yeseong31@naver.com',
        license='MIT'
    )
    api.add_namespace(Meet, '/meet')
    api.add_namespace(Todos, '/todo')

    return app
