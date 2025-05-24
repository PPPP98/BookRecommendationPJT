from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:book_pk>/create/', views.thread_create, name='thread_create'),
    path('<int:pk>/', views.thread_detail, name='thread_detail'),
]