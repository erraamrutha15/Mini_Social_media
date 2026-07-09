"""
URL configuration for the accounts application.

Maps URL patterns to their corresponding views for user registration,
login, profile management, user listing, and follow/unfollow actions.
"""

from django.urls import path

from . import views


urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),

    # Profile endpoints
    path(
        'profile/<str:username>/',
        views.ProfileView.as_view(),
        name='profile',
    ),

    # User listing endpoint
    path('users/', views.UserListView.as_view(), name='user-list'),

    # Follow/Unfollow endpoints
    path('follow/', views.FollowView.as_view(), name='follow'),
    path('unfollow/', views.UnfollowView.as_view(), name='unfollow'),
]
