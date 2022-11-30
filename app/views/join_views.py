from flask import request, session, make_response, jsonify, current_app
from flask_restx import Namespace, Resource

ns = Namespace(
    name="Join",
    description="Coding Town 채널 API",
)


@ns.route('/')
@ns.doc(params={'room_id': '방 ID',
                'display_name': '화면 공유 사용자 이름',
                'mute_audio': '오디오 on/off 여부',
                'mute_video': '영상 on/off 여부'},
        responses={202: 'Success', 500: 'Failed'})
class Join(Resource):
    def get(self):
        display_name = request.args.get('display_name')  # 영상통화 사용자
        mute_audio = request.args.get('mute_audio')  # 1 or 0: 오디오 on/off
        mute_video = request.args.get('mute_video')  # 1 or 0: 영상 on/off
        room_id = request.args.get('room_id')
        
        # 세션은 room_id를 키로 가짐
        session[room_id] = {'name': display_name,
                            'mute_audio': mute_audio,
                            'mute_video': mute_video}

        current_app.logger.info("INFO 레벨로 출력")
        return make_response(jsonify(session[room_id]))
