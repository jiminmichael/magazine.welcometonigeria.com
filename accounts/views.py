import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import User
from .serializers import UserSerializer, SignupSerializer, SigninSerializer, ProfileUpdateSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        email = data['email']
        name_parts = data['name'].strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(parts := name_parts) > 1 else ''

        # Generate a clean unique username from email or name
        base_username = slugify(data['name']) or email.split('@')[0]
        base_username = re.sub(r'[^a-zA-Z0-9_-]', '', base_username)[:30] or 'traveller'
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=data['password'],
            first_name=first_name,
            last_name=last_name,
            bio=data.get('bio', ''),
        )

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            user.save()

        # Log user in
        login(request, user)

        return Response({
            "message": "Account created successfully.",
            "user": UserSerializer(user, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)


class SigninView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email'].strip().lower()
        password = serializer.validated_data['password']
        remember = serializer.validated_data.get('remember', False)

        user = authenticate(request, username=email, password=password)
        if user is None:
            user = authenticate(request, email=email, password=password)
        if user is None:
            try:
                target_user = User.objects.get(email__iexact=email)
                if target_user.check_password(password):
                    user = target_user
            except User.DoesNotExist:
                user = None

        if user is None:
            return Response({
                "error": "Invalid email address or password. Please verify your details."
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({
                "error": "This account is inactive. Please contact support."
            }, status=status.HTTP_403_FORBIDDEN)

        login(request, user)

        if not remember:
            request.session.set_expiry(0)  # Session expires when browser closes
        else:
            request.session.set_expiry(1209600)  # 2 weeks

        return Response({
            "message": "Signed in successfully.",
            "user": UserSerializer(user, context={'request': request}).data
        }, status=status.HTTP_200_OK)


class SignoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Signed out successfully."}, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({
                "authenticated": False,
                "user": None
            }, status=status.HTTP_200_OK)

        return Response({
            "authenticated": True,
            "user": UserSerializer(request.user, context={'request': request}).data
        }, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def patch(self, request):
        serializer = ProfileUpdateSerializer(
            instance=request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        updated_user = serializer.save()
        return Response({
            "message": "Profile updated successfully.",
            "user": UserSerializer(updated_user, context={'request': request}).data
        }, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        if not email:
            return Response({"error": "Please provide an email address."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email__iexact=email)
            token = default_token_generator.make_token(user)
            # In a full deployment, send email with reset link:
            # reset_link = request.build_absolute_uri(f"/reset-password/?uid={user.pk}&token={token}")
            send_mail(
                subject="Password Reset - Welcome to Nigeria Travel Magazine",
                message=f"Hello {user.get_display_name()},\n\nWe received a request to reset your password. Use token: {token} to reset your password.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass  # Do not disclose if user exists

        return Response({
            "message": "If an account matches that email address, password reset instructions have been sent."
        }, status=status.HTTP_200_OK)


class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, identifier):
        # identifier can be username, user id, or slugified name
        user = None
        if identifier.isdigit():
            user = User.objects.filter(pk=int(identifier)).first()
        if not user:
            user = User.objects.filter(username__iexact=identifier).first()
        if not user:
            # Check by first_name / last_name slug or email prefix
            for u in User.objects.all():
                if slugify(u.get_display_name()) == slugify(identifier):
                    user = u
                    break

        if not user:
            return Response({"error": "Traveller profile not found."}, status=status.HTTP_404_NOT_FOUND)

        published_stories = user.stories.filter(status='published')
        states_shared = list(published_stories.values_list('state__name', flat=True).distinct())

        return Response({
            "id": user.id,
            "username": user.username,
            "name": user.get_display_name(),
            "photo": user.get_avatar_url(),
            "bio": user.bio or "A traveller sharing personal experiences from across Nigeria.",
            "stats": {
                "published_count": published_stories.count(),
                "states_count": len(states_shared),
                "states": states_shared
            }
        }, status=status.HTTP_200_OK)
