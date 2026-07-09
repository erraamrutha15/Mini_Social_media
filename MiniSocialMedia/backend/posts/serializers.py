"""
Serializers for the posts application.

Provides serialization and deserialization for Post, Comment, and Like
data, converting between Django model instances and JSON representations
for the REST API.
"""

from rest_framework import serializers

from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    Includes the author's username as a read-only field derived from
    the related User model. The post and author fields are read-only
    as they are set automatically in the view.
    """

    # Derived field: author's username from the related User model
    author_username = serializers.CharField(
        source='author.username',
        read_only=True,
        help_text='Username of the comment author.'
    )

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'author_username',
            'content', 'created_at',
        ]
        read_only_fields = ['post', 'author']


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.

    Includes computed fields for like count, comment count, whether
    the current user has liked the post, and nested comments.
    """

    # Derived field: author's username from the related User model
    author_username = serializers.CharField(
        source='author.username',
        read_only=True,
        help_text='Username of the post author.'
    )

    # Computed fields
    like_count = serializers.SerializerMethodField(
        help_text='Total number of likes on this post.'
    )
    comment_count = serializers.SerializerMethodField(
        help_text='Total number of comments on this post.'
    )
    is_liked = serializers.SerializerMethodField(
        help_text='Whether the requesting user has liked this post.'
    )

    # Nested comments
    comments = CommentSerializer(
        many=True,
        read_only=True,
        help_text='All comments on this post.'
    )

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username', 'content', 'image', 'video', 'created_at',
            'like_count', 'comment_count', 'is_liked', 'comments',
        ]
        read_only_fields = ['author']

    def get_like_count(self, obj):
        """
        Return the total number of likes on the post.

        Args:
            obj: The Post instance.

        Returns:
            int: The count of likes.
        """
        return obj.likes.count()

    def get_comment_count(self, obj):
        """
        Return the total number of comments on the post.

        Args:
            obj: The Post instance.

        Returns:
            int: The count of comments.
        """
        return obj.comments.count()

    def get_is_liked(self, obj):
        """
        Check if the requesting user has liked this post.

        Returns False for anonymous (unauthenticated) users or when
        no request context is available.

        Args:
            obj: The Post instance.

        Returns:
            bool: True if the requesting user has liked this post.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                post=obj,
                user=request.user,
            ).exists()
        return False
