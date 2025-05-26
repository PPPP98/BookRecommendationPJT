from django.core.management.base import BaseCommand
from books.similarity_utils import build_faiss_index

class Command(BaseCommand):
    help = '도서 임베딩 벡터를 사용하여 FAISS 인덱스를 생성합니다.'

    def handle(self, *args, **options):
        self.stdout.write('FAISS 인덱스 생성 시작...')
        
        try:
            index, book_id_to_idx, idx_to_book_id = build_faiss_index()
            self.stdout.write(
                self.style.SUCCESS(
                    f'FAISS 인덱스 생성 완료: 총 {index.ntotal}개 도서 벡터'
                )
            )
        except ValueError as e:
            self.stdout.write(
                self.style.ERROR(f'오류: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'예기치 않은 오류 발생: {str(e)}')
            )
