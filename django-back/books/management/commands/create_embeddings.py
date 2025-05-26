from django.core.management.base import BaseCommand
from books.embedding_utils import batch_create_embeddings

class Command(BaseCommand):
    help = '도서 메타데이터 임베딩 생성'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='처리할 최대 도서 수',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='기존 임베딩 무시하고 전체 재생성',
        )

    def handle(self, *args, **options):
        limit = options.get('limit')
        force_update = options.get('force', False)
        
        self.stdout.write(self.style.SUCCESS('도서 임베딩 생성 시작...'))
        
        if limit:
            self.stdout.write(f'최대 {limit}개 도서 처리')
        
        if force_update:
            self.stdout.write('모든 도서 임베딩 재생성')
        else:
            self.stdout.write('임베딩이 없는 도서만 처리')
        
        result = batch_create_embeddings(limit=limit, force_update=force_update)
        
        self.stdout.write(self.style.SUCCESS(
            f'임베딩 생성 완료: 총 {result["total"]}개 중 '
            f'{result["success"]}개 성공, {result["failed"]}개 실패'
        ))
