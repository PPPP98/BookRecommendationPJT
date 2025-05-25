from django.db.models import Q, F, ExpressionWrapper, FloatField
import re

def preprocess_search_query(query):
    """
    검색어 전처리 함수
    - 특수문자 제거
    - 공백 정규화
    - 검색어 토큰화
    """
    # 특수문자 제거 및 공백 정규화 (한글, 영문, 숫자만 허용)
    query = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', query)
    query = ' '.join(query.split())
    
    # 검색어 토큰화 (2글자 이상만 유효한 토큰으로 처리)
    tokens = [token for token in query.split() if len(token) >= 2]
    
    return tokens

def build_search_query(tokens, field=None):
    """
    검색 쿼리 생성 함수
    - 필드별 가중치 적용
    - 정확한 일치, 부분 일치에 따른 가중치 차등 적용
    """
    queries = Q()
    weights = {
        'title': 3.0,
        'subTitle': 2.0,
        'author': 2.0,
        'description': 1.0,
        'publisher': 1.0
    }
    
    for token in tokens:
        if field == 'title':
            # 제목 검색
            queries |= (
                Q(title__iexact=token) |  # 정확한 일치
                Q(title__icontains=token) |  # 부분 일치
                Q(subTitle__icontains=token)  # 부제목 부분 일치
            )
        elif field == 'author':
            # 저자 검색
            queries |= (
                Q(author__iexact=token) |  # 정확한 일치
                Q(author__icontains=token) |  # 부분 일치
                Q(author_info__icontains=token)  # 저자 정보 부분 일치
            )
        else:
            # 통합 검색 (필드별 가중치 적용)
            queries |= (
                Q(title__iexact=token) |  # 제목 정확한 일치 (최고 가중치)
                Q(title__icontains=token) |  # 제목 부분 일치
                Q(subTitle__icontains=token) |  # 부제목 부분 일치
                Q(author__icontains=token) |  # 저자 부분 일치
                Q(description__icontains=token) |  # 설명 부분 일치
                Q(publisher__icontains=token)  # 출판사 부분 일치
            )
    
    return queries

from django.utils import timezone

def calculate_search_score(queryset, search_tokens):
    """
    검색 결과 스코어 계산 함수
    - 필드별 가중치 적용
    - 일치 정도에 따른 점수 계산
    - 인기도(좋아요, 스레드 수) 반영
    - 출판일 최신성 반영
    """
    # 기본 텍스트 매칭 점수
    base_score = 0
    for token in search_tokens:
        # 제목 정확 일치
        if token.lower() == queryset.title.lower():
            base_score += 3.0
        # 제목 부분 일치
        elif token.lower() in queryset.title.lower():
            base_score += 2.0
        # 저자 일치
        if token.lower() in queryset.author.lower():
            base_score += 2.0
        # 설명 일치
        if token.lower() in queryset.description.lower():
            base_score += 1.0
    
    # 인기도 점수 계산 (좋아요 수와 스레드 수 기반)
    popularity_weight = 0.3
    like_count = queryset.liked_users.count()
    thread_count = queryset.threads.count()
    popularity_score = (like_count * 0.7 + thread_count * 0.3) * popularity_weight
    
    # 최신성 점수 계산 (1년 이내: 만점, 5년 이상: 최저점)
    recency_weight = 0.2
    days_old = (timezone.now().date() - queryset.pub_date).days
    years_old = days_old / 365
    recency_score = max(0, 1 - (years_old / 5)) * recency_weight
    
    # 최종 점수 계산 (기본 점수 + 인기도 + 최신성)
    final_score = base_score + popularity_score + recency_score
            
    return final_score
