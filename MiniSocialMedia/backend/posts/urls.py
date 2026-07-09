"""
URL configuration for the posts application.

Maps URL patterns to their corresponding views for post management,
commenting, and like/unlike actions.
"""

from django.urls import path

from . import views


urlpatterns = [
    # Post list and create endpoint
    path('', views.PostListCreateView.as_view(), name='post-list-create'),

    # Post delete endpoint (by primary key)
    path('<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comment create and list endpoint (by post primary key)
    path(
        '<int:pk>/comments/',
        views.CommentCreateView.as_view(),
        name='comment-create',
    ),

    # Like endpoint (by post primary key)
    path('<int:pk>/like/', views.LikeView.as_view(), name='post-like'),

    # Unlike endpoint (by post primary key)
    path('<int:pk>/unlike/', views.UnlikeView.as_view(), name='post-unlike'),
]
