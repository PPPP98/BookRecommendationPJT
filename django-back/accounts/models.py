from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    profile_image = models.CharField(max_length=200, blank=True)
    
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
    
    def __str__(self):
        return self.username
