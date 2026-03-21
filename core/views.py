from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .serializers import TenantSignupSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from core.models import Tenant
from rest_framework import status

User = get_user_model()


class TenantSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, tenant_slug):
        tenant = get_object_or_404(Tenant, slug=tenant_slug, is_active=True)

        serializer = TenantSignupSerializer(
            data=request.data,
            context={"tenant": tenant},
        )

        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    "message": "Signup successful",
                    "tenant": tenant.slug,
                    "user_id": user.id,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=201,
            )

        return Response(serializer.errors, status=400)



class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        errors = {}

        if not email:
            errors["email"] = ["Email is required"]

        if not password:
            errors["password"] = ["Password is required"]

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"errors": {"email": ["Invalid email"]}},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(password, user.password):
            return Response(
                {"errors": {"password": ["Invalid password"]}},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        refresh["tenant"] = user.tenant.slug
        refresh["role"] = user.role

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

#Tenan-aware base queryset mixin
class TenantQuerysetMixin:
    def get_queryset(self):
        return super().get_queryset().filter(
            tenant=self.request.user.tenant
        )
