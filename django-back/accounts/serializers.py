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

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['profile_image'] = self.validated_data.get('profile_image', '')
        data['interested_categories'] = self.validated_data.get('interested_categories', [])
        return data
    
    def custom_signup(self, request, user):
        user.profile_image = self.cleaned_data.get('profile_image')
        user.save()
        
        # interested_categories 처리
        categories = self.cleaned_data.get('interested_categories', [])
        if categories:
            user.interested_categories.set(categories)