"""
DRF Serializers for User and Profile models.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    class Meta:
        model = Profile
        fields = [
            'avatar', 'bio', 'skills', 'website', 'linkedin', 
            'github', 'twitter', 'location', 'date_of_birth'
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model."""
    
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'is_email_verified', 'is_2fa_enabled', 'phone_number', 
            'is_phone_verified', 'profile', 'created_at'
        ]
        read_only_fields = ['id', 'is_email_verified', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='student')
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'role'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'student')
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with user data."""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        data['user'] = UserSerializer(self.user).data
        
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request."""
    
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""
    
    token = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for email verification."""
    
    token = serializers.CharField()


class SocialLoginSerializer(serializers.Serializer):
    """Serializer for social login."""
    
    provider = serializers.CharField()
    access_token = serializers.CharField()
    
    def validate_provider(self, value):
        valid_providers = ['google', 'github', 'linkedin', 'facebook']
        if value not in valid_providers:
            raise serializers.ValidationError(f'Provider must be one of: {", ".join(valid_providers)}')
        return value


class TwoFactorSetupSerializer(serializers.Serializer):
    """Serializer for 2FA setup."""
    
    phone_number = serializers.CharField(max_length=20, required=False)
    
    def validate_phone_number(self, value):
        # Basic phone number validation
        import re
        if value and not re.match(r'^\+?[1-9]\d{1,14}$', value.replace('-', '').replace(' ', '')):
            raise serializers.ValidationError('Invalid phone number format')
        return value


class TwoFactorVerifySerializer(serializers.Serializer):
    """Serializer for 2FA verification."""
    
    token = serializers.CharField(max_length=6)
    phone_number = serializers.CharField(max_length=20, required=False)
    
    def validate_token(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError('Token must be a 6-digit number')
        return value
    
    def validate_phone_number(self, value):
        import re
        if value and not re.match(r'^\+?[1-9]\d{1,14}$', value.replace('-', '').replace(' ', '')):
            raise serializers.ValidationError('Invalid phone number format')
        return value


class TwoFactorDisableSerializer(serializers.Serializer):
    """Serializer for disabling 2FA."""
    
    token = serializers.CharField(max_length=6)
    
    def validate_token(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError('Token must be a 6-digit number')
        return value

