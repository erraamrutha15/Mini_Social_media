"""
Models for the posts application.

Defines the Post, Comment, and Like models that form the core content
system of the social media platform. Users can create posts, comment
on posts, and like/unlike posts.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    """
    Model representing a social media post.

    Each post is authored by a user and contains text content.
    Posts are ordered by creation date (newest first).

    Attributes:
        author: The user who created the post.
        content: The text content of the post (max 1000 characters).
        created_at: Timestamp when the post was created.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='The user who authored this post.'
    )
    content = models.TextField(
        max_length=1000,
        blank=True,
        default='',
        help_text='The text content of the post (max 1000 characters).'
    )
    image = models.ImageField(
        upload_to='posts/images/',
        blank=True,
        null=True,
        help_text='Optional image attachment for the post.'
    )
    video = models.FileField(
        upload_to='posts/videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['mp4', 'webm', 'ogg', 'mov', 'avi']
        )],
        help_text='Optional video attachment for the post.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when this post was created.'
    )

    def __str__(self):
        """Return a truncated string representation of the post."""
        return f"{self.author.username}: {self.content[:50]}..."

    class Meta:
        """Meta options for the Post model."""
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    """
    Model representing a comment on a post.

    Each comment is linked to a specific post and authored by a user.
    Comments are ordered chronologically (oldest first).

    Attributes:
        post: The post this comment belongs to.
        author: The user who wrote the comment.
        content: The text content of the comment (max 500 characters).
        created_at: Timestamp when the comment was created.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='The post this comment belongs to.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='The user who wrote this comment.'
    )
    content = models.TextField(
        max_length=500,
        help_text='The text content of the comment (max 500 characters).'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when this comment was created.'
    )

    def __str__(self):
        """Return a string representation of the comment."""
        return f"Comment by {self.author.username} on Post {self.post.id}"

    class Meta:
        """Meta options for the Comment model."""
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Like(models.Model):
    """
    Model representing a like on a post.

    Each like links a user to a post. The unique_together constraint
    ensures a user can only like a post once.

    Attributes:
        post: The post that was liked.
        user: The user who liked the post.
        created_at: Timestamp when the like was created.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        help_text='The post that was liked.'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        help_text='The user who liked the post.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the like was created.'
    )

    def __str__(self):
        """Return a string representation of the like."""
        return f"{self.user.username} likes Post {self.post.id}"

    class Meta:
        """Meta options for the Like model."""
        unique_together = ('post', 'user')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
