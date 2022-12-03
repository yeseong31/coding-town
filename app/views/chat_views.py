from flask import request, session, render_template, make_response, jsonify, Blueprint
from flask_restx import Namespace, Resource, fields

bp = Blueprint('chat', __name__, url_prefix='/chat')

ns = Namespace(
    name="Chat",
    description="Coding Town Test Chat API",
)
chat_fields = ns.model(
    'Chat',
    {'name': fields.String(description='이름', required=True, example='홍길동'),
     'room': fields.String(description='방 이름', required=True, example='asdf')}
)


@ns.route('/')
@ns.doc(responses={202: 'Success', 500: 'Failed'})
class Index(Resource):
    @ns.expect(chat_fields)
    def post(self):
        session['name'] = request.json.get('name')
        session['room'] = request.json.get('room')
        data = {
            'session_name': session['name'],
            'session_room': session['room']
        }
        return make_response(jsonify(data), 200)


@bp.route('/test', methods=('GET', 'POST'))
def test():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        data = {
            'message': '이름 및 방 이름이 지정되지 않았습니다.'
        }
        return make_response(jsonify(data), 500)
    # data = {
    #     'name': session['name'],
    #     'room': session['room']
    # }
    # return make_response(jsonify(data), 200)
    return render_template('chat.html', name=name, room=room)
