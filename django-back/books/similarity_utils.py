import json
import numpy as np
import faiss
import os
import pickle
from django.conf import settings
from .models import Book

# FAISS 인덱스 및 매핑 파일 저장 경로
FAISS_DATA_DIR = os.path.join(settings.BASE_DIR, 'books', 'faiss_data')
FAISS_INDEX_PATH = os.path.join(FAISS_DATA_DIR, 'book_index')
BOOK_ID_MAP_PATH = os.path.join(FAISS_DATA_DIR, 'book_id_map.pkl')

# 디렉토리가 없으면 생성
os.makedirs(FAISS_DATA_DIR, exist_ok=True)

def load_book_vectors():
    """
    모든 책의 임베딩 벡터를 로드합니다.
    """
    # 임베딩이 있는 모든 책 조회
    books = Book.objects.exclude(embedding_vector__isnull=True)
    
    # 책 ID와 인덱스 매핑을 위한 딕셔너리
    book_id_to_idx = {}
    idx_to_book_id = {}
    
    vectors = []
    for idx, book in enumerate(books):
        try:
            # JSON 문자열에서 벡터 로드
            vector = json.loads(book.embedding_vector)
            vectors.append(vector)
            
            # 책 ID와 인덱스 매핑 저장
            book_id_to_idx[book.id] = idx
            idx_to_book_id[idx] = book.id
        except Exception as e:
            print(f"책 '{book.title}' (ID: {book.id})의 벡터 로드 실패: {str(e)}")
            continue
    
    if not vectors:
        raise ValueError("로드할 임베딩 벡터가 없습니다.")
    
    # 벡터 배열 생성
    vectors = np.array(vectors, dtype=np.float32)
    
    return vectors, book_id_to_idx, idx_to_book_id

def build_faiss_index(vectors=None, book_id_to_idx=None, idx_to_book_id=None):
    """
    FAISS 인덱스를 생성하고 저장합니다.
    """
    if vectors is None or book_id_to_idx is None or idx_to_book_id is None:
        vectors, book_id_to_idx, idx_to_book_id = load_book_vectors()
    
    # 벡터 차원 확인 (OpenAI text-embedding-3-small 모델은 1536차원)
    dimension = vectors.shape[1]
    
    # L2 거리를 사용하는 기본 인덱스 생성
    index = faiss.IndexFlatL2(dimension)
    
    # 벡터 추가
    index.add(vectors)
    
    # 인덱스 및 ID 매핑 저장
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(BOOK_ID_MAP_PATH, 'wb') as f:
        pickle.dump({
            'book_id_to_idx': book_id_to_idx,
            'idx_to_book_id': idx_to_book_id
        }, f)
    
    print(f"FAISS 인덱스 생성 완료 (총 {index.ntotal}개 벡터)")
    return index, book_id_to_idx, idx_to_book_id

def load_faiss_index():
    """
    저장된 FAISS 인덱스를 로드합니다.
    """
    try:
        # 인덱스 파일이 없으면 새로 생성
        if not (os.path.exists(FAISS_INDEX_PATH) and os.path.exists(BOOK_ID_MAP_PATH)):
            return build_faiss_index()
        
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(BOOK_ID_MAP_PATH, 'rb') as f:
            id_maps = pickle.load(f)
        
        return index, id_maps['book_id_to_idx'], id_maps['idx_to_book_id']
    except Exception as e:
        print(f"FAISS 인덱스 로드 실패: {str(e)}")
        return build_faiss_index()

def find_similar_books(book_id, top_k=3):
    """
    특정 책과 가장 유사한 top_k개의 책을 찾아서 Book 객체와 유사도 점수를 함께 반환합니다.
    """
    try:
        # FAISS 인덱스 로드
        index, book_id_to_idx, idx_to_book_id = load_faiss_index()
        
        # 검색할 책 찾기
        book = Book.objects.get(id=book_id)
        book_idx = book_id_to_idx.get(book_id)
        
        if book_idx is None:
            raise ValueError(f"책 ID {book_id}의 임베딩을 찾을 수 없습니다.")
        
        # 쿼리 벡터 준비
        query_vector = np.array(json.loads(book.embedding_vector), dtype=np.float32)
        query_vector = query_vector.reshape(1, -1)  # 2D 배열로 변환
        
        # 유사 책 검색 (자기 자신 포함됨)
        distances, indices = index.search(query_vector, top_k + 1)
        
        # 결과 처리 (자기 자신 제외)
        similar_book_ids = []
        similarity_scores = {}
        
        for i, idx in enumerate(indices[0]):
            result_book_id = idx_to_book_id[idx]
            if result_book_id != book_id:  # 자기 자신 제외
                similar_book_ids.append(result_book_id)
                similarity_scores[result_book_id] = float(1 / (1 + distances[0][i]))  # 유사도 점수 (0~1)
                
            if len(similar_book_ids) >= top_k:
                break
        
        # Book 객체들을 한 번에 조회
        similar_books = []
        if similar_book_ids:
            books = Book.objects.filter(id__in=similar_book_ids)
            # 조회된 Book 객체에 유사도 점수 추가
            for book in books:
                book.similarity_score = similarity_scores[book.id]
                similar_books.append(book)
            # 유사도 점수로 정렬
            similar_books.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return similar_books
    except Exception as e:
        print(f"유사 도서 검색 실패: {str(e)}")
        return []
