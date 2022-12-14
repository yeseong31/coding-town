import json
import random

import bcrypt
from django.core.paginator import Paginator
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sockets.models import Room, Tag
from sockets.serializers import RoomsSerializer, CreateRoomSerializer, JoinRoomSerializer


class RoomsAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description='검색어',
                default='',
                type=openapi.TYPE_STRING,
                required=False)
        ],
        responses={
            200: 'OK',
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def get(self, request):
        """
        Room 전체 목록 조회
        
        :param request:
        - search: 검색어 (Room 이름, Tag 이름, Room 생성자 닉네임 등)
        
        :return:
        - roomCount: 생성된 Room의 수
        - rooms: 생성된 Room 정보 리스트
            - roomName: Room 이름
            - roomCode: Room 코드
            - isPrivate: Room 암호화 여부
            - password: Room 비밀번호 (isPrivate이 False인 경우 빈 문자열)
            - currentUser: Room 현재 입장 인원 수
            - totalUser: Room 입장 제한 인원 수
        """
        page = request.GET.get('page', '1')
        search = request.GET.get('search', '')
        room_list = Room.objects.order_by('-created_at')
        
        if search:
            room_list = room_list.filter(
                Q(name__icontains=search) |  # Room 이름 검색
                Q(owner__icontains=search) |  # Room 생성자 닉네임 검색
                Q(tags__name__icontains=search)  # Tag 이름 검색
            ).distinct()
        
        paginator = Paginator(room_list, 20)
        page_obj = paginator.get_page(page)
        
        serializer = RoomsSerializer(page_obj, many=True)
        response_data = {
            'page': page,
            'search': search,
            'roomCount': len(serializer.data),
            'rooms': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CreateRoomAPI(APIView):
    @swagger_auto_schema(
        request_body=CreateRoomSerializer,
        responses={
            201: 'Created',
            400: 'Bed Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request):
        """
        Room 생성 후 입장 코드 반환
        
        :param request:
        - roomName: 생성할 Room 이름
        - nickName: Room 생성자 닉네임
        - password: Room 비밀번호
        
        :return:
        - roomCode: 생성된 Room의 고유한 6자리 랜덤 번호
        """
        request = json.loads(request.body)
        name = request.get('roomName')
        owner = request.get('nickName')
        password = request.get('password', '')
        tags = request.get('tags')
        
        # 필요한 정보가 제대로 전달되지 않은 경우
        if not (name and owner):
            return Response(
                {
                    'message': '[Server] The required information was not delivered properly. ',
                    'roomCode': -1,
                    'isSuccess': False
                },
                status=status.HTTP_400_BAD_REQUEST)
        
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
            is_private=False if password == '' else True,
            password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(),
            owner=owner,
        )
        room.save()
        
        # Tag 생성 및 저장
        if tags:
            for tag_name in tags:
                tag = Tag.objects.filter(name=tag_name, slug=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name, slug=tag_name)
                    tag.save()
                room.tags.add(tag)
            room.save()
        
        return Response(
            {
                'roomCode': room.code,
                'isSuccess': True
            },
            status=status.HTTP_201_CREATED)


class JoinRoomAPI(APIView):
    @swagger_auto_schema(
        request_body=JoinRoomSerializer,
        responses={
            201: 'Created',
            400: 'Bed Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request):
        """
        Room 참가 가능 여부 확인
        
        :param request:
        - roomName: 참가하고자 하는 Room 이름
        - roomCode: 참가하고자 하는 Room 코드
        - nickName: 참가자 닉네임
        - password: Room 비밀번호 (is_private이 False인 경우 빈 문자열)
        
        :return:
        - isSuccess: Room 참가 가능 여부 (비밀번호를 잘못 입력하거나 존재하지 않는 방이라면 False)
        - message: Room 참가 불가능한 이유 (isSuccess가 True인 경우 빈 문자열)
        """
        request = json.loads(request.body)
        name = request.get('roomName')
        code = request.get('roomCode')
        nickname = request.get('nickName')
        password = request.get('password', '')
        
        # 필요한 정보가 제대로 전달되지 않은 경우
        if not (name and code and nickname):
            return Response(
                {
                    'message': '[Server] The required information was not delivered properly. ',
                    'roomCode': -1,
                    'isSuccess': False
                },
                status=status.HTTP_400_BAD_REQUEST)
        
        # Room 정보 확인
        room = Room.objects.get(name=name, code=code)
        # 존재하지 않는 Room인 경우
        if not room:
            return Response(
                {
                    'message': "[Server] This room doesn't exist.",
                    'roomCode': -1,
                    'isSuccess': False
                },
                status=status.HTTP_400_BAD_REQUEST)
        # 비밀번호를 입력하지 않은 경우
        elif room.is_private and not password:
            return Response(
                {
                    'message': "[Server] The room with the password set. Please enter your password.",
                    'roomCode': -1,
                    'isSuccess': False
                },
                status=status.HTTP_400_BAD_REQUEST)
        # 잘못된 비밀번호를 입력한 경우
        elif password and not bcrypt.checkpw(password.encode('utf-8'), room.password.encode('utf-8')):
            return Response(
                {
                    'message': "[Server] Invalid password entered.",
                    'roomCode': -1,
                    'isSuccess': False
                },
                status=status.HTTP_401_UNAUTHORIZED)
        # Room 참가 가능한 경우
        else:
            return Response(
                {
                    'message': f"[Server] {nickname} can participate in the room.",
                    'roomCode': code,
                    'isSuccess': True
                },
                status=status.HTTP_202_ACCEPTED)
