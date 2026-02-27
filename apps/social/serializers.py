"""
Serializers for social app.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Discussion, Comment, StudyGroup, StudyGroupMembership, GroupPost, UserConnection

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""

    author = serializers.SerializerMethodField()
    upvotes_count = serializers.SerializerMethodField()
    is_upvoted = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'discussion', 'parent',
            'upvotes_count', 'is_upvoted', 'replies_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_author(self, obj):
        return {
            'id': str(obj.author.id),
            'username': obj.author.username,
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
            'avatar': obj.author.profile.avatar.url if hasattr(obj.author, 'profile') and obj.author.profile.avatar else None
        }

    def get_upvotes_count(self, obj):
        return obj.upvotes.count()

    def get_is_upvoted(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.upvotes.filter(id=request.user.id).exists()
        return False

    def get_replies_count(self, obj):
        return obj.replies.count()


class DiscussionSerializer(serializers.ModelSerializer):
    """Serializer for discussions."""

    author = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = [
            'id', 'title', 'content', 'author', 'course', 'lesson',
            'comments_count', 'is_author', 'is_pinned', 'is_resolved',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_author(self, obj):
        return {
            'id': str(obj.author.id),
            'username': obj.author.username,
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
            'avatar': obj.author.profile.avatar.url if hasattr(obj.author, 'profile') and obj.author.profile.avatar else None
        }

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.author == request.user
        return False


class StudyGroupMembershipSerializer(serializers.ModelSerializer):
    """Serializer for study group membership."""

    user = serializers.SerializerMethodField()

    class Meta:
        model = StudyGroupMembership
        fields = ['id', 'user', 'role', 'joined_at', 'is_active']
        read_only_fields = ['id', 'joined_at']

    def get_user(self, obj):
        return {
            'id': str(obj.user.id),
            'username': obj.user.username,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'avatar': obj.user.profile.avatar.url if hasattr(obj.user, 'profile') and obj.user.profile.avatar else None
        }


class StudyGroupSerializer(serializers.ModelSerializer):
    """Serializer for study groups."""

    creator = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()
    members = StudyGroupMembershipSerializer(many=True, read_only=True, source='studygroupmembership_set')

    class Meta:
        model = StudyGroup
        fields = [
            'id', 'name', 'description', 'creator', 'course',
            'members', 'members_count', 'is_member', 'is_creator',
            'max_members', 'is_private', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_creator(self, obj):
        return {
            'id': str(obj.creator.id),
            'username': obj.creator.username,
            'first_name': obj.creator.first_name,
            'last_name': obj.creator.last_name
        }

    def get_members_count(self, obj):
        return obj.members.count()

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.members.filter(id=request.user.id).exists()
        return False

    def get_is_creator(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.creator == request.user
        return False


class GroupPostSerializer(serializers.ModelSerializer):
    """Serializer for group posts."""

    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = GroupPost
        fields = [
            'id', 'title', 'content', 'author', 'study_group',
            'likes_count', 'is_liked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_author(self, obj):
        return {
            'id': str(obj.author.id),
            'username': obj.author.username,
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
            'avatar': obj.author.profile.avatar.url if hasattr(obj.author, 'profile') and obj.author.profile.avatar else None
        }

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.likes.filter(id=request.user.id).exists()
        return False


class UserConnectionSerializer(serializers.ModelSerializer):
    """Serializer for user connections."""

    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    connection_type = serializers.SerializerMethodField()

    class Meta:
        model = UserConnection
        fields = [
            'id', 'from_user', 'to_user', 'status',
            'connection_type', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_from_user(self, obj):
        return {
            'id': str(obj.from_user.id),
            'username': obj.from_user.username,
            'first_name': obj.from_user.first_name,
            'last_name': obj.from_user.last_name,
            'avatar': obj.from_user.profile.avatar.url if hasattr(obj.from_user, 'profile') and obj.from_user.profile.avatar else None
        }

    def get_to_user(self, obj):
        return {
            'id': str(obj.to_user.id),
            'username': obj.to_user.username,
            'first_name': obj.to_user.first_name,
            'last_name': obj.to_user.last_name,
            'avatar': obj.to_user.profile.avatar.url if hasattr(obj.to_user, 'profile') and obj.to_user.profile.avatar else None
        }

    def get_connection_type(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if obj.from_user == request.user:
                return 'following'
            elif obj.to_user == request.user:
                return 'follower'
        return 'connection'
