from django.urls import path

from common.views import RegisterView, LoginView

app_name = 'common'

urlpatterns = [
    # ----- 회원가입 -----
    path('signup/', RegisterView.as_view(), name='signup'),
    # ----- 로그인 -----
    path('login/', LoginView.as_view(), name='login'),
]
