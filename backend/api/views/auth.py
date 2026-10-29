import pyotp
import traceback
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core import signing
from django.db.models import Q
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.throttling import ScopedRateThrottle

from ..models import UserProfile
from ..serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        password = request.data.get('password', '')
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([ScopedRateThrottle])
def login_view(request):
    throttle_scope = 'auth'
    username = request.data.get('username')
    password = request.data.get('password')
    totp_code = request.data.get('totp_code')
    pre_auth_token = request.data.get('pre_auth_token')

    if pre_auth_token:
        try:
            data = signing.loads(pre_auth_token, salt='medlife-2fa-pre-auth', max_age=120)
            user_id = data.get('user_id')
            user = User.objects.get(pk=user_id)
        except (signing.BadSignature, signing.SignatureExpired, User.DoesNotExist):
            return Response({"error": "Session expired or invalid. Please sign in again."}, status=status.HTTP_400_BAD_REQUEST)

        profile = UserProfile.objects.filter(user=user).first()
        if not profile or not profile.is_2fa_enabled or not profile.totp_secret:
            return Response({"error": "2FA is not configured for this account."}, status=status.HTTP_400_BAD_REQUEST)

        if not totp_code:
            return Response({"error": "Authenticator code is required."}, status=status.HTTP_400_BAD_REQUEST)

        totp = pyotp.TOTP(profile.totp_secret)
        if not totp.verify(totp_code, valid_window=1):
            return Response({"error": "Invalid or expired authenticator code."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

        profile, _ = UserProfile.objects.get_or_create(user=user)

        if profile.is_2fa_enabled and profile.totp_secret:
            token = signing.dumps({'user_id': user.id}, salt='medlife-2fa-pre-auth')
            return Response({
                "requires_2fa": True,
                "pre_auth_token": token,
                "message": "Please enter the 6-digit code from your authenticator app."
            }, status=status.HTTP_200_OK)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token_str = str(refresh)

    response = Response({
        "message": "Login successful",
        "username": user.username
    }, status=status.HTTP_200_OK)

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        path='/'
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token_str,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        path='/'
    )

    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logs out the user by blacklisting their refresh token and clearing auth cookies (P2-02).
    """
    try:
        refresh_token = request.data.get('refresh_token') or request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
        response = Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')
        return response
    except (TokenError, Exception) as e:
        response = Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')
        return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_2fa_view(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    if profile.is_2fa_enabled:
        return Response({"error": "2FA is already enabled for this account."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not profile.totp_secret:
        profile.totp_secret = pyotp.random_base32()
        profile.save()
        
    totp_uri = pyotp.totp.TOTP(profile.totp_secret).provisioning_uri(
        name=user.email or user.username,
        issuer_name="MedLife AI"
    )
    
    return Response({
        "totp_uri": totp_uri,
        "message": "Scan this QR code with your authenticator app."
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_and_enable_2fa_view(request):
    user = request.user
    code = request.data.get('code') or request.data.get('totp_code')
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    if not profile.totp_secret:
        return Response({"error": "Setup not initialized."}, status=status.HTTP_400_BAD_REQUEST)
        
    totp = pyotp.TOTP(profile.totp_secret)
    if totp.verify(code, valid_window=1):
        profile.is_2fa_enabled = True
        profile.save()
        return Response({"message": "2FA successfully enabled!"}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

RESET_REQUEST_MESSAGE = "If an account with those details exists, a reset link has been sent to its email."

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([ScopedRateThrottle])
def forgot_password_view(request):
    throttle_scope = 'auth'
    identifier = (request.data.get('email') or request.data.get('username') or '').strip()
    if not identifier:
        return Response({"error": "Email or username is required."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(Q(email__iexact=identifier) | Q(username__iexact=identifier)).first()

    if not user or not user.email:
        return Response({"message": RESET_REQUEST_MESSAGE}, status=status.HTTP_200_OK)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"

    try:
        send_mail(
            subject="MedLife.ai Password Reset Request",
            message=(
                f"Hello {user.username},\n\n"
                f"Click the link below to reset your password for your MedLife.ai account:\n"
                f"{reset_link}\n\n"
                f"If you did not request this, please ignore this email."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:
        traceback.print_exc()
        return Response(
            {"error": "Could not send the email right now. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({"message": RESET_REQUEST_MESSAGE}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([ScopedRateThrottle])
def reset_password_confirm_view(request):
    throttle_scope = 'auth'
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    if not uidb64 or not token or not new_password:
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return Response({"error": "Invalid reset request."}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired reset link."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # P2-15: Django validates the new password server-side
        validate_password(new_password, user)
    except ValidationError as e:
        return Response({"error": " ".join(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response(
        {"message": "Password has been reset successfully. You can now sign in."},
        status=status.HTTP_200_OK
    )