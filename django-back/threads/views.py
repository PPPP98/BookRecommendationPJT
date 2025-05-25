from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Prefetch
from django.contrib.auth import get_user_model
from .serializers import (
    ThreadCreateSerializer,
    ThreadDetailSerializer,
    CommentSerializer,
    ThreadListSerializer,
)
from .models import Thread, Comment
from django.shortcuts import get_object_or_404
from books.models import Book

User = get_user_model()


class ThreadPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def thread_create(requset, book_pk):
    """도서 별 스레드 생성 요청"""
    if requset.method == "POST":
        try:
            book = get_object_or_404(Book, pk=book_pk)
        except Book.DoesNotExist:
            return Response(
                {"error": "해당 도서를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ThreadCreateSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save(user=requset.user, book=book)
            response_serializer = ThreadDetailSerializer(
                serializer.instance, context={"request": requset}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def thread_detail(request, pk):
    """스레드 상세 조회"""
    try:
        thread = Thread.objects.prefetch_related("comments").get(pk=pk)
    except Thread.DoesNotExist:
        return Response(
            {"error": "스레드를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ThreadDetailSerializer(thread, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def thread_update_delete(request, pk):
    """스레드 수정 및 삭제"""
    try:
        thread = Thread.objects.get(pk=pk, user=request.user)
    except Thread.DoesNotExist:
        return Response(
            {"error": "스레드를 찾을 수 없거나 권한이 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PUT":
        serializer = ThreadDetailSerializer(
            thread,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        thread.delete()
        return Response(
            {"message": "성공적으로 삭제하였습니다"}, status=status.HTTP_204_NO_CONTENT
        )

    elif request.method == "GET":
        serializer = ThreadDetailSerializer(thread, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def thread_like(request, pk):
    """쓰레드 좋아요 토글"""
    try:
        thread = Thread.objects.get(pk=pk)
    except Thread.DoesNotExist:
        return Response(
            {"error": "쓰레드를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )

    user = request.user
    # exists()를 사용하여 쿼리 최적화
    is_liked = thread.liked_users.filter(id=user.id).exists()

    if is_liked:
        thread.liked_users.remove(user)
        liked = False
    else:
        thread.liked_users.add(user)
        liked = True

    # count()만 호출하여 쿼리 최적화
    like_count = thread.liked_users.count()

    return Response(
        {"liked": liked, "like_count": like_count}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_create(request, thread_pk):
    """댓글 생성"""
    try:
        thread = Thread.objects.get(pk=thread_pk)
    except Thread.DoesNotExist:
        return Response(
            {"error": "스레드를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    """댓글 조회, 수정, 삭제"""
    try:
        comment = Comment.objects.get(pk=comment_pk, user=request.user)
    except Comment.DoesNotExist:
        return Response(
            {"error": "댓글을 찾을 수 없거나 권한이 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        comment.delete()
        return Response(
            {"message": "성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def thread_list(request):
    """
    쓰레드 전체 목록 조회
    - 최신순 정렬
    - 페이지당 20개 로드
    - 좋아요 수, 댓글 수 포함
    """
    # DB 쿼리 최적화
    queryset = Thread.objects.select_related(
        'user', 'book'
    ).prefetch_related(
        Prefetch('liked_users', queryset=User.objects.only('id')),
        Prefetch('comments', queryset=Comment.objects.only('id', 'thread_id'))
    ).annotate(
        like_count=Count('liked_users', distinct=True),
        comment_count=Count('comments', distinct=True)
    ).only(
        'id', 'title', 'created_at',
        'user__id', 'user__nickname',
        'book__id', 'book__title', 'book__cover'
    ).order_by('-created_at')

    # 페이지네이션 적용
    paginator = ThreadPagination()
    paginated_threads = paginator.paginate_queryset(queryset, request)

    # 직렬화
    serializer = ThreadListSerializer(paginated_threads, many=True)
    response_data = {
        "count": paginator.page.paginator.count,
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "results": serializer.data,
    }

    return Response(response_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def popular_threads(request):
    """
    인기 쓰레드 조회 (좋아요 수 기준 상위 5개)
    GET /api/threads/popular/
    """
    # DB 쿼리 최적화
    queryset = Thread.objects.select_related(
        'user', 'book'
    ).prefetch_related(
        Prefetch('liked_users', queryset=User.objects.only('id')),
        Prefetch('comments', queryset=Comment.objects.only('id', 'thread_id'))
    ).annotate(
        like_count=Count('liked_users', distinct=True),
        comment_count=Count('comments', distinct=True)
    ).only(
        'id', 'title', 'created_at',
        'user__id', 'user__nickname', 'user__profile_image',
        'book__id', 'book__title', 'book__cover'
    ).order_by('-like_count')[:5]

    # 직렬화
    serializer = ThreadListSerializer(queryset, many=True)
    
    return Response(serializer.data)
