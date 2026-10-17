from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import NewsletterSubscription, ContactMessage


class NewsletterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=255, required=True)
    message = serializers.CharField(required=True)


class NewsletterSubscribeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NewsletterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Please provide a valid email address."}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email'].strip().lower()
        sub, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )
        if not created and not sub.is_active:
            sub.is_active = True
            sub.save()

        return Response({
            "message": "Thanks for subscribing! You'll receive real travel stories and updates from across Nigeria."
        }, status=status.HTTP_200_OK)


class ContactSubmissionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        contact_msg = ContactMessage.objects.create(
            name=data['name'].strip(),
            email=data['email'].strip().lower(),
            subject=data['subject'].strip(),
            message=data['message'].strip(),
        )

        # Notify admin via email (as configured in settings)
        try:
            send_mail(
                subject=f"[WTN Magazine Contact] {contact_msg.subject}",
                message=f"New message from {contact_msg.name} ({contact_msg.email}):\n\n{contact_msg.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        return Response({
            "message": "Thank you for reaching out! We have received your message and will get back to you shortly."
        }, status=status.HTTP_201_CREATED)
