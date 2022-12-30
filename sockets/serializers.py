from rest_framework import serializers

from .models import Room, Tag


class TagSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name
    
    class Meta:
        model = Tag


class RoomSerializer(serializers.ModelSerializer):
    roomName = serializers.CharField(max_length=50, source='name')
    roomCode = serializers.IntegerField(source='code')
    isPrivate = serializers.BooleanField(source='is_private')
    currentUser = serializers.IntegerField(source='current_num')
    totalUser = serializers.IntegerField(source='total_num')
    tags = TagSerializer(read_only=True, many=True)
    
    class Meta:
        model = Room
        fields = ('roomName', 'roomCode', 'isPrivate', 'currentUser', 'totalUser', 'tags',)
        extra_kwargs = {'roomCode': {'write_only': True}}
        depth = 1
