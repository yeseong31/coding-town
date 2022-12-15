from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from app.sockets import sio


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def page_not_found(e):
    """404 Not Found 페이지"""
    return render_template('404.html'), 404


def bad_gateway(e):
    """502 Bad Gateway 페이지"""
    return render_template('502.html'), 502


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_envvar('APP_CONFIG_FILE')
    CORS(app)
    Bcrypt(app)

    # ----- Error Page -----
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(502, bad_gateway)
    
    # ----- DB -----
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # ----- Api -----
    from .views import room_views, lobby_views
    api = Api(
        app,
        version='0.1',
        title='Coding Town API Server',
        description="YS's Coding Town API Server",
        terms_url='/',
        contact_email='yeseong31@naver.com',
        license='MIT'
    )
    api.add_namespace(room_views.ns, '/')
    api.add_namespace(lobby_views.ns, '/lobby')

    # --- WebRTC ---
    sio.init_app(app,
                 cors_allowed_origins='*',
                 logger=True,
                 engineio_logger=True)

    # ----- Blueprint -----
    app.register_blueprint(room_views.bp)

    return app
