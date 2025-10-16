from typing import Dict, Any
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User

class UserService:
    @staticmethod
    def create_user(data: Dict[str, Any]) -> User:
        raw_password = data.pop('password', None)
        if not raw_password:
            raise ValueError('Password is required')
            
        user = User(**data)
        user.set_password(raw_password)  # Mã hóa password trước khi lưu
        user.save()
        
        return user

    @staticmethod
    def create_user_token(user: User) -> Token:
        token, _ = Token.objects.get_or_create(user=user)
        return token

    @staticmethod
    def authenticate_user(username: str, password: str) -> User:
        return authenticate(username=username, password=password)

    @staticmethod
    def change_user_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save()

    @staticmethod
    def update_user_profile(user: User, data: Dict[str, Any]) -> User:
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def delete_user_token(user: User) -> None:
        Token.objects.filter(user=user).delete()