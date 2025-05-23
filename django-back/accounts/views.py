# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import get_user_model
# from .serializers import UserSerializer

# User = get_user_model()

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_user(request):
#     user = request.user
#     user.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_detail(request):
#     serializer = UserSerializer(request.user)
#     return Response(serializer.data)
