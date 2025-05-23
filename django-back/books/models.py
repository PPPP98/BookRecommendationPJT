from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)  # 카테고리명

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Book(models.Model):
    title = models.CharField(max_length=200)  # 책 제목
    description = models.TextField()  # 책 설명
    isbn = models.CharField(max_length=50, unique=True)  # ISBN
    cover = models.URLField(max_length=500)  # 책 표지 이미지 URL
    publisher = models.CharField(max_length=100)  # 출판사
    pub_date = models.DateField()  # 출판일
    author = models.CharField(max_length=100)  # 저자
    author_info = models.TextField()  # 저자 소개
    author_photo = models.URLField(max_length=500)  # 저자 사진 URL
    customer_review_rank = models.IntegerField()  # 고객 평점
    subTitle = models.CharField(max_length=200, blank=True)  # 부제목
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="books"
    )  # 카테고리

    def __str__(self):
        return self.title
