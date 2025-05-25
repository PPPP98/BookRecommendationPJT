from django.core.cache import cache
from django.db.models import Count, Q, F, Value, CharField, Case, When, IntegerField
from django.db.models.functions import Lower
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import BookListSerializer, BookDetailSerializer
from .models import Book, Category
from .utils import preprocess_search_query, build_search_query, calculate_search_score

class BookSearchUserThrottle(UserRateThrottle):
    rate = '60/minute'  # 인증된 사용자는 분당 60회 요청 가능

class BookSearchAnonThrottle(AnonRateThrottle):
    rate = '30/minute'  # 비인증 사용자는 분당 30회 요청 가능

class SuggestionUserThrottle(UserRateThrottle):
    rate = '180/minute'  # 인증된 사용자는 분당 180회 요청 가능 (3회/초)

class SuggestionAnonThrottle(AnonRateThrottle):
    rate = '120/minute'  # 비인증 사용자는 분당 120회 요청 가능 (2회/초)


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


@api_view(["GET"])
def book_list(request):  # 기본 쿼리셋 with 최적화
    queryset = Book.objects.select_related("category").annotate(
        like_count=Count("liked_users", distinct=True),
        thread_count=Count("threads", distinct=True),
    )

    # 카테고리 필터링
    category = request.query_params.get("category", None)
    if category:
        queryset = queryset.filter(category__name=category)

    # 정렬
    ordering = request.query_params.get("ordering", "-pub_date")
    if ordering == "-like_count":
        queryset = queryset.order_by("-like_count")
    elif ordering == "-thread_count":
        queryset = queryset.order_by("-thread_count")
    else:
        queryset = queryset.order_by("-pub_date")

    # 페이지네이션
    paginator = CustomPagination()
    page = paginator.paginate_queryset(queryset, request)

    serializer = BookListSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def book_detail(request, pk):
    try:
        book = (
            Book.objects.select_related("category")
            .prefetch_related("threads")
            .annotate(
                like_count=Count("liked_users", distinct=True),
                thread_count=Count("threads", distinct=True),
            )
            .get(pk=pk)
        )
    except Book.DoesNotExist:
        return Response(
            {"error": "도서를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = BookDetailSerializer(book, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    return Response(
        {"categories": [{"id": cat.id, "name": cat.name} for cat in categories]},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_like(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            {"error": "도서를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )

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

    return Response(
        {"liked": liked, "like_count": like_count}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@throttle_classes([BookSearchUserThrottle, BookSearchAnonThrottle])
def search_books(request):
    """
    도서 검색 API
    - 제목, 저자, 출판사, 설명 검색
    - 필드 지정 검색
    - 출판일 범위 검색
    - 검색 결과 스코어링 및 정렬
    - 요청 제한: 인증 사용자 60회/분, 비인증 사용자 30회/분
    """
    query = request.GET.get("q", "")
    field = request.GET.get("field", "all")  # 검색 필드 (title, author, all)
    pub_date_from = request.GET.get("pub_date_from", None)
    pub_date_to = request.GET.get("pub_date_to", None)

    # 기본 쿼리셋
    queryset = Book.objects.select_related("category").annotate(
        like_count=Count("liked_users", distinct=True),
        thread_count=Count("threads", distinct=True),
    )

    if query:
        # 검색어 전처리
        search_tokens = preprocess_search_query(query)
        
        if search_tokens:
            # 검색 쿼리 생성
            search_query = build_search_query(search_tokens, field)
            queryset = queryset.filter(search_query)
            
            # 검색 결과에 스코어 추가 및 정렬
            results = []
            for book in queryset:
                score = calculate_search_score(book, search_tokens)
                results.append({
                    'book': book,
                    'score': score
                })
            
            # 스코어 기준 정렬
            results.sort(key=lambda x: x['score'], reverse=True)
            
            # 정렬된 결과로 쿼리셋 재구성
            book_ids = [result['book'].id for result in results]
            queryset = Book.objects.filter(id__in=book_ids)

    # 출판일 범위 검색
    if pub_date_from:
        queryset = queryset.filter(pub_date__gte=pub_date_from)
    if pub_date_to:
        queryset = queryset.filter(pub_date__lte=pub_date_to)

    # 페이지네이션
    paginator = CustomPagination()
    page = paginator.paginate_queryset(queryset, request)

    # 시리얼라이저를 통한 응답 데이터 생성
    serializer = BookListSerializer(page, many=True)
    
    # 응답에 메타데이터 추가
    response_data = {
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data
    }
    
    if query and search_tokens:
        response_data['search_info'] = {
            'query': query,
            'tokens': search_tokens,
            'field': field
        }
    
    return Response(response_data)


@api_view(["GET"])
@throttle_classes([SuggestionUserThrottle, SuggestionAnonThrottle])
def search_suggestions(request):
    """
    검색어 자동완성 API
    - 제목, 저자 기반 추천
    - 시작 부분 매칭을 우선으로 하고, 중간 문자열 매칭도 포함
    - 최대 5개 결과 반환
    - 인기도 기반 정렬
    - 캐싱 적용 (5분)
    - 요청 제한: 인증 사용자 180회/분, 비인증 사용자 120회/분
    """
    query = request.GET.get("q", "").strip()
    if not query:
        return Response([])

    # 캐시 키 생성
    cache_key = f'search_suggestions:{query}'
    
    # 캐시된 결과 확인
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return Response(cached_result)

    # 단일 쿼리로 통합 (CASE를 사용하여 우선순위 지정)
    suggestions = Book.objects.annotate(
        popularity=Count('liked_users', distinct=True) + Count('threads', distinct=True),
        is_starts_with=Case(
            When(Q(title__istartswith=query) | Q(author__istartswith=query), then=1),
            default=0,
            output_field=IntegerField(),
        )
    ).filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    ).order_by(
        '-is_starts_with',  # 시작 매칭 우선
        '-popularity',      # 그 다음 인기도
    ).values(
        'title', 
        'author', 
        'popularity',
        'is_starts_with'
    ).distinct()[:10]  # 약간 여유있게 가져옴

    # 결과 가공
    result = []
    seen = set()

    for item in suggestions:
        if len(result) >= 5:
            break

        # 제목 처리
        if item['title'].lower().find(query.lower()) != -1 and item['title'] not in seen:
            result.append({
                'text': item['title'],
                'type': 'title',
                'popularity': item['popularity'],
                'match_type': 'starts_with' if item['is_starts_with'] else 'contains'
            })
            seen.add(item['title'])

        # 저자 처리
        if item['author'].lower().find(query.lower()) != -1 and item['author'] not in seen:
            result.append({
                'text': item['author'],
                'type': 'author',
                'popularity': item['popularity'],
                'match_type': 'starts_with' if item['is_starts_with'] else 'contains'
            })
            seen.add(item['author'])

    result = result[:5]
    
    # 결과 캐싱 (5분)
    cache.set(cache_key, result, 300)

    return Response(result)
