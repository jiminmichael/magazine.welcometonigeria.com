from django.contrib import admin
from django.utils import timezone
from .models import State, Story, StoryImage, SavedStory


class StoryImageInline(admin.TabularInline):
    model = StoryImage
    extra = 1
    fields = ('image', 'image_url', 'caption', 'order')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'slug', 'stories_count')
    search_fields = ('name', 'code')
    prepopulated_fields = {'slug': ('name',)}

    def stories_count(self, obj):
        return obj.stories.filter(status='published').count()
    stories_count.short_description = 'Published Stories'


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'state',
        'location',
        'author_name',
        'status',
        'featured',
        'published_date',
        'created_at',
    )
    list_filter = ('status', 'featured', 'state', 'published_date')
    search_fields = ('title', 'location', 'author_name', 'author_email', 'experience')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [StoryImageInline]
    actions = ['approve_and_publish', 'feature_stories', 'unfeature_stories']

    @admin.action(description="Approve and Publish selected stories")
    def approve_and_publish(self, request, queryset):
        updated = queryset.update(
            status='published',
            published_date=timezone.now().date()
        )
        self.message_user(request, f"{updated} story/stories successfully marked as Published.")

    @admin.action(description="Mark selected stories as Featured")
    def feature_stories(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"{updated} story/stories marked as Featured.")

    @admin.action(description="Remove Featured flag from selected stories")
    def unfeature_stories(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f"{updated} story/stories unfeatured.")


@admin.register(SavedStory)
class SavedStoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'story__title')
