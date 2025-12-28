from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Lesson
import uuid

User = get_user_model()


class Discussion(models.Model):
    """
    Model for course discussions and Q&A.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='discussions', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='discussions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['course', '-created_at']),
            models.Index(fields=['lesson', '-created_at']),
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Model for comments on discussions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(User, related_name='upvoted_comments', blank=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.discussion.title}'


class StudyGroup(models.Model):
    """
    Model for study groups.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_study_groups')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_groups', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='study_groups', through='StudyGroupMembership')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    max_members = models.PositiveIntegerField(default=10)
    is_private = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class StudyGroupMembership(models.Model):
    """
    Model for study group membership.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=[
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ], default='member')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('study_group', 'user')

    def __str__(self):
        return f'{self.user.username} in {self.study_group.name}'


class GroupPost(models.Model):
    """
    Model for posts in study groups.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_posts')
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_group_posts', blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class UserConnection(models.Model):
    """
    Model for user connections/friendships.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('blocked', 'Blocked'),
    ], default='pending')
    
    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username}'