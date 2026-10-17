from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    bio = models.TextField(blank=True, verbose_name="Bio / About")
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Profile Avatar"
    )
    avatar_url = models.URLField(
        blank=True,
        max_length=500,
        verbose_name="External Avatar URL",
        help_text="Used for initial seed travellers and third-party photos"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username or self.email.split('@')[0]

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        if self.avatar_url:
            return self.avatar_url
        return "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=180&q=80"
