from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        help_text='Required. Must be at least 8 characters long'
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone_number', 
                 'address', 'first_name', 'last_name', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_password(self, value):
        """
        Validate password strength
        """
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one digit.'
            )
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one uppercase letter.'
            )
        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one lowercase letter.'
            )
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text='Required. Must be at least 8 characters long'
    )

    def validate_new_password(self, value):
        """
        Validate new password strength
        """
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one digit.'
            )
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one uppercase letter.'
            )
        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one lowercase letter.'
            )
        return value

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'address')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False}
        }