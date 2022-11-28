from flask import Flask
from flask_cors import CORS
from flask_restx import Api

import config


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)

    CORS(app)
    app.secret_key = config.SECRET_KEY

    # ----- Api -----
    from .views.meet_views import ns as meet
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
    api.add_namespace(meet, '/meet')
    api.add_namespace(todo, '/todo')

    return app
