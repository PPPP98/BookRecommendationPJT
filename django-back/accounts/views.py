from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(['GET'])
def check_username(request):
    """
    username 중복 체크
    GET /api/accounts/check-username/?username=검사할유저명
    """
    username = request.GET.get('username', '')
    if not username:
        return Response(
            {'error': 'Username is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = User.objects.filter(username=username).exists()
    return Response({'exists': exists})

@api_view(['GET'])
def check_email(request):
    """
    email 중복 체크
    GET /api/accounts/check-email/?email=검사할이메일
    """
    email = request.GET.get('email', '')
    if not email:
        return Response(
            {'error': 'Email is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = User.objects.filter(email=email).exists()
    return Response({'exists': exists})

@api_view(['GET'])
def check_nickname(request):
    """
    nickname 중복 체크
    GET /api/accounts/check-nickname/?nickname=검사할닉네임
    """
    nickname = request.GET.get('nickname', '')
    if not nickname:
        return Response(
            {'error': 'Nickname is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = User.objects.filter(nickname=nickname).exists()
    return Response({'exists': exists})