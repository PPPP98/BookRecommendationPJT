import json
import numpy as np
import time
from openai import OpenAI
from django.conf import settings
from django.utils import timezone
from .models import Book

def create_book_embedding(book):
    client = OpenAI(api_key=settings.OPEN_AI_KEY)
    """
    책 정보를 기반으로 OpenAI 임베딩 생성
    가장 저렴한 모델인 text-embedding-3-small 사용
    """
    # 임베딩을 위한 텍스트 준비
    text_to_embed = f"""
    제목: {book.title}
    부제: {book.subTitle if book.subTitle else ''}
    저자: {book.author}
    출판사: {book.publisher}
    카테고리: {book.category.name}
    설명: {book.description}
    저자 정보: {book.author_info}
    """
    
    try:
        # OpenAI API 호출
        response = client.embeddings.create(
            input=text_to_embed,
            model="text-embedding-3-small"  # 가장 저렴한 임베딩 모델
        )
        
        # 임베딩 결과 저장
        embedding_vector = response.data[0].embedding
        
        # 임베딩 벡터를 JSON 문자열로 저장
        book.embedding_vector = json.dumps(embedding_vector)
        book.embedding_updated_at = timezone.now()
        book.save(update_fields=['embedding_vector', 'embedding_updated_at'])
        
        print(f"✅ 성공: 책 '{book.title}'의 임베딩 생성 완료 ({len(embedding_vector)} 차원)")
        return True
    except Exception as e:
        print(f"❌ 오류: 책 '{book.title}' (ID: {book.id})의 임베딩 생성 실패: {str(e)}")
        return False

def batch_create_embeddings(limit=None, force_update=False):
    """
    여러 책의 임베딩을 일괄 생성
    limit: 처리할 최대 책 수 (None이면 전체)
    force_update: True면 기존 임베딩이 있어도 재생성
    """
    # 임베딩이 없거나 업데이트가 필요한 책 조회
    if force_update:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(embedding_vector__isnull=True)
    
    if limit:
        books = books[:limit]
    
    total = books.count()
    success = 0
    failed = 0
    
    print(f"📚 총 {total}개 도서의 임베딩 생성 시작...")
    
    for i, book in enumerate(books):
        print(f"🔄 처리 중 ({i+1}/{total}): {book.title}")
        
        # API 호출 제한을 위한 지연 (분당 60-100회 호출 제한 고려)
        if i > 0 and i % 10 == 0:
            print("⏳ API 속도 제한 방지: 2초 대기...")
            time.sleep(2)
        
        result = create_book_embedding(book)
        if result:
            success += 1
        else:
            failed += 1
    
    print(f"📊 처리 결과: 총 {total}개 중 {success}개 성공, {failed}개 실패")
    
    return {
        "total": total,
        "success": success,
        "failed": failed
    }

def get_embedding(text):
    client = OpenAI(api_key=settings.OPEN_AI_KEY)
    """
    주어진 텍스트의 임베딩을 생성합니다.
    """
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"임베딩 생성 실패: {str(e)}")
        raise
