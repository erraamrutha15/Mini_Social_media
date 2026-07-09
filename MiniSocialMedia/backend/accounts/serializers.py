"""
Serializers for the accounts application.

Provides serialization and deserialization for User, Registration, and Profile
data, converting between Django model instances and JSON representations.
"""

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile, Follow


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Django User model.

    Used for listing all users with their basic information.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles validation and creation of new user accounts.
    The password field is write-only to prevent it from being
    included in API responses.
    """

    password = serializers.CharField(
        write_only=True,
        help_text='User password (write-only, never returned in responses).'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        """
        Create a new User instance with properly hashed password.

        Uses Django's create_user method to ensure the password is
        hashed before being stored in the database.

        Args:
            validated_data: Dictionary of validated field values.

        Returns:
            User: The newly created User instance.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class ProfilePostSerializer(serializers.Serializer):
    """
    Minimal post serializer for nesting within profile responses.

    Avoids circular imports by not importing from the posts app.
    Provides only the essential post data needed for a profile view.
    """

    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

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


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the user Profile model.

    Provides detailed user profile information including follower/following
    counts, whether the requesting user follows this profile, and the
    user's posts.
    """

    # Fields from the related User model
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    # Computed fields
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'first_name', 'last_name', 'bio',
            'followers_count', 'following_count', 'is_following', 'posts',
        ]

    def get_followers_count(self, obj):
        """
        Return the number of users who follow this profile's user.

        Args:
            obj: The Profile instance.

        Returns:
            int: Number of followers.
        """
        return obj.user.followers_set.count()

    def get_following_count(self, obj):
        """
        Return the number of users this profile's user is following.

        Args:
            obj: The Profile instance.

        Returns:
            int: Number of users being followed.
        """
        return obj.user.following_set.count()

    def get_is_following(self, obj):
        """
        Check if the requesting user is following this profile's user.

        Returns False for anonymous (unauthenticated) users.

        Args:
            obj: The Profile instance.

        Returns:
            bool: True if the requesting user follows this profile's user.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(
                follower=request.user,
                following=obj.user
            ).exists()
        return False

    def get_posts(self, obj):
        """
        Return all posts authored by this profile's user.

        Uses a minimal serializer to avoid circular imports with
        the posts application.

        Args:
            obj: The Profile instance.

        Returns:
            list: Serialized post data.
        """
        posts = obj.user.posts.all().order_by('-created_at')
        return ProfilePostSerializer(posts, many=True).data

    def update(self, instance, validated_data):
        """
        Update the Profile and related User fields.

        Handles nested User data (first_name, last_name) alongside
        Profile-specific data (bio).

        Args:
            instance: The Profile instance to update.
            validated_data: Dictionary of validated field values.

        Returns:
            Profile: The updated Profile instance.
        """
        # Extract nested user data if present
        user_data = validated_data.pop('user', {})

        # Update User fields
        user = instance.user
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        user.save()

        # Update Profile fields
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        return instance
