from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import RegisterSerializer
from django.contrib.auth.models import User


# -----------------------
# User Registration API
# -----------------------
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Create user but set inactive until admin approval
        user = serializer.save(is_active=False)
        return Response(
            {
                "user": serializer.data,
                "message": "User registered successfully. Wait for admin approval."
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------
# JWT Login API with active check
# -----------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Standard JWT validation
        data = super().validate(attrs)

        # Check if user is active (approved by admin)
        if not self.user.is_active:
            raise serializers.ValidationError(
                "Account not approved by admin yet."
            )

        # Optionally add user info to response
        data.update({
            "username": self.user.username,
            "email": self.user.email,
        })
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
