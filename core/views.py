import os
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import Http404


PAGES = [
    'index',
    'about',
    'stories',
    'story',
    'states',
    'state',
    'share-story',
    'travel-tips',
    'contact',
    'signin',
    'signup',
    'forgot-password',
    'account',
    'profile',
    'privacy-policy',
    'terms',
]


@ensure_csrf_cookie
def render_page(request, page_name="index"):
    # Strip any trailing .html or slash
    clean_name = page_name.replace('.html', '').strip('/')
    if not clean_name:
        clean_name = "index"

    if clean_name not in PAGES:
        raise Http404("Page not found")

    template_file = f"{clean_name}.html"
    return render(request, template_file, {
        "page_name": clean_name,
    })
