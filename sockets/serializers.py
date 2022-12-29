from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    roomName = serializers.CharField(max_length=50, source='name')
    roomCode = serializers.IntegerField(source='code')
    isPrivate = serializers.BooleanField(source='is_private')
    currentUser = serializers.IntegerField(source='current_num')
    totalUser = serializers.IntegerField(source='total_num')

    class Meta:
        model = Room
        fields = ('roomName', 'roomCode', 'isPrivate', 'currentUser', 'totalUser', 'tags')
