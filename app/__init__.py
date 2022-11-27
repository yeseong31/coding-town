from flask import Flask
from flask_cors import CORS

import config


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)

    CORS(app)
    app.secret_key = config.SECRET_KEY

    # ----- Blueprint -----
    from .views import base_views
    app.register_blueprint(base_views.bp)

    return app
