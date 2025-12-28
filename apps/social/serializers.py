from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.social.models import Discussion, Comment, StudyGroup, StudyGroupMembership, GroupPost, UserConnection
from apps.courses.models import Course, Lesson

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar']
        read_only_fields = ['id']


class DiscussionSerializer(serializers.ModelSerializer):
    """
    Serializer for Discussion model.
    """
    author = UserSerializer(read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = Discussion
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'author')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """
    author = UserSerializer(read_only=True)
    upvotes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'author')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)
    
    def get_upvotes_count(self, obj):
        return obj.upvotes.count()


class StudyGroupMembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for StudyGroupMembership model.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudyGroupMembership
        fields = '__all__'
        read_only_fields = ('id', 'joined_at')


class StudyGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for StudyGroup model.
    """
    creator = UserSerializer(read_only=True)
    members = UserSerializer(read_only=True, many=True)
    member_count = serializers.SerializerMethodField()
    memberships = StudyGroupMembershipSerializer(source='studygroupmembership_set', many=True, read_only=True)
    
    class Meta:
        model = StudyGroup
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'creator', 'memberships')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creator'] = user
        return super().create(validated_data)
    
    def get_member_count(self, obj):
        return obj.members.count()


class GroupPostSerializer(serializers.ModelSerializer):
    """
    Serializer for GroupPost model.
    """
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupPost
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'author')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)
    
    def get_likes_count(self, obj):
        return obj.likes.count()


class UserConnectionSerializer(serializers.ModelSerializer):
    """
    Serializer for UserConnection model.
    """
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserConnection
        fields = '__all__'
        read_only_fields = ('id', 'created_at')