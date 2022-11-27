from flask import Blueprint, make_response, jsonify
from flask_restx import Namespace

from config import conn_mariadb

bp = Blueprint('meet', __name__, url_prefix='/meet')
Meet = Namespace(
    name="Meet",
    description="Coding Town 채널 API",
)


@bp.route('/')
def home():
    db = conn_mariadb()
    cursor = db.cursor()

    sql = 'SELECT * FROM TEST;'
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()

    data = {'result': result}
    return make_response(jsonify(data), 200)
