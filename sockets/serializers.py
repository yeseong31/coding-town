from rest_framework import serializers

from .models import Room, Tag


class TagSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name
    
    class Meta:
        model = Tag
        fields = ('name',)


class RoomsSerializer(serializers.ModelSerializer):
    roomName = serializers.CharField(max_length=50, source='name', help_text='Room 이름')
    roomCode = serializers.IntegerField(source='code', help_text='Room 코드')
    isPrivate = serializers.BooleanField(source='is_private', help_text='Room 암호화 여부')
    currentUser = serializers.IntegerField(source='current_num', help_text='Room 현재 입장 인원 수')
    totalUser = serializers.IntegerField(source='total_num', help_text='Room 입장 제한 인원 수')
    tags = TagSerializer(read_only=True, many=True)
    
    class Meta:
        model = Room
        fields = ('roomName', 'roomCode', 'isPrivate', 'currentUser', 'totalUser', 'tags',)
        extra_kwargs = {'roomCode': {'write_only': True}}
        depth = 1


class CreateRoomSerializer(serializers.ModelSerializer):
    roomName = serializers.CharField(max_length=50, source='name', help_text='생성할 Room 이름', required=True)
    nickName = serializers.CharField(max_length=128, source='owner', help_text='Room 생성자 닉네임', required=True)
    password = serializers.CharField(max_length=128, help_text='Room 비밀번호', required=False)
    tags = TagSerializer(many=True, help_text='Room에 등록할 태그', required=False)
    
    class Meta:
        model = Room
        fields = ('roomName', 'nickName', 'password', 'tags',)
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1


class JoinRoomSerializer(serializers.ModelSerializer):
    roomName = serializers.CharField(max_length=50, source='name', help_text='Room 이름', required=True)
    roomCode = serializers.IntegerField(source='code', help_text='Room 코드', required=True)
    nickName = serializers.CharField(max_length=128, source='owner', help_text='Room 생성자 닉네임', required=True)
    password = serializers.CharField(max_length=128, help_text='Room 비밀번호', required=False)
    
    class Meta:
        model = Room
        fields = ('roomName', 'roomCode', 'nickName', 'password',)
        extra_kwargs = {'roomCode': {'write_only': True}, 'password': {'write_only': True}}
        depth = 1
    
