"""
Views for user authentication and profile management.
"""

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
import secrets

from .models import User, Profile
from .serializers import (
    UserSerializer, RegisterSerializer, ProfileSerializer,
    CustomTokenObtainPairSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, EmailVerificationSerializer,
    SocialLoginSerializer, TwoFactorSetupSerializer,
    TwoFactorVerifySerializer, TwoFactorDisableSerializer
)
from .permissions import IsOwnerOrAdmin


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate email verification token
        token = secrets.token_urlsafe(32)
        user.email_verification_token = token
        user.save()
        
        # Send verification email
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Registration successful. Please check your email to verify your account.'
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT login view with user data."""
    
    serializer_class = CustomTokenObtainPairSerializer


class EmailVerificationView(views.APIView):
    """Email verification endpoint."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            user = User.objects.get(email_verification_token=token)
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()
            
            return Response({
                'message': 'Email verified successfully.'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid verification token.'
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(views.APIView):
    """Request password reset endpoint."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Send reset email
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
            
            return Response({
                'message': 'Password reset email sent.'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Don't reveal if email exists
            return Response({
                'message': 'If the email exists, a reset link has been sent.'
            }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(views.APIView):
    """Confirm password reset endpoint."""
    
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Invalid reset link.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({
                'error': 'Invalid or expired reset link.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        return Response({
            'message': 'Password reset successful.'
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile."""
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    """Update extended profile information."""
    
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile


class UserListView(generics.ListAPIView):
    """List all users (admin only)."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class SocialLoginView(views.APIView):
    """Social login endpoint."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SocialLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        provider = serializer.validated_data['provider']
        access_token = serializer.validated_data['access_token']
        
        # Import the provider adapter based on the provider
        if provider == 'google':
            from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
            adapter = GoogleOAuth2Adapter(request)
        elif provider == 'github':
            from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
            adapter = GitHubOAuth2Adapter(request)
        elif provider == 'linkedin':
            from allauth.socialaccount.providers.linkedin.views import LinkedInOAuth2Adapter
            adapter = LinkedInOAuth2Adapter(request)
        elif provider == 'facebook':
            from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
            adapter = FacebookOAuth2Adapter(request)
        else:
            return Response(
                {'error': 'Unsupported provider'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a token object
        from allauth.socialaccount.providers.oauth2.client import OAuth2Token
        token = OAuth2Token(token=access_token)
        
        # Get the provider instance
        provider_instance = adapter.get_provider()
        
        # Create a fake request to pass to the provider
        from django.http import HttpRequest
        fake_request = HttpRequest()
        fake_request.method = 'GET'
        fake_request.META = request.META.copy()
        fake_request.session = request.session
        
        # Get user data from the provider
        try:
            # This is a simplified approach - in practice, allauth handles this via their internal flow
            # For API usage, we'll use the token to fetch user data
            if provider == 'google':
                import requests
                user_data_response = requests.get(
                    'https://www.googleapis.com/oauth2/v2/userinfo',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                user_data = user_data_response.json()
                
                email = user_data.get('email')
                first_name = user_data.get('given_name', '')
                last_name = user_data.get('family_name', '')
                username = user_data.get('email', '').split('@')[0]
                
            elif provider == 'github':
                import requests
                user_data_response = requests.get(
                    'https://api.github.com/user',
                    headers={'Authorization': f'token {access_token}'}
                )
                user_data = user_data_response.json()
                
                email = user_data.get('email') or ''
                username = user_data.get('login', '')
                first_name = user_data.get('name', '').split(' ')[0] if user_data.get('name') else username
                last_name = ' '.join(user_data.get('name', '').split(' ')[1:]) if user_data.get('name') and len(user_data.get('name', '').split(' ')) > 1 else ''
                
            elif provider == 'facebook':
                import requests
                user_data_response = requests.get(
                    f'https://graph.facebook.com/me?fields=email,first_name,last_name&access_token={access_token}'
                )
                user_data = user_data_response.json()
                
                email = user_data.get('email', '')
                first_name = user_data.get('first_name', '')
                last_name = user_data.get('last_name', '')
                username = user_data.get('id', email.split('@')[0] if email else 'fb_user')
                
            elif provider == 'linkedin':
                import requests
                user_data_response = requests.get(
                    'https://api.linkedin.com/v2/me',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                user_data = user_data_response.json()
                
                # LinkedIn requires additional email request
                email_response = requests.get(
                    'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                email_data = email_response.json()
                email = email_data.get('elements', [{}])[0].get('handle~', {}).get('emailAddress', '')
                
                first_name = user_data.get('localizedFirstName', '')
                last_name = user_data.get('localizedLastName', '')
                username = email.split('@')[0] if email else 'linkedin_user'
            
            # Try to find existing user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create new user
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_email_verified=True  # Social providers verify emails
                )
                
                # Create profile
                Profile.objects.get_or_create(user=user)
            
            # Generate JWT token for the user
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        
        except Exception as e:
            return Response(
                {'error': f'Error during social authentication: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class MagicLinkRequestView(views.APIView):
    """Request a magic link for passwordless login."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if user exists
            return Response(
                {'message': 'If the email exists, a magic link has been sent.'},
                status=status.HTTP_200_OK
            )
        
        # Generate magic link token
        import secrets
        token = secrets.token_urlsafe(32)
        user.email_verification_token = token
        user.save()
        
        # Send magic link via email
        magic_link = f"{settings.FRONTEND_URL}/auth/magic-login/{token}"
        send_mail(
            'Your Magic Login Link',
            f'Click the link to login: {magic_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        
        return Response(
            {'message': 'If the email exists, a magic link has been sent.'},
            status=status.HTTP_200_OK
        )


class MagicLinkLoginView(views.APIView):
    """Login with a magic link token."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email_verification_token=token)
            
            # Clear the token after successful login
            user.email_verification_token = None
            user.save()
            
            # Generate JWT token
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired magic link'},
                status=status.HTTP_400_BAD_REQUEST
            )


class OTPRequestView(views.APIView):
    """Request an OTP for passwordless login."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        
        if not email and not phone:
            return Response(
                {'error': 'Email or phone is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # In a real implementation, you would use a service like Twilio for SMS
        # For now, we'll just generate an OTP and store it temporarily
        import random
        otp = f"{random.randint(100000, 999999)}"
        
        # Store OTP in session or cache (in real app, use Redis or database)
        from django.utils import timezone
        from datetime import timedelta
        expires_at = timezone.now() + timedelta(minutes=10)  # OTP expires in 10 minutes
        request.session['otp'] = otp
        request.session['otp_attempts'] = 0
        request.session['otp_expires'] = expires_at.isoformat()
        
        if email:
            # Send OTP via email
            send_mail(
                'Your One-Time Password',
                f'Your OTP is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
        
        # In a real app, you would also send via SMS if phone number is provided
        
        return Response(
            {'message': 'OTP has been sent'},
            status=status.HTTP_200_OK
        )


class OTPVerifyView(views.APIView):
    """Verify an OTP for passwordless login."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')
        phone = request.data.get('phone')
        
        if not otp:
            return Response(
                {'error': 'OTP is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if OTP exists in session and hasn't expired
        session_otp = request.session.get('otp')
        otp_expires_str = request.session.get('otp_expires')
        
        if not session_otp or not otp_expires_str:
            return Response(
                {'error': 'Please request a new OTP'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        from datetime import datetime
        otp_expires = datetime.fromisoformat(otp_expires_str)
        
        if timezone.now() > otp_expires:
            # Clear expired OTP
            request.session.pop('otp', None)
            request.session.pop('otp_expires', None)
            request.session.pop('otp_attempts', None)
            
            return Response(
                {'error': 'OTP has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if session_otp != otp:
            # Increment attempts counter
            attempts = request.session.get('otp_attempts', 0) + 1
            request.session['otp_attempts'] = attempts
            
            if attempts >= 3:  # Max 3 attempts
                # Clear OTP after too many attempts
                request.session.pop('otp', None)
                request.session.pop('otp_expires', None)
                request.session.pop('otp_attempts', None)
                
                return Response(
                    {'error': 'Too many failed attempts. Please request a new OTP.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(
                {'error': 'Invalid OTP'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # OTP is valid, clear session data
        request.session.pop('otp', None)
        request.session.pop('otp_expires', None)
        request.session.pop('otp_attempts', None)
        
        # Find user by email or phone
        user = None
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
        
        # In a real implementation, you would also look up by phone number
        
        if not user:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate JWT token
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


class TwoFactorSetupView(views.APIView):
    """Setup 2FA for the user."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = TwoFactorSetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        phone_number = serializer.validated_data.get('phone_number')
        
        # Update phone number if provided
        if phone_number:
            user.phone_number = phone_number
            user.save()
        
        # Generate TOTP device for the user
        from two_factor.models import PhoneDevice
        from django_otp.plugins.otp_totp.models import TOTPDevice
        
        # Remove existing TOTP devices for this user
        TOTPDevice.objects.filter(user=user).delete()
        
        # Create new TOTP device
        totp_device = TOTPDevice.objects.create(
            user=user,
            name='default',
        )
        
        # For phone number, we'll use the PhoneDevice
        if phone_number:
            # Remove existing phone devices
            PhoneDevice.objects.filter(user=user).delete()
            
            # Create new phone device
            phone_device = PhoneDevice.objects.create(
                user=user,
                name='default_phone',
                number=phone_number,
                method='sms'  # Can also be 'call'
            )
        
        # Generate QR code for authenticator apps
        import base64
        from io import BytesIO
        import qrcode
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Generate the provisioning URI
        provisioning_uri = totp_device.config_url
        
        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for API response
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return Response({
            'qr_code': qr_code_base64,
            'provisioning_uri': provisioning_uri,
            'message': '2FA setup initiated. Scan the QR code with your authenticator app.'
        })


class TwoFactorVerifyView(views.APIView):
    """Verify 2FA token and enable 2FA for the user."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = TwoFactorVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        token = serializer.validated_data['token']
        phone_number = serializer.validated_data.get('phone_number')
        
        from django_otp import devices_for_user
        from django_otp.plugins.otp_totp.models import TOTPDevice
        
        # Get the user's TOTP device
        totp_device = TOTPDevice.objects.filter(user=user, name='default').first()
        
        if not totp_device:
            return Response(
                {'error': '2FA not properly set up'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the token
        if totp_device.verify_token(token):
            # Enable 2FA for the user
            user.is_2fa_enabled = True
            
            # If phone number is provided, update it
            if phone_number:
                user.phone_number = phone_number
                
            user.save()
            
            return Response({
                'message': '2FA enabled successfully',
                'is_2fa_enabled': True
            })
        else:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TwoFactorDisableView(views.APIView):
    """Disable 2FA for the user."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = TwoFactorDisableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        token = serializer.validated_data['token']
        
        from django_otp.plugins.otp_totp.models import TOTPDevice
        
        # Get the user's TOTP device
        totp_device = TOTPDevice.objects.filter(user=user, name='default').first()
        
        if not totp_device:
            return Response(
                {'error': '2FA not properly set up'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the token
        if totp_device.verify_token(token):
            # Disable 2FA for the user
            user.is_2fa_enabled = False
            user.save()
            
            # Remove TOTP devices
            TOTPDevice.objects.filter(user=user).delete()
            
            return Response({
                'message': '2FA disabled successfully',
                'is_2fa_enabled': False
            })
        else:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TwoFactorLoginView(TokenObtainPairView):
    """Login view that handles 2FA if enabled."""
    
    def post(self, request, *args, **kwargs):
        # First, try normal authentication
        response = super().post(request, *args, **kwargs)
        
        # If login was successful, check if 2FA is enabled
        if response.status_code == 200:
            email = request.data.get('email') or request.data.get('username')
            
            try:
                user = User.objects.get(email=email)
                
                if user.is_2fa_enabled:
                    # Remove regular tokens and return 2FA required response
                    response.data = {
                        'requires_2fa': True,
                        'user_id': str(user.id)
                    }
                    
                    # Generate a temporary token that will be used for 2FA verification
                    from rest_framework_simplejwt.tokens import AccessToken
                    from datetime import timedelta
                    temp_token = AccessToken.for_user(user)
                    temp_token.set_exp(lifetime=timedelta(minutes=5))  # Short-lived token for 2FA
                    temp_token['2fa_required'] = True
                    
                    response.data['temp_token'] = str(temp_token)
                    
                    return response
            except User.DoesNotExist:
                pass
        
        return response


class TwoFactorLoginVerifyView(views.APIView):
    """Verify 2FA token after initial login."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        temp_token = request.data.get('temp_token')
        
        if not token or not temp_token:
            return Response(
                {'error': 'Token and temp_token are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework_simplejwt.exceptions import TokenError
        
        try:
            # Decode the temporary token
            decoded_token = AccessToken(temp_token)
            
            if not decoded_token.get('2fa_required', False):
                return Response(
                    {'error': 'Invalid temporary token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_id = decoded_token.get('user_id')
            user = User.objects.get(id=user_id)
        except (TokenError, User.DoesNotExist):
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django_otp.plugins.otp_totp.models import TOTPDevice
        
        # Get the user's TOTP device
        totp_device = TOTPDevice.objects.filter(user=user, name='default').first()
        
        if not totp_device:
            return Response(
                {'error': '2FA not properly set up'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the token
        if totp_device.verify_token(token):
            # Generate proper JWT tokens
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                {'error': 'Invalid 2FA token'},
                status=status.HTTP_400_BAD_REQUEST
            )
