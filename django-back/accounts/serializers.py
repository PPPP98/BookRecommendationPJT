from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from books.models import Category, Book
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from dj_rest_auth.serializers import LoginSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    profile_image = serializers.ImageField(required=False)
    interested_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False
    )

    nickname = serializers.CharField(
        max_length=30,
        required=True,
        allow_blank=False,
        error_messages={
            'blank': '닉네임을 입력해주세요.',
            'max_length': '닉네임은 최대 30자까지 입력할 수 있습니다.'
        }
    )

    bio = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': '자기소개는 최대 500자까지 입력할 수 있습니다.'
        }
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['profile_image'] = self.validated_data.get('profile_image', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        data['bio'] = self.validated_data.get('bio', '')
        # interested_categories는 선택적 필드이므로 기본값을 빈 리스트로 설정
        data['interested_categories'] = self.validated_data.get('interested_categories', [])

        return data
    
    def custom_signup(self, request, user):
        user.profile_image = self.cleaned_data.get('profile_image')
        user.nickname = self.cleaned_data.get('nickname')
        user.bio = self.cleaned_data.get('bio')
        user.save()
        
        # interested_categories 처리
        categories = self.cleaned_data.get('interested_categories', [])
        if categories:
            user.interested_categories.set(categories)

    def validate_profile_image(self, image):
        if not image:
            return image
            
        # 파일 크기 검사 (3MB)
        if image.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError('이미지 크기는 3MB를 초과할 수 없습니다.')
            
        # 파일 확장자 검사
        ext = os.path.splitext(image.name)[1][1:].lower()
        if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError('지원하지 않는 이미지 형식입니다. (jpg, jpeg, png, gif만 가능)')
            
        return image

class UserSimpleSerializer(serializers.ModelSerializer):
    """팔로우/팔로워 목록에서 사용할 간단한 사용자 정보 시리얼라이저"""
    class Meta:
        model = User
        fields = ['id', 'nickname', 'profile_image']


class UserFollowToggleSerializer(serializers.ModelSerializer):
    """팔로우 토글 응답용 시리얼라이저"""
    is_following = serializers.SerializerMethodField()
    follower_count = serializers.IntegerField()
    following_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'is_following', 'follower_count', 'following_count']

    def get_is_following(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.followers.filter(id=user.id).exists()
        return False


class BookSimpleSerializer(serializers.ModelSerializer):
    """프로필에서 사용할 간단한 도서 정보 시리얼라이저"""
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover']


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 상세 정보 시리얼라이저"""
    follower_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    is_following = serializers.SerializerMethodField()
    interested_categories = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'nickname', 'profile_image', 'bio',
            'follower_count', 'following_count', 'is_following',
            'interested_categories'
        ]

    def get_is_following(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.followers.filter(id=user.id).exists()
        return False
        
    def get_interested_categories(self, obj):
        return [
            {'id': category.id, 'name': category.name}
            for category in obj.interested_categories.all()
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """사용자 프로필 수정 시리얼라이저"""
    interested_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ['nickname', 'profile_image', 'bio', 'interested_categories']
        
    def validate_profile_image(self, image):
        if not image:
            return image
            
        # 파일 크기 검사 (3MB)
        if image.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError('이미지 크기는 3MB를 초과할 수 없습니다.')
            
        # 파일 확장자 검사
        ext = os.path.splitext(image.name)[1][1:].lower()
        if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError('지원하지 않는 이미지 형식입니다. (jpg, jpeg, png, gif만 가능)')
            
        return image

    def validate_nickname(self, value):
        # 현재 사용자의 닉네임은 제외하고 중복 검사
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise ValidationError('이미 사용 중인 닉네임입니다.')
        return value


class UserFollowListSerializer(serializers.ModelSerializer):
    """팔로잉/팔로워 목록 조회용 시리얼라이저"""
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'nickname', 'profile_image', 'bio', 'is_following']
    
    def get_is_following(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated and user.id != obj.id:
            return user.following.filter(id=obj.id).exists()
        return False

class CustomLoginSerializer(LoginSerializer):
    email = None  # email 필드 제거
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """로그인 응답에 포함될 사용자 상세 정보 시리얼라이저"""
    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'profile_image', 'username')
        read_only_fields = ('email',)
