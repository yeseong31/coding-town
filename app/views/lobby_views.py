from flask import make_response, jsonify, request
from flask_restx import Namespace, Resource

ns = Namespace(
    name="Lobby",
    description="Coding Town Lobby API",
)


@ns.route('')
@ns.doc(responses={200: 'Success', 500: 'Failed'},
        params={
            'search': {'in': 'query', 'description': '조회할 방 이름', 'required': False}
        })
class Lobby(Resource):
    def get(self):
        """Lobby 정보 조회

        :parameter
        - search: 조회할 방 이름 (없으면 전체 방 정보 조회)

        :returns
        - roomCount: 생성된 방 개수
        - rooms: 생성된 방들의 정보를 담은 배열
            - roomName: 방 이름
            - roomCode: 방에 부여된 고유한 6자리 랜덤 번호
            - tags: 방에 설정된 태그
            - isPrivate: 비밀번호가 걸린 방인지 확인
            - password: 방 비밀번호 (isPrivate==False라면 빈 문자열)
            - currentUser: 방 참여자 수
            - totalUser: 방에 참여 가능한 참여자 수
        """
        # 로비 정보 확인
        # ...

        # 검색어
        search = request.args.get('search')
        if search is None:
            # 전체 정보 조회
            pass

        # search에 해당하는 방 정보 조회
        response_data = {
            'roomCount': 0,
            'rooms': {
                'roomName': 'test',
                'roomCode': 000000,
                'tags': ['tags'],
                'isPrivate': True,
                'password': 'test',
                'currentUser': 1,
                'totalUser': 5
            }
        }
        return make_response(jsonify(response_data))
