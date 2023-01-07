from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from common.models import MyUser as User
from common.serializers import RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    """
    사용자 등록(회원가입)
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    """
    사용자 조회 및 로그인
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({'token': token.key}, status=status.HTTP_200_OK)


def page_not_found(request, exception):
    return render(request, '404.html', {})
