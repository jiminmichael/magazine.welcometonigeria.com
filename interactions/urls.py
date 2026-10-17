from django.urls import path
from .views import NewsletterSubscribeView, ContactSubmissionView

app_name = 'interactions'

urlpatterns = [
    path('newsletter/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('contact/', ContactSubmissionView.as_view(), name='contact-submit'),
]

