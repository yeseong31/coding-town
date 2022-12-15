from flask import request, session, render_template, make_response, jsonify, Blueprint
from flask_restx import Namespace, Resource, fields

bp = Blueprint('room', __name__, url_prefix='/')

ns = Namespace(
    name="Room",
    description="Coding Town Room API",
)

room_fields = ns.model(
    'Room',
    {
        'roomName': fields.String(description='생성할 방 이름', required=True, example='room1'),
        'nickName': fields.String(description='방 생성자 닉네임', required=True, example='홍길동'),
        'password': fields.String(description='비밀번호', required=True, example='asdf')
    }
)


@ns.route('room')
@ns.doc(responses={200: 'Success', 500: 'Failed'})
class CreateRoom(Resource):
    @ns.expect(room_fields)
    def post(self):
        """Room 입장에 필요한 정보를 확인한 뒤 입장 코드 반환

        :argument
        - roomName: 생성할 방 이름
        - nickName: 방 생성자 닉네임
        - password: 방 비밀번호

        :returns
        - roomCode: 생성된 방의 고유한 6자리 랜덤 번호
        """

        room_name = request.json.get('roomName')
        nickname = request.json.get('nickName')
        password = request.json.get('password')

        # 해당 방 이름이 존재하지 않으면 입장 불가
        # ...
        # 비밀번호가 일치하지 않으면 입장 불가
        # ...

        response_data = {
            'roomCode': 000000
        }
        return make_response(jsonify(response_data))


@bp.route('test', methods=('GET', 'POST'))
def test():
    return render_template('chat.html')
