from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import UserRegistrationSerializer
from apps.authentication.services.otp_service import create_email_otp


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Register a new user and automatically send an email OTP
        for verification. The user remains inactive until the OTP
        is verified via the authentication endpoints.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Trigger OTP for registration flow
        create_email_otp(email=user.email, purpose="register")

        data = {
            "message": "Registration successful. Please verify the OTP sent to your email.",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "phone_number": user.phone_number,
            },
        }

        return Response(data, status=status.HTTP_201_CREATED)

