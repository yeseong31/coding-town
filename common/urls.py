from django.urls import path

from common.views import RegisterView, SigninView

app_name = 'common'

urlpatterns = [
    # ----- 회원 등록 -----
    path('register/', RegisterView.as_view()),
    # ----- 회원 조회 -----
    path('signin/', SigninView.as_view()),
]