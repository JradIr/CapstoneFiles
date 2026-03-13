from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users
from .serializers import UsersSerializer
from django.shortcuts import render

#def home(request):
#    return render(request, 'home.html')

# Helper to generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if check_password(password, user.password_hash):
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, 'user': UsersSerializer(user).data})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    user = request.user
    return Response({'message': f'Welcome {user.username}, this is your dashboard'})

@api_view(["POST"])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if Users.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = Users.objects.create(
        username=username,
        password_hash=make_password(password)
    )
    return Response({"message": "Account created successfully!"}, status=201)

"""
@api_view(["POST"])
def update_admin_password(request):
    username = request.data.get("username")
    new_password = request.data.get("new_password")

    try:
        admin = AdminAccounts.objects.get(username=username)
        admin.password_hash = make_password(new_password)
        admin.save()
        return Response({"message": "Password updated successfully!"})
    except AdminAccounts.DoesNotExist:
        return Response({"error": "Admin not found"}, status=404)
"""

