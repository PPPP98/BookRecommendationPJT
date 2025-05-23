from rest_framework import serializers
from .models import Book, Category
from threads.models import Thread

class ThreadSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'title']

class BookListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    like_count = serializers.IntegerField(read_only=True)
    thread_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'cover',
            'category_name',
            'like_count',
            'thread_count',
        ]

class BookDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    like_count = serializers.IntegerField(read_only=True)
    thread_count = serializers.IntegerField(read_only=True)
    threads = ThreadSimpleSerializer(source='thread_set', many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'isbn',
            'cover',
            'publisher',
            'pub_date',
            'author',
            'author_info',
            'author_photo',
            'customer_review_rank',
            'subTitle',
            'category_name',
            'like_count',
            'thread_count',
            'threads',
        ]