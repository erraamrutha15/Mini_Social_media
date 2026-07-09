"""
Views for the posts application.

Provides API endpoints for creating, listing, and deleting posts,
as well as commenting on posts and liking/unliking posts.
"""

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer


class PostListCreateView(ListCreateAPIView):
    """
    API endpoint for listing all posts and creating new posts.

    GET /api/posts/
        Returns a list of all posts ordered by creation date (newest first).
        Each post includes author info, content, like/comment counts,
        whether the current user has liked it, and nested comments.
        Permission: AllowAny

    POST /api/posts/
        Creates a new post with the authenticated user as the author.
        Permission: IsAuthenticated

    Request Body (POST):
        - content (str): The text content of the post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        """
        Return appropriate permissions based on the request method.

        - GET (list): Allow any user (including unauthenticated).
        - POST (create): Require authentication.

        Returns:
            list: Permission instances for the current request.
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        """
        Set the post author to the currently authenticated user.

        Args:
            serializer: The validated PostSerializer instance.
        """
        serializer.save(author=self.request.user)


class PostDeleteView(DestroyAPIView):
    """
    API endpoint for deleting a post.

    DELETE /api/posts/<id>/

    Only allows users to delete their own posts. Returns 404 if the
    post doesn't exist or doesn't belong to the authenticated user.

    Permission: IsAuthenticated
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only posts authored by the requesting user.

        This ensures users can only delete their own posts.
        A 404 is returned if they try to delete someone else's post.

        Returns:
            QuerySet: Posts filtered to the authenticated user.
        """
        return Post.objects.filter(author=self.request.user)


class CommentCreateView(APIView):
    """
    API endpoint for creating comments on a post and listing comments.

    POST /api/posts/<id>/comments/
        Creates a new comment on the specified post.
        Permission: IsAuthenticated

    GET /api/posts/<id>/comments/
        Returns all comments for the specified post.
        Permission: AllowAny

    Request Body (POST):
        - content (str): The text content of the comment.
    """

    def get_permissions(self):
        """
        Return appropriate permissions based on the request method.

        Returns:
            list: Permission instances for the current request.
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, pk):
        """
        List all comments for a specific post.

        Args:
            request: The HTTP request object.
            pk: The primary key of the post.

        Returns:
            Response: List of serialized comment data.
        """
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """
        Create a new comment on a specific post.

        Args:
            request: The HTTP request object.
            pk: The primary key of the post to comment on.

        Returns:
            Response: Serialized comment data on success.
        """
        post = get_object_or_404(Post, pk=pk)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    """
    API endpoint for liking a post.

    POST /api/posts/<id>/like/

    Creates a like relationship between the authenticated user and
    the specified post. Returns an error if the post is already liked.

    Permission: IsAuthenticated
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Like a specific post.

        Handles duplicate likes gracefully using IntegrityError
        from the unique_together constraint on the Like model.

        Args:
            request: The HTTP request object.
            pk: The primary key of the post to like.

        Returns:
            Response: Success or error message.
        """
        post = get_object_or_404(Post, pk=pk)

        try:
            Like.objects.create(post=post, user=request.user)
            return Response(
                {'detail': 'Post liked'},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {'detail': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UnlikeView(APIView):
    """
    API endpoint for unliking a post.

    POST /api/posts/<id>/unlike/

    Removes the like relationship between the authenticated user
    and the specified post.

    Permission: IsAuthenticated
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Unlike a specific post.

        Removes the Like object if it exists. Returns an error if
        the user hasn't liked the post.

        Args:
            request: The HTTP request object.
            pk: The primary key of the post to unlike.

        Returns:
            Response: Success or error message.
        """
        post = get_object_or_404(Post, pk=pk)

        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            return Response(
                {'detail': 'Like removed'},
                status=status.HTTP_200_OK,
            )
        except Like.DoesNotExist:
            return Response(
                {'detail': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
