from django.urls import path
from . import views

urlpatterns = [
    # 쓰레드 목록 조회
    path('', views.thread_list, name='thread_list'),
    path('following/', views.following_threads, name='following-threads'),  # 팔로잉 유저의 쓰레드
    path('popular/', views.popular_threads, name='thread-popular'),  # 인기 쓰레드 조회
    path('books/<int:book_pk>/create/', views.thread_create, name='thread_create'),
    path('<int:pk>/', views.thread_detail, name='thread_detail'),
    path('<int:pk>/update-delete/', views.thread_update_delete, name='thread_update_delete'),
    path('<int:pk>/like/', views.thread_like, name='thread_like'),
    # 댓글 관련 URL
    path('<int:thread_pk>/comments/create/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
]