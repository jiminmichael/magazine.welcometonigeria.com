from django.urls import path, re_path
from .views import render_page

app_name = 'core'

urlpatterns = [
    path('', render_page, {'page_name': 'index'}, name='home'),
    re_path(r'^(?P<page_name>[a-zA-Z0-9_-]+(?:\.html)?)/?$', render_page, name='page'),
]

