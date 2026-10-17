import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class State(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name="State Name")
    slug = models.SlugField(max_length=70, unique=True)
    code = models.CharField(max_length=5, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']
        verbose_name = "Nigerian State"
        verbose_name_plural = "Nigerian States"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Story(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )

    RECOMMEND_CHOICES = (
        ('Absolutely', 'Absolutely'),
        ('Yes, with a few notes', 'Yes, with a few notes'),
        ('Maybe', 'Maybe'),
        ('Not this time', 'Not this time'),
        ('Not specified', 'Not specified'),
    )

    title = models.CharField(max_length=255, verbose_name="Story Title")
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    legacy_id = models.CharField(max_length=100, blank=True, null=True, unique=True, db_index=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stories",
        verbose_name="Contributor Account"
    )
    author_name = models.CharField(max_length=150, verbose_name="Contributor Name")
    author_email = models.EmailField(blank=True, verbose_name="Contributor Email")
    author_photo_url = models.URLField(max_length=500, blank=True, verbose_name="Author Photo URL")

    state = models.ForeignKey(
        State,
        on_delete=models.PROTECT,
        related_name="stories",
        verbose_name="State"
    )
    location = models.CharField(max_length=150, verbose_name="City / Location")
    travel_date = models.DateField(verbose_name="Date of Travel")
    published_date = models.DateField(blank=True, null=True, verbose_name="Publication Date")

    preview = models.TextField(blank=True, verbose_name="Lead / Preview Text")
    experience = models.TextField(verbose_name="Full Experience & Narrative")
    tips = models.TextField(blank=True, verbose_name="Travel Tips")
    enjoyed = models.TextField(blank=True, verbose_name="What was enjoyed most")
    recommendation = models.CharField(
        max_length=50,
        default='Not specified',
        verbose_name="Recommendation"
    )

    featured = models.BooleanField(default=False, db_index=True, verbose_name="Featured Story")
    popularity = models.PositiveIntegerField(default=0, verbose_name="Popularity / Views")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,
        verbose_name="Editorial Status"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Travel Story"
        verbose_name_plural = "Travel Stories"

    def __str__(self):
        return f"{self.title} ({self.state.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or f"story-{uuid.uuid4().hex[:8]}"
            slug = base
            counter = 1
            while Story.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        if not self.preview and self.experience:
            self.preview = self.experience[:220].rsplit(' ', 1)[0] + '...'
        super().save(*args, **kwargs)

    @property
    def identifier(self):
        return self.legacy_id or self.slug or str(self.id)


class StoryImage(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="stories/%Y/%m/", blank=True, null=True)
    image_url = models.URLField(max_length=600, blank=True, help_text="Direct URL for sample or CDN photos")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Story Photograph"
        verbose_name_plural = "Story Photographs"

    def __str__(self):
        return f"Photo for {self.story.title} (#{self.order})"

    def get_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=82"


class SavedStory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_stories"
    )
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'story')
        verbose_name = "Saved Story"
        verbose_name_plural = "Saved Stories"

    def __str__(self):
        return f"{self.user} saved {self.story}"
