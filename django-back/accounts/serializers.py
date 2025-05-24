from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from books.models import Category

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
