from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from .serializers import (
    UserFollowToggleSerializer,
    UserFollowListSerializer,
    UserProfileSerializer,
    BookSimpleSerializer,
    UserProfileUpdateSerializer,
)
from .paginations import UserListPagination
from books.models import Book
from .embedding_utils import find_similar_books_for_user, update_user_embedding
from books.serializers import BookSimilarSerializer

User = get_user_model()

@api_view(['GET'])
def check_username(request):
    """
    username 중복 체크
    GET /api/accounts/check-username/?username=검사할유저명
    """
    username = request.GET.get('username', '')
    if not username:
        return Response(
            {'error': 'Username is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = User.objects.filter(username=username).exists()
    return Response({'exists': exists})

@api_view(['GET'])
def check_email(request):
    """
    email 중복 체크
    GET /api/accounts/check-email/?email=검사할이메일
    """
    email = request.GET.get('email', '')
    if not email:
        return Response(
            {'error': 'Email is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = User.objects.filter(email=email).exists()
    return Response({'exists': exists})

@api_view(['GET'])
def check_nickname(request):
    """
    nickname 중복 체크
    GET /api/accounts/check-nickname/?nickname=검사할닉네임
    """
    nickname = request.GET.get('nickname', '')
    if not nickname:
        return Response(
            {'error': 'Nickname is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = User.objects.filter(nickname=nickname).exists()
    return Response({'exists': exists})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_toggle(request, user_id):
    """
    유저 팔로우/언팔로우 토글
    POST /api/accounts/{user_id}/follow/
    """
    target_user = get_object_or_404(User, id=user_id)
    user = request.user

    if user == target_user:
        return Response(
            {'error': '자기 자신을 팔로우할 수 없습니다.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if user.following.filter(id=target_user.id).exists():
        user.following.remove(target_user)
        is_following = False
    else:
        user.following.add(target_user)
        is_following = True

    # 팔로워/팔로잉 수 계산
    target_user = User.objects.annotate(
        follower_count=Count('followers', distinct=True),
        following_count=Count('following', distinct=True)
    ).get(id=user_id)

    serializer = UserFollowToggleSerializer(
        target_user,
        context={'request': request}
    )
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def following_list(request, user_id):
    """
    유저가 팔로우하는 사용자 목록 조회
    GET /api/accounts/{user_id}/following/
    """
    user = get_object_or_404(User, id=user_id)
    
    # 페이지네이션 설정
    paginator = UserListPagination()
    following = user.following.all().order_by('-id')  # 최신순
    paginated_following = paginator.paginate_queryset(following, request)

    serializer = UserFollowListSerializer(
        paginated_following,
        many=True,
        context={'request': request}
    )

    response_data = {
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data
    }

    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def followers_list(request, user_id):
    """
    유저를 팔로우하는 사용자 목록 조회
    GET /api/accounts/{user_id}/followers/
    """
    user = get_object_or_404(User, id=user_id)
    
    # 페이지네이션 설정
    paginator = UserListPagination()
    followers = user.followers.all().order_by('-id')  # 최신순
    paginated_followers = paginator.paginate_queryset(followers, request)

    serializer = UserFollowListSerializer(
        paginated_followers,
        many=True,
        context={'request': request}
    )

    response_data = {
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data
    }

    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def profile_detail(request, user_id):
    """
    유저 프로필 상세 정보 조회
    GET /api/accounts/{user_id}/profile/
    - 기본 정보
    - 팔로워/팔로잉 수
    - 최근 좋아요한 책 5개
    - 최근 팔로우한 사용자 5명
    """
    # 프로필 정보 조회 및 최적화
    user = User.objects.annotate(
        follower_count=Count('followers', distinct=True),
        following_count=Count('following', distinct=True)
    ).prefetch_related(
        Prefetch(
            'like_books',
            queryset=Book.objects.only('id', 'title', 'author', 'cover').order_by('-id')[:5],
            to_attr='recent_liked_books'
        ),
        Prefetch(
            'following',
            queryset=User.objects.only('id', 'nickname', 'profile_image').order_by('-id')[:5],
            to_attr='recent_following'
        )
    ).get(id=user_id)

    serializer = UserProfileSerializer(
        user,
        context={'request': request}
    )

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def liked_books(request, user_id):
    """
    유저가 좋아요한 도서 목록 조회
    GET /api/accounts/{user_id}/liked-books/
    """
    user = get_object_or_404(User, id=user_id)
    
    # 페이지네이션 설정
    paginator = UserListPagination()
    liked_books = user.like_books.all().order_by('-id')  # 최신순
    paginated_books = paginator.paginate_queryset(liked_books, request)

    serializer = BookSimpleSerializer(paginated_books, many=True)

    response_data = {
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data
    }

    return Response(response_data)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    프로필 조회 및 수정
    GET /api/accounts/profile/ : 프로필 조회
    PUT /api/accounts/profile/ : 프로필 수정
    """
    user = request.user

    if request.method == 'GET':
        # 팔로워/팔로잉 수 계산
        user = User.objects.annotate(
            follower_count=Count('followers', distinct=True),
            following_count=Count('following', distinct=True)
        ).prefetch_related(
            'interested_categories',
            Prefetch(
                'like_books',
                queryset=Book.objects.all()[:5],
                to_attr='recent_liked_books'
            ),
            Prefetch(
                'following',
                queryset=User.objects.all()[:5],
                to_attr='recent_following'
            )
        ).get(id=user.id)

        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileUpdateSerializer(
            user, 
            data=request.data, 
            context={'request': request},
            partial=True
        )
        
        if serializer.is_valid():
            # 관심 카테고리 처리
            if 'interested_categories' in request.data:
                user.interested_categories.set(serializer.validated_data.get('interested_categories', []))
            
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_books(request):
    """
    현재 사용자에게 맞춤 도서를 추천합니다.
    GET /api/accounts/recommended-books/
    """
    user = request.user

    # 임베딩 벡터가 없는 경우 생성
    if not user.embedding_vector:
        success = update_user_embedding(user)
        if not success:
            return Response(
                {'error': '사용자 프로필 데이터가 부족합니다. 관심 카테고리나 자기소개를 추가해주세요.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    # 유사한 책 검색
    similar_books = find_similar_books_for_user(user, top_k=5)
    
    if not similar_books:
        return Response(
            {'error': '추천할 만한 도서를 찾지 못했습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = BookSimilarSerializer(similar_books, many=True)
    return Response(serializer.data)