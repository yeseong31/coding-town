import random
from datetime import datetime

import bcrypt
from flask import request, render_template, make_response, jsonify, Blueprint, flash
from flask_restx import Namespace, Resource, fields

from app import db
from app.models import Room, User

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


@ns.route('/')
@ns.doc(responses={200: 'OK', 201: 'Created', 400: 'Bad Request', 500: 'Failed'})
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

        # 유효성 검사
        room_name = request.json.get('roomName')
        password = request.json.get('password')
        nickname = request.json.get('nickName')

        if not (room_name or password or nickname):
            message = '필요한 데이터가 제대로 전달되지 않았습니다.'
            flash(message)
            return make_response(jsonify({'message': message}), 400)

        # 사용자 확인
        user = User.query.filter_by(nickname=nickname).first()
        if not user:
            user = User(nickname=nickname)
            db.session.add(user)
            db.session.commit()

        # 랜덤 시드 설정
        random.seed()

        # 방 생성
        room = Room(room_name=room_name,
                    room_code=int(random.random() * 10 ** 6),
                    is_private=False if password == '' or password is None else True,
                    password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                    current_user=0,
                    total_user=10,
                    room_owner=user.id,
                    created_at=datetime.now())
        db.session.add(room)
        db.session.commit()

        response_data = {
            'roomCode': room.room_code
        }
        return make_response(jsonify(response_data))


@bp.route('test', methods=('GET', 'POST'))
def test():
    return render_template('chat.html')
