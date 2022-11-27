from flask import Blueprint, make_response, jsonify

from config import conn_mariadb

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    db = conn_mariadb()
    cursor = db.cursor()

    sql = 'SELECT * FROM TEST;'
    cursor.execute(sql)
    result = cursor.fetchone()
    # print(result)
    cursor.close()

    data = {'test': 200}
    return make_response(jsonify(data), 200)
