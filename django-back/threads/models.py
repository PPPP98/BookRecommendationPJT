from django.db import models
from django.utils import timezone
from django.conf import settings

class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='threads')

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.thread.title}"

