import json
import numpy as np
from django.utils import timezone
from openai import OpenAI
from django.conf import settings

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=settings.OPEN_AI_KEY)

def get_embedding(text):
    """
    주어진 텍스트의 임베딩을 생성합니다.
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    # 임베딩 생성 성공 로그
    print(f"✅ 임베딩 생성 성공: {len(response.data[0].embedding)} 차원")
    return response.data[0].embedding

def create_user_metadata_text(user):
    """
    사용자의 메타데이터를 텍스트로 변환합니다.
    """
    from .models import User
    if not isinstance(user, User):
        print(f"Warning: Expected User instance, got {type(user)}")
        return ""
        
    metadata = []
    
    # 관심 카테고리 정보 추가
    categories = user.interested_categories.all()
    if categories:
        category_names = [cat.name for cat in categories]
        metadata.append(f"관심 있는 도서 카테고리: {', '.join(category_names)}")
    
    # 자기소개 정보 추가
    if user.bio:
        metadata.append(f"자기소개: {user.bio}")
    
    # 좋아요한 책 정보 추가
    liked_books = user.like_books.all()
    if liked_books:
        book_titles = [book.title for book in liked_books]
        metadata.append(f"좋아하는 책: {', '.join(book_titles)}")
        
        # 좋아요한 책들의 작가 정보 추가
        authors = set(book.author for book in liked_books)
        if authors:
            metadata.append(f"선호하는 작가: {', '.join(authors)}")
    
    return " ".join(metadata)

def update_user_embedding(user):
    """
    사용자의 메타데이터를 기반으로 임베딩 벡터를 생성/업데이트합니다.
    """
    # 메타데이터 텍스트 생성
    metadata_text = create_user_metadata_text(user)
    
    if metadata_text.strip():  # 메타데이터가 있는 경우만 임베딩 생성
        try:
            # OpenAI API를 사용하여 임베딩 생성
            embedding = get_embedding(metadata_text)
            
            # 임베딩 벡터와 업데이트 시간 저장
            user.embedding_vector = json.dumps(embedding)
            user.embedding_updated_at = timezone.now()
            user.save(update_fields=['embedding_vector', 'embedding_updated_at'])
            
            print(f"✅ 사용자 '{user.username}'의 임베딩 생성/업데이트 완료")
            return True
            
        except Exception as e:
            print(f"❌ 사용자 '{user.username}'의 임베딩 생성 중 오류 발생: {str(e)}")
            return False  # 실제 오류 발생 시에만 False 반환
    
    return False

def find_similar_books_for_user(user, top_k=5):
    """
    사용자의 임베딩 벡터와 유사한 책을 찾습니다.
    """
    from books.similarity_utils import load_faiss_index
    
    if not user.embedding_vector:
        return []
    
    try:
        # 사용자 임베딩 벡터 로드
        embedding = np.array(json.loads(user.embedding_vector), dtype=np.float32)
        embedding = embedding.reshape(1, -1)
        
        # FAISS 인덱스 로드
        index, book_id_to_idx, idx_to_book_id = load_faiss_index()
        
        # 유사한 책 검색
        distances, indices = index.search(embedding, top_k + len(user.like_books.all()))
        
        # 검색 결과 처리 (이미 좋아요한 책 제외)
        from books.models import Book
        liked_book_ids = set(user.like_books.values_list('id', flat=True))
        similar_books = []
        
        for i, idx in enumerate(indices[0]):
            book_id = idx_to_book_id[idx]
            if book_id not in liked_book_ids:
                book = Book.objects.get(id=book_id)
                book.similarity_score = float(1 / (1 + distances[0][i]))
                similar_books.append(book)
                
                if len(similar_books) >= top_k:
                    break
        
        return similar_books
    except Exception as e:
        print(f"사용자 기반 도서 추천 실패: {str(e)}")
        return []
