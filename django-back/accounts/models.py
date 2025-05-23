from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 추가 필드
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    def __str__(self):
        return self.username
