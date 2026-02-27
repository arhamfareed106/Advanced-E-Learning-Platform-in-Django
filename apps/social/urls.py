"""
URL patterns for social app API.
"""

from django.urls import path
from .views import (
    DiscussionListCreateView, DiscussionDetailView,
    CommentListCreateView, CommentDetailView,
    StudyGroupListCreateView, StudyGroupDetailView,
    StudyGroupMembershipView,
    GroupPostListCreateView, GroupPostDetailView,
    UserConnectionListCreateView, UserConnectionDetailView,
    accept_connection, like_comment, like_group_post, get_user_connections
)

app_name = 'social'

urlpatterns = [
    # Discussions
    path('discussions/', DiscussionListCreateView.as_view(), name='discussion_list'),
    path('discussions/<uuid:pk>/', DiscussionDetailView.as_view(), name='discussion_detail'),

    # Comments
    path('discussions/<uuid:discussion_id>/comments/', CommentListCreateView.as_view(), name='comment_list'),
    path('comments/<uuid:pk>/', CommentDetailView.as_view(), name='comment_detail'),

    # Study Groups
    path('study-groups/', StudyGroupListCreateView.as_view(), name='study_group_list'),
    path('study-groups/<uuid:pk>/', StudyGroupDetailView.as_view(), name='study_group_detail'),
    path('study-groups/<uuid:pk>/join/', StudyGroupMembershipView.as_view(), name='study_group_join'),

    # Group Posts
    path('study-groups/<uuid:study_group_id>/posts/', GroupPostListCreateView.as_view(), name='group_post_list'),
    path('group-posts/<uuid:pk>/', GroupPostDetailView.as_view(), name='group_post_detail'),

    # User Connections
    path('connections/', UserConnectionListCreateView.as_view(), name='user_connection_list'),
    path('connections/<uuid:pk>/', UserConnectionDetailView.as_view(), name='user_connection_detail'),
    path('connections/<uuid:connection_id>/accept/', accept_connection, name='accept_connection'),
    path('my-connections/', get_user_connections, name='get_user_connections'),

    # Likes
    path('comments/<uuid:comment_id>/like/', like_comment, name='like_comment'),
    path('posts/<uuid:post_id>/like/', like_group_post, name='like_group_post'),
]
