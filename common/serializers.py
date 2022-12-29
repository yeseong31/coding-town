from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from common.models import MyUser as User


class RegisterSerializer(serializers.ModelSerializer):
    """회원 등록 Serializer"""
    
    nickname = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=False
    )
    
    class Meta:
        model = User
        fields = ('nickname', 'password', 'password2',)
    
    def validate(self, data):
        """
        비밀번호 일치 여부 확인

        :arguments:
        - password: 비밀번호
        - password2: 비밀번호 확인
        :returns:
        - data: 전달된 password와 password2 정보
        """
        # if data['password'] != data['password2']:
        #     raise serializers.ValidationError({'password': "Password fields didn't match."})
        return data
    
    def create(self, validated_data):
        """
        CREATE 요청에 대해 create() 메서드를 overwrite 및 User/Token 생성

        :arguments:
        - nickname: 사용자 닉네임
        - password: 비밀번호
        :returns:
        - user: 생성된 사용자
        """
        user = User.objects.create_user(
            nickname=validated_data['nickname'],
            # password=validated_data['password'],
        )
        # user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class SigninSerializer(serializers.Serializer):
    """회원 조회 Serializer"""
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(required=False, write_only=True)
    
    def validate(self, data):
        # user = authenticate(**data)
        user = User.objects.get(nickname=data['nickname'])
        if user:
            return Token.objects.get(user=user)
        raise serializers.ValidationError({'error': 'Unable to sign in with provided credentials.'})
