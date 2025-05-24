from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:book_pk>/create/', views.thread_create, name='thread_create'),
    path('<int:pk>/', views.thread_detail, name='thread_detail'),
    path('<int:pk>/update-delete/', views.thread_update_delete, name='thread_update_delete'),
]