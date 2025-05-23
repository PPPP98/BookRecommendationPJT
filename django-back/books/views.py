from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import BookListSerializer, BookDetailSerializer
from .models import Book, Category

class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def book_list(request):    # 기본 쿼리셋 with 최적화
    queryset = Book.objects.select_related('category').annotate(
        like_count=Count('liked_users', distinct=True),
        thread_count=Count('threads', distinct=True)
    )
    
    # 카테고리 필터링
    category = request.query_params.get('category', None)
    if category:
        queryset = queryset.filter(category__name=category)
    
    # 정렬
    ordering = request.query_params.get('ordering', '-pub_date')
    if ordering == '-like_count':
        queryset = queryset.order_by('-like_count')
    elif ordering == '-thread_count':
        queryset = queryset.order_by('-thread_count')
    else:
        queryset = queryset.order_by('-pub_date')
    
    # 페이지네이션
    paginator = CustomPagination()
    page = paginator.paginate_queryset(queryset, request)
    
    serializer = BookListSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def book_detail(request, pk):
    try:
        book = Book.objects.select_related('category').prefetch_related('threads').annotate(
            like_count=Count('liked_users', distinct=True),
            thread_count=Count('threads', distinct=True)
        ).get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': '도서를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookDetailSerializer(book, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    return Response({
        'categories': [{'id': cat.id, 'name': cat.name} for cat in categories]
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_like(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': '도서를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    # exists()를 사용하여 쿼리 최적화
    is_liked = book.liked_users.filter(id=user.id).exists()
    
    if is_liked:
        book.liked_users.remove(user)
        liked = False
    else:
        book.liked_users.add(user)
        liked = True
    
    # count()만 호출하여 쿼리 최적화
    like_count = book.liked_users.count()
    
    return Response({
        'liked': liked,
        'like_count': like_count
    }, status=status.HTTP_200_OK)
