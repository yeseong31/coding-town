import random

import bcrypt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.models import MyUser as User
from sockets.models import Room


@api_view(('POST',))
def room_post(request):
    """
    Room 생성 후 입장 코드 반환
    :param request:
    - roomName: 생성할 방 이름
    - nickName: 방 생성자 닉네임
    - password: 방 비밀번호
    :return:
    - roomCode: 생성된 방의 고유한 6자리 랜덤 번호
    """
    if request.method == 'POST':
        name = request.POST.get('roomName')
        password = request.POST.get('password')
        owner = request.POST.get('nickName')
        
        # 사용자가 존재하지 않으면 생성
        user = User.objects.get(nickname=owner)
        if not user:
            user = User.objects.create_user(owner)
        # 랜덤 시드 생성
        random.seed()
        # Room 생성
        room = Room(
            name=name,
            code=int(random.random() * 10 ** 6),
            is_private=False if password == '' or password is None else True,
            password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(),
            owner=user,
            current_num=1,
        )
        room.save()
        return Response({'roomCode': room.code}, status=status.HTTP_200_OK)
    else:
        return Response({'message': '[Server] Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
    