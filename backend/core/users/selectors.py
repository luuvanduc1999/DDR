from typing import Optional
from django.db.models import QuerySet
from .models import User

def get_user_by_id(user_id: int) -> Optional[User]:
    return User.objects.filter(id=user_id).first()

def get_user_by_username(username: str) -> Optional[User]:
    return User.objects.filter(username=username).first()

def get_user_by_email(email: str) -> Optional[User]:
    return User.objects.filter(email=email).first()

def get_all_users() -> QuerySet[User]:
    return User.objects.all()

def get_active_users() -> QuerySet[User]:
    return User.objects.filter(is_active=True)