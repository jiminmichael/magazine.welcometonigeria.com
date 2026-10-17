from rest_framework import serializers
from .models import State, Story, StoryImage, SavedStory


class StateSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ['id', 'name', 'code', 'slug', 'count']

    def get_count(self, obj):
        return obj.stories.filter(status='published').count()


class StorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='identifier', read_only=True)
    state = serializers.CharField(source='state.name', read_only=True)
    author = serializers.CharField(source='author_name', read_only=True)
    authorId = serializers.SerializerMethodField()
    authorPhoto = serializers.SerializerMethodField()
    date = serializers.DateField(source='travel_date', format='%Y-%m-%d', read_only=True)
    publishedDate = serializers.DateField(source='published_date', format='%Y-%m-%d', read_only=True)
    story = serializers.CharField(source='experience', read_only=True)
    images = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'state',
            'location',
            'author',
            'authorId',
            'authorPhoto',
            'date',
            'publishedDate',
            'preview',
            'story',
            'images',
            'tips',
            'enjoyed',
            'recommendation',
            'featured',
            'popularity',
            'status',
        ]

    def get_authorId(self, obj):
        if obj.author:
            return obj.author.username
        from django.utils.text import slugify
        return slugify(obj.author_name) or str(obj.id)

    def get_authorPhoto(self, obj):
        request = self.context.get('request')
        url = ""
        if obj.author:
            url = obj.author.get_avatar_url()
        elif obj.author_photo_url:
            url = obj.author_photo_url
        else:
            url = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=160&q=80"
        
        if request and url.startswith('/media/'):
            return request.build_absolute_uri(url)
        return url

    def get_images(self, obj):
        request = self.context.get('request')
        image_list = []
        for img in obj.images.all():
            img_url = img.get_url()
            if request and img_url.startswith('/media/'):
                img_url = request.build_absolute_uri(img_url)
            image_list.append(img_url)
        if not image_list:
            image_list.append("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=82")
        return image_list

    def get_status(self, obj):
        return 'Published' if obj.status == 'published' else 'Pending Review'


class StorySubmissionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    state = serializers.CharField(max_length=100, required=True)
    location = serializers.CharField(max_length=150, required=True)
    travel_date = serializers.DateField(required=True)
    title = serializers.CharField(max_length=255, required=True)
    experience = serializers.CharField(min_length=80, required=True)
    enjoyed = serializers.CharField(required=False, allow_blank=True, default='')
    recommend = serializers.CharField(required=False, allow_blank=True, default='Not specified')
    travel_tips = serializers.CharField(required=False, allow_blank=True, default='')

