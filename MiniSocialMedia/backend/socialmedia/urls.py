"""
URL configuration for the Mini Social Media Platform project.

Routes API requests to the appropriate application URL configurations:
- /                → API welcome / root endpoint
- /admin/          → Django admin interface
- /api/accounts/   → Accounts app (registration, login, profiles, follow)
- /api/posts/      → Posts app (posts, comments, likes)
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """Root endpoint — returns a welcome message and available API routes."""
    return Response({
        'message': 'Welcome to MiniSocial API',
        'endpoints': {
            'register': '/api/accounts/register/',
            'login': '/api/accounts/login/',
            'users': '/api/accounts/users/',
            'profile': '/api/accounts/profile/<username>/',
            'follow': '/api/accounts/follow/',
            'unfollow': '/api/accounts/unfollow/',
            'posts': '/api/posts/',
            'post_detail': '/api/posts/<id>/',
            'comments': '/api/posts/<id>/comments/',
            'like': '/api/posts/<id>/like/',
            'unlike': '/api/posts/<id>/unlike/',
        }
    })


urlpatterns = [
    # API root / welcome page
    path('', api_root, name='api-root'),

    # Django admin interface
    path('admin/', admin.site.urls),

    # API endpoints for user accounts and authentication
    path('api/accounts/', include('accounts.urls')),

    # API endpoints for posts, comments, and likes
    path('api/posts/', include('posts.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

