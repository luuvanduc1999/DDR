from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.db import transaction

from .models import User
from .selectors import get_all_users
from .services import UserService
from .permissions import IsOwnerOrAdmin, IsNotAuthenticated, IsSuperAdmin
from .serializers import (
    UserSerializer, LoginSerializer, 
    ChangePasswordSerializer, UserProfileUpdateSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_all_users()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsNotAuthenticated()]
        elif self.action == 'login':
            return [AllowAny()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        elif self.action in ['change_password', 'update_profile']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = UserService.create_user(serializer.validated_data)
        token = UserService.create_user_token(user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = UserService.authenticate_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user and user.is_active:
            login(request, user)
            token = UserService.create_user_token(user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff
            })
            
        return Response(
            {'error': 'Invalid credentials or account is disabled'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            UserService.delete_user_token(request.user)
            logout(request)
            return Response({'message': 'Successfully logged out'})
        return Response(
            {'error': 'Not logged in'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        self.check_object_permissions(request, user)
        
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Current password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully'})