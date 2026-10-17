from django.urls import path
from .views import (
    StateListView,
    StoryListView,
    StoryDetailView,
    StorySubmissionView,
    StorySaveToggleView,
    UserStoriesView,
)

app_name = 'stories'

urlpatterns = [
    path('states/', StateListView.as_view(), name='states-list'),
    path('stories/', StoryListView.as_view(), name='stories-list'),
    path('stories/submit/', StorySubmissionView.as_view(), name='story-submit'),
    path('stories/user/', UserStoriesView.as_view(), name='user-stories'),
    path('stories/<str:identifier>/', StoryDetailView.as_view(), name='story-detail'),
    path('stories/<str:identifier>/save/', StorySaveToggleView.as_view(), name='story-save-toggle'),
]

