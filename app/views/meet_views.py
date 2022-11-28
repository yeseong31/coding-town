from flask import make_response, jsonify
from flask_restx import Namespace, Resource

from config import conn_mariadb

ns = Namespace(
    name="Meet",
    description="Coding Town 채널 API",
)


@ns.route('/')
class Meet(Resource):
    def get(self):
        db = conn_mariadb()
        cursor = db.cursor()
    
        sql = 'SELECT * FROM TEST;'
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
    
        data = {'result': result}
        return make_response(jsonify(data), 200)
