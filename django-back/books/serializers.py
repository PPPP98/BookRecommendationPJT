from rest_framework import serializers
from .models import Book, Category
from threads.models import Thread

class ThreadSimpleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Thread
        fields = ['id', 'title', 'created_at', 'user', 'like_count', 'comment_count']
    
    def get_user(self, obj):
        from threads.serializers import UserSimpleSerializer
        return UserSimpleSerializer(obj.user).data
    
    def get_like_count(self, obj):
        return obj.liked_users.count()
    
    def get_comment_count(self, obj):
        return obj.comments.count()

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

class BookSimilarSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    similarity_score = serializers.FloatField()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'cover',
            'category_name',
            'similarity_score',
        ]

class BookDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    like_count = serializers.IntegerField(read_only=True)
    thread_count = serializers.IntegerField(read_only=True)
    threads = ThreadSimpleSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    similar_books = serializers.SerializerMethodField()

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
            'is_liked',
            'similar_books'
        ]
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.like_books.filter(id=obj.id).exists()
        return False
        
    def get_similar_books(self, obj):
        from .similarity_utils import find_similar_books
        similar_books = find_similar_books(obj.id, top_k=3)
        serializer = BookSimilarSerializer(similar_books, many=True)
        return serializer.data
        return serializer.data