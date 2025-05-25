from django.db.models import Q, F, ExpressionWrapper, FloatField
import re

def preprocess_search_query(query):
    """
    검색어 전처리 함수
    - 공백 정규화
    - 검색어 토큰화
    """
    # 공백 정규화
    query = ' '.join(query.split())
    
    # 검색어 토큰화 (1글자 이상 허용)
    tokens = [token for token in query.split()]
    
    return tokens

def build_search_query(tokens, field=None):
    """
    검색 쿼리 생성 함수
    - 필드별 검색
    - 정확한 일치를 우선 순위로 처리
    """
    queries = Q()
    
    if field == 'title':
        # 제목 검색 - 정확한 일치를 우선으로 함
        exact_title = ' '.join(tokens)
        queries = (
            Q(title__iexact=exact_title) |  # 완전 일치
            Q(title__istartswith=exact_title) |  # 시작 일치
            Q(title__icontains=exact_title)  # 부분 일치
        )
    elif field == 'author':
        # 저자 검색
        exact_author = ' '.join(tokens)
        queries = (
            Q(author__iexact=exact_author) |
            Q(author__istartswith=exact_author) |
            Q(author__icontains=exact_author)
        )
    else:
        # 통합 검색
        exact_query = ' '.join(tokens)
        queries = (
            Q(title__iexact=exact_query) |
            Q(title__istartswith=exact_query) |
            Q(title__icontains=exact_query) |
            Q(author__iexact=exact_query) |
            Q(author__icontains=exact_query) |
            Q(description__icontains=exact_query)
        )
    
    return queries

from django.utils import timezone

def calculate_search_score(book, search_tokens):
    """
    검색 결과 스코어 계산
    - 제목 완전 일치: 100점
    - 제목 시작 일치: 80점
    - 제목 부분 일치: 60점
    - 저자 일치: 40점
    - 설명 포함: 20점
    """
    score = 0
    query = ' '.join(search_tokens)
    
    # 제목 검사
    if book.title.lower() == query.lower():
        score += 100
    elif book.title.lower().startswith(query.lower()):
        score += 80
    elif query.lower() in book.title.lower():
        score += 60
    
    # 저자 검사
    if book.author.lower() == query.lower():
        score += 40
    elif query.lower() in book.author.lower():
        score += 30
    
    # 설명 검사
    if query.lower() in book.description.lower():
        score += 20
    
    return score
