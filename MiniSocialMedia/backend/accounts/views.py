"""
Views for the accounts application.

Provides API endpoints for user registration, login, profile management,
user listing, and follow/unfollow functionality.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token

from .models import Profile, Follow
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer


class RegisterView(APIView):
    """
    API endpoint for user registration.

    POST /api/accounts/register/

    Creates a new user account, generates an authentication token,
    and returns the token along with user information.

    Request Body:
        - username (str): Unique username for the new account.
        - email (str): Email address for the new account.
        - password (str): Password for the new account.
        - first_name (str): User's first name.
        - last_name (str): User's last name.

    Response (201):
        - token (str): Authentication token for the new user.
        - user_id (int): The ID of the created user.
        - username (str): The username of the created user.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user registration."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create authentication token for the new user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user authentication.

    POST /api/accounts/login/

    Authenticates a user with username and password, returns an
    authentication token for subsequent API requests.

    Request Body:
        - username (str): The user's username.
        - password (str): The user's password.

    Response (200):
        - token (str): Authentication token.
        - user_id (int): The authenticated user's ID.
        - username (str): The authenticated user's username.

    Response (401):
        - detail (str): Error message for invalid credentials.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user login."""
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user with provided credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # Get or create an authentication token
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {'detail': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ProfileView(RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profiles.

    GET /api/accounts/profile/<username>/
        Returns the profile data for the specified user, including
        follower/following counts, follow status, and user's posts.

    PUT /api/accounts/profile/<username>/
        Updates the profile for the authenticated user (own profile only).
        Supports updating bio, first_name, and last_name.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'username'

    def get_object(self):
        """
        Retrieve the Profile instance for the given username.

        Uses the username URL parameter to look up the associated
        User and their Profile.

        Returns:
            Profile: The profile instance for the specified username.

        Raises:
            Http404: If no user with the given username exists.
        """
        username = self.kwargs.get('username')
        profile = get_object_or_404(Profile, user__username=username)
        return profile

    def update(self, request, *args, **kwargs):
        """
        Update the user's profile.

        Only allows users to update their own profile. Returns a 403
        error if a user attempts to modify another user's profile.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Updated profile data or permission error.
        """
        profile = self.get_object()

        # Ensure the requesting user can only edit their own profile
        if request.user != profile.user:
            return Response(
                {'detail': 'You can only edit your own profile.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    """
    API endpoint for listing all registered users.

    GET /api/accounts/users/

    Returns a list of all users with their basic information
    (id, username, email, first_name, last_name).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class FollowView(APIView):
    """
    API endpoint for following a user.

    POST /api/accounts/follow/

    Creates a follow relationship between the authenticated user
    and the specified target user. Prevents self-following.

    Request Body:
        - following_id (int): The ID of the user to follow.

    Response (201):
        - detail (str): Success message.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle follow action."""
        following_id = request.data.get('following_id')

        # Validate that the target user exists
        following_user = get_object_or_404(User, id=following_id)

        # Prevent users from following themselves
        if request.user == following_user:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create follow relationship (or ignore if already exists)
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=following_user,
        )

        if not created:
            return Response(
                {'detail': 'You are already following this user.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'detail': 'Followed successfully'},
            status=status.HTTP_201_CREATED,
        )


class UnfollowView(APIView):
    """
    API endpoint for unfollowing a user.

    POST /api/accounts/unfollow/

    Removes the follow relationship between the authenticated user
    and the specified target user.

    Request Body:
        - following_id (int): The ID of the user to unfollow.

    Response (200):
        - detail (str): Success message.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle unfollow action."""
        following_id = request.data.get('following_id')

        # Validate that the target user exists
        following_user = get_object_or_404(User, id=following_id)

        # Attempt to delete the follow relationship
        try:
            follow = Follow.objects.get(
                follower=request.user,
                following=following_user,
            )
            follow.delete()
            return Response(
                {'detail': 'Unfollowed successfully'},
                status=status.HTTP_200_OK,
            )
        except Follow.DoesNotExist:
            return Response(
                {'detail': 'You are not following this user.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
