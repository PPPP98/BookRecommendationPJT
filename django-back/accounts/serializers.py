from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserDetailsSerializer(RegisterSerializer):
    image = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['image'] = self.validated_data.get('image', '')
        return data
    
    def save(self, request):
        user = super().save(request)
        user.image = self.cleaned_data.get('image')
        user.save()
        return user