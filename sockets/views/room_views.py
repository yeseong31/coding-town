import random

import bcrypt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

        # Room 정보 확인
        room = Room.objects.filter(name=name).first()
        # Room 이름이 중복되는 경우
        if room:
            return Response(
                {
                    'message': '[Server] There is already a Room with a duplicate name.',
                    'roomCode': -1,
                    'isSuccess': False
                },
                status=status.HTTP_400_BAD_REQUEST)

        # 랜덤 시드 생성
        random.seed()

        # Room 생성 및 저장
        room = Room(
            name=name,
            code=int(random.random() * 10 ** 6),
            is_private=False if password == '' or password is None else True,
            password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(),
            owner=owner,
        )
        room.save()

        return Response(
            {
                'roomCode': room.code,
                'isSuccess': True
            },
            status=status.HTTP_201_CREATED)

    # POST 요청이 아닌 경우
    else:
        return Response(
            {
                'message': '[Server] Invalid request.',
                'roomCode': -1,
                'isSuccess': False
            },
            status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def room_join(request):
    """
    Room 참가 가능 여부 확인
    :param request:
    - roomName: 참가하고자 하는 방 이름
    - roomCode: 참가하고자 하는 방 코드
    - nickName: 참가자 닉네임
    - password: 방 비밀번호 (is_private 활성 시 빈 문자열)
    :return:
    - isSuccess: 참가 가능 여부 (비밀번호를 잘못 입력하거나 존재하지 않는 방이라면 False)
    - message: 참가 불가능한 이유 (isSuccess가 True이면 빈 문자열)
    """
    if request.method == 'POST':
        name = request.POST.get('roomName')
        code = request.POST.get('roomCode')
        nickname = request.POST.get('nickName')
        password = request.POST.get('password')

        # Room 정보 확인
        room = Room.objects.get(name=name, code=code)
        # 존재하지 않는 Room인 경우
        if not room:
            return Response(
                {
                    'message': "[Server] This room doesn't exist.",
                    'isSuccess': False
                },
                status=status.HTTP_400_BAD_REQUEST)
        # 비밀번호를 입력하지 않은 경우
        elif room.is_private and not password:
            return Response(
                {
                    'message': "[Server] The room with the password set. Please enter your password.",
                    'isSuccess': False
                },
                status=status.HTTP_400_BAD_REQUEST)
        # 잘못된 비밀번호를 입력한 경우
        elif password and not bcrypt.checkpw(password.encode('utf-8'), room.password.encode('utf-8')):
            return Response(
                {
                    'message': "[Server] Invalid password entered.",
                    'isSuccess': False
                },
                status=status.HTTP_401_UNAUTHORIZED)
        # Room 참가 가능한 경우
        else:
            return Response(
                {
                    'message': f"[Server] {nickname} can participate in the room.",
                    'isSuccess': True
                },
                status=status.HTTP_202_ACCEPTED)

    # POST 요청이 아닌 경우
    else:
        return Response(
            {
                'message': '[Server] Invalid request.',
                'isSuccess': False
            },
            status=status.HTTP_400_BAD_REQUEST)
