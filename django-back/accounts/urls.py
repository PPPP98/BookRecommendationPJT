from django.urls import path, include
from . import views

urlpatterns = [
    # dj-rest-auth URLs
    path('', include('dj_rest_auth.urls')),  # 로그인, 로그아웃
    path('registration/', include('dj_rest_auth.registration.urls')),  # 회원가입
    
    # 중복 체크 URLs
    path('check-username/', views.check_username, name='check-username'),
    path('check-email/', views.check_email, name='check-email'),
    path('check-nickname/', views.check_nickname, name='check-nickname'),
    
    # 커스텀 URLs
    # path('delete/', views.delete_user, name='user-delete'),  # 회원탈퇴
    # path('profile/', views.user_detail, name='user-detail'),  # 프로필 조회
]
