from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from model_utils import FieldTracker

class User(AbstractUser):
    tracker = FieldTracker(fields=['bio', 'embedding_vector'])
    
    profile_image = models.ImageField(
        upload_to='users/images/',  # 이미지 저장 경로
        blank=True, 
        null=True
    )

    nickname = models.CharField(
        max_length=30, 
        unique=True, 
    )

    bio = models.TextField(
        blank=True, 
        null=True, 
        help_text='자기소개를 입력하세요.'
    )
    
    # ManyToMany relationships
    following = models.ManyToManyField(
        'self', 
        symmetrical=False,
        related_name='followers'
    )
    like_books = models.ManyToManyField(
        'books.Book',
        related_name='liked_users'
    )
    like_threads = models.ManyToManyField(
        'threads.Thread',
        related_name='liked_users'
    )
    interested_categories = models.ManyToManyField(
        'books.Category',
        related_name='interested_users'
    )
      # 사용자 임베딩 데이터
    embedding_vector = models.TextField(
        null=True,
        blank=True,
        help_text='사용자 메타데이터 기반 임베딩 벡터'
    )
    embedding_updated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='임베딩 벡터 최종 업데이트 시간'
    )

    def __str__(self):
        return self.username
