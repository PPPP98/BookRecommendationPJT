from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import ThreadCreateSerializer, ThreadDetailSerializer
from .models import Thread
from django.shortcuts import get_object_or_404
from books.models import Book
from django.db.models import Count


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def thread_create(requset, book_pk):
    """도서 별 스레드 리스트 조회, 생성 요청"""
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
