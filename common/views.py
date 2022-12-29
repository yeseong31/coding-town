from rest_framework import generics, status
from rest_framework.response import Response

from common.models import MyUser as User
from common.serializers import RegisterSerializer, SigninSerializer


class RegisterView(generics.CreateAPIView):
    """사용자 등록: POST"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class SigninView(generics.GenericAPIView):
    """사용자 조회 및 로그인: POST"""
    serializer_class = SigninSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({'token': token.key}, status=status.HTTP_200_OK)
