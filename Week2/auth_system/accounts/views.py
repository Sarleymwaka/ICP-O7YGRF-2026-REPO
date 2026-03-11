# accounts/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 1️⃣ Registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# 2️⃣ JWT Login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 3️⃣ Password Reset Request (number 6)
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:8000/api/auth/reset-confirm/{uid}/{token}/"
            send_mail(
                'Password Reset',
                f'Click here to reset your password: {reset_link}',
                'no-reply@example.com',
                [email],
            )
        return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

# 4️⃣ Password Reset Confirm
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get('password')
        password2 = request.data.get('password2')
        if not password or not password2:
            return Response({"error": "Both password fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        if password != password2:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid UID."}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)