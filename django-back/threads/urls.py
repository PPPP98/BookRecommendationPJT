from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:book_pk>/create/', views.thread_create, name='thread_create'),
    path('<int:pk>/', views.thread_detail, name='thread_detail'),
    path('<int:pk>/update-delete/', views.thread_update_delete, name='thread_update_delete'),
    path('<int:pk>/like/', views.thread_like, name='thread_like'),
    # 댓글 관련 URL
    path('<int:thread_pk>/comments/create/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
]