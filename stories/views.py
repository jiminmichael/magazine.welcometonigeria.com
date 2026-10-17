from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import State, Story, StoryImage, SavedStory
from .serializers import StateSerializer, StorySerializer, StorySubmissionSerializer


class StateListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        states = State.objects.all().order_by('order', 'name')
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Story.objects.filter(status='published').select_related('state', 'author').prefetch_related('images')

        # Filter by search term
        q = request.query_params.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(experience__icontains=q) |
                Q(preview__icontains=q) |
                Q(location__icontains=q) |
                Q(author_name__icontains=q) |
                Q(state__name__icontains=q)
            )

        # Filter by state
        state_param = request.query_params.get('state', '').strip()
        if state_param:
            if state_param.lower() == 'abuja':
                queryset = queryset.filter(Q(state__name__iexact='FCT Abuja') | Q(state__name__iexact='Abuja'))
            else:
                queryset = queryset.filter(
                    Q(state__name__iexact=state_param) | Q(state__slug__iexact=state_param)
                )

        # Filter by featured
        featured_param = request.query_params.get('featured')
        if featured_param is not None:
            if featured_param.lower() in ['true', '1']:
                queryset = queryset.filter(featured=True)

        # Filter by author
        author_param = request.query_params.get('author', '').strip()
        if author_param:
            queryset = queryset.filter(
                Q(author__username__iexact=author_param) |
                Q(author_name__iexact=author_param)
            )

        # Sorting
        sort_param = request.query_params.get('sort', 'newest').lower()
        if sort_param == 'popular':
            queryset = queryset.order_by('-popularity', '-published_date')
        elif sort_param == 'featured':
            queryset = queryset.filter(featured=True).order_by('-published_date')
        else:
            queryset = queryset.order_by('-published_date', '-travel_date', '-created_at')

        # Limit if requested
        limit = request.query_params.get('limit')
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]

        serializer = StorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoryDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, identifier):
        story = Story.objects.filter(legacy_id=identifier).first()
        if not story:
            story = Story.objects.filter(slug=identifier).first()
        if not story and identifier.isdigit():
            story = Story.objects.filter(pk=int(identifier)).first()
        return story

    def get(self, request, identifier):
        story = self.get_object(identifier)
        if not story:
            return Response({"error": "Story not found."}, status=status.HTTP_404_NOT_FOUND)

        if story.status != 'published':
            # Allow author or staff to see pending/archived
            is_author = request.user.is_authenticated and (story.author == request.user)
            is_staff = request.user.is_authenticated and request.user.is_staff
            if not (is_author or is_staff):
                return Response({
                    "error": "This story is currently pending review.",
                    "status": "Pending Review"
                }, status=status.HTTP_403_FORBIDDEN)

        # Increment popularity views count
        Story.objects.filter(pk=story.pk).update(popularity=F('popularity') + 1)
        story.refresh_from_db()

        serializer = StorySerializer(story, context={'request': request})
        data = serializer.data

        # Related stories from same state
        related = Story.objects.filter(
            status='published',
            state=story.state
        ).exclude(pk=story.pk)[:3]
        data['related'] = StorySerializer(related, many=True, context={'request': request}).data

        # Check if saved by current user
        if request.user.is_authenticated:
            data['is_saved'] = SavedStory.objects.filter(user=request.user, story=story).exists()
        else:
            data['is_saved'] = False

        return Response(data, status=status.HTTP_200_OK)


class StorySubmissionView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = StorySubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        state_name = data['state'].strip()
        state = State.objects.filter(name__iexact=state_name).first()
        if not state:
            if state_name.lower() in ['abuja', 'fct']:
                state = State.objects.filter(name__icontains='Abuja').first()
        if not state:
            # Fallback or create
            state, _ = State.objects.get_or_create(name=state_name)

        author_user = request.user if request.user.is_authenticated else None
        author_name = data.get('name', '').strip()
        if not author_name and author_user:
            author_name = author_user.get_display_name()
        if not author_name:
            author_name = "Community Traveller"

        author_email = data.get('email', '').strip()
        if not author_email and author_user:
            author_email = author_user.email

        story = Story.objects.create(
            title=data['title'].strip(),
            author=author_user,
            author_name=author_name,
            author_email=author_email,
            state=state,
            location=data['location'].strip(),
            travel_date=data['travel_date'],
            experience=data['experience'].strip(),
            preview=data['experience'].strip()[:220],
            tips=data.get('travel_tips', '').strip(),
            enjoyed=data.get('enjoyed', '').strip(),
            recommendation=data.get('recommend', 'Not specified'),
            status='pending',
        )

        # Handle uploaded images
        # Front-end may send photos under 'photos' or 'images' or individual files
        uploaded_files = request.FILES.getlist('photos') or request.FILES.getlist('images')
        for idx, file in enumerate(uploaded_files[:4]):  # Max 4 photos
            StoryImage.objects.create(
                story=story,
                image=file,
                order=idx + 1
            )

        return Response({
            "message": "Your story has been submitted successfully for review.",
            "id": story.identifier,
            "status": "Pending Review"
        }, status=status.HTTP_201_CREATED)


class StorySaveToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, identifier):
        story = Story.objects.filter(legacy_id=identifier).first()
        if not story:
            story = Story.objects.filter(slug=identifier).first()
        if not story and identifier.isdigit():
            story = Story.objects.filter(pk=int(identifier)).first()

        if not story:
            return Response({"error": "Story not found."}, status=status.HTTP_404_NOT_FOUND)

        saved_record = SavedStory.objects.filter(user=request.user, story=story).first()
        if saved_record:
            saved_record.delete()
            return Response({"saved": False, "message": "Story removed from saved stories."}, status=status.HTTP_200_OK)
        else:
            SavedStory.objects.create(user=request.user, story=story)
            return Response({"saved": True, "message": "Story saved to your reading list."}, status=status.HTTP_200_OK)


class UserStoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_stories = Story.objects.filter(author=user).select_related('state').prefetch_related('images')
        submitted = StorySerializer(user_stories, many=True, context={'request': request}).data
        pending = StorySerializer(user_stories.filter(status='pending'), many=True, context={'request': request}).data
        published = StorySerializer(user_stories.filter(status='published'), many=True, context={'request': request}).data

        saved_records = SavedStory.objects.filter(user=user).select_related('story__state').prefetch_related('story__images')
        saved_stories = [record.story for record in saved_records if record.story.status == 'published']
        saved = StorySerializer(saved_stories, many=True, context={'request': request}).data

        visited_states = list(user_stories.values_list('state__name', flat=True).distinct())

        return Response({
            "submitted": submitted,
            "pending": pending,
            "published": published,
            "saved": saved,
            "stats": {
                "submitted_count": len(submitted),
                "pending_count": len(pending),
                "published_count": len(published),
                "saved_count": len(saved),
                "states_count": len(visited_states),
                "states": visited_states,
            }
        }, status=status.HTTP_200_OK)
