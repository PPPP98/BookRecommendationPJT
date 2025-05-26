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
    
    # 프로필 관련 URLs
    path('profile/', views.profile, name='profile'),  # 내 프로필 조회/수정
    
    # 팔로우 관련 URLs
    path('<int:user_id>/follow/', views.follow_toggle, name='follow-toggle'),
    path('<int:user_id>/following/', views.following_list, name='following-list'),
    path('<int:user_id>/followers/', views.followers_list, name='followers-list'),
    path('<int:user_id>/profile/', views.profile_detail, name='profile-detail'),
    path('<int:user_id>/liked-books/', views.liked_books, name='liked-books'),
]
