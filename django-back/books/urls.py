from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # 도서 목록 조회 (페이지네이션, 정렬, 카테고리 필터링 지원)
    path('', views.book_list, name='book_list'),
    
    # 도서 상세 조회
    path('<int:pk>/', views.book_detail, name='book_detail'),
    
    # 도서 좋아요/좋아요 취소
    path('<int:pk>/like/', views.book_like, name='book_like'),
    
    # 카테고리 목록 조회
    path('categories/', views.category_list, name='category_list'),    # 도서 검색
    path('search/', views.search_books, name='search_books'),
    
    # 검색어 자동완성
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
]