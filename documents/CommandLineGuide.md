# 도서 추천 시스템 커맨드라인 가이드

## 1. 환경 설정

### 1.1 패키지 설치
```bash
# django-back 디렉토리로 이동
cd django-back

# 필요한 패키지 설치
pip install django-model-utils  # 모델 필드 변경 추적을 위한 패키지

# 현재 requirements.txt 업데이트
pip freeze > requirements.txt
```

## 2. 데이터베이스 마이그레이션

### 2.1 마이그레이션 생성
```bash
# django-back 디렉토리에서
python manage.py makemigrations accounts
```
결과: `accounts/migrations/0005_user_embedding_updated_at_user_embedding_vector.py` 생성

### 2.2 마이그레이션 적용
```bash
python manage.py migrate
```

## 3. 임베딩 관리 명령어

### 3.1 모든 도서의 임베딩 생성
```bash
# 전체 도서의 임베딩 생성
python manage.py create_book_embeddings

# 특정 개수만 처리 (예: 100개)
python manage.py create_book_embeddings --limit 100

# 기존 임베딩 강제 업데이트
python manage.py create_book_embeddings --force
```

### 3.2 FAISS 인덱스 관리
```bash
# FAISS 인덱스 재생성
python manage.py build_faiss_index

# 인덱스 강제 업데이트
python manage.py build_faiss_index --force
```

## 4. 개발 서버 실행
```bash
python manage.py runserver
```

## 5. API 테스트

### 5.1 도서 추천 API 테스트 (curl 사용)
```bash
# JWT 토큰으로 인증된 요청
curl -X GET \
  http://localhost:8000/api/accounts/recommended-books/ \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```

## 6. 트러블슈팅

### 6.1 임베딩 초기화
```bash
# 모든 사용자의 임베딩 초기화
python manage.py shell
```
```python
from accounts.models import User
User.objects.update(embedding_vector=None, embedding_updated_at=None)
```

### 6.2 FAISS 인덱스 초기화
```bash
# FAISS 데이터 디렉토리 삭제 후 재생성
rm -rf books/faiss_data/*
python manage.py build_faiss_index
```

## 7. 성능 모니터링

### 7.1 임베딩 상태 확인
```python
# Django 쉘에서
from accounts.models import User
from books.models import Book

# 사용자 임베딩 통계
print(f"전체 사용자: {User.objects.count()}")
print(f"임베딩 있는 사용자: {User.objects.exclude(embedding_vector__isnull=True).count()}")

# 도서 임베딩 통계
print(f"전체 도서: {Book.objects.count()}")
print(f"임베딩 있는 도서: {Book.objects.exclude(embedding_vector__isnull=True).count()}")
```

## 주의사항
1. 마이그레이션 전에 항상 데이터베이스 백업
2. 대량의 임베딩 생성 시 API 호출 제한 고려
3. FAISS 인덱스 재생성 시 서비스 중단 가능성 고려
