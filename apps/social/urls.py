from django.urls import path
from . import views

urlpatterns = [
    # Discussion URLs
    path('discussions/', views.DiscussionListCreateView.as_view(), name='discussion-list-create'),
    path('discussions/<uuid:pk>/', views.DiscussionDetailView.as_view(), name='discussion-detail'),
    
    # Comment URLs
    path('discussions/<uuid:discussion_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<uuid:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<uuid:comment_id>/like/', views.like_comment, name='like-comment'),
    
    # Study Group URLs
    path('study-groups/', views.StudyGroupListCreateView.as_view(), name='study-group-list-create'),
    path('study-groups/<uuid:pk>/', views.StudyGroupDetailView.as_view(), name='study-group-detail'),
    path('study-groups/<uuid:study_group_id>/join/', views.StudyGroupMembershipView.as_view(), name='study-group-join'),
    path('study-groups/<uuid:study_group_id>/leave/', views.StudyGroupMembershipView.as_view(), name='study-group-leave'),
    
    # Group Post URLs
    path('study-groups/<uuid:study_group_id>/posts/', views.GroupPostListCreateView.as_view(), name='group-post-list-create'),
    path('posts/<uuid:pk>/', views.GroupPostDetailView.as_view(), name='group-post-detail'),
    path('posts/<uuid:post_id>/like/', views.like_group_post, name='like-group-post'),
    
    # User Connection URLs
    path('connections/', views.UserConnectionListCreateView.as_view(), name='connection-list-create'),
    path('connections/<uuid:pk>/', views.UserConnectionDetailView.as_view(), name='connection-detail'),
    path('connections/<uuid:connection_id>/accept/', views.accept_connection, name='accept-connection'),
    path('user-connections/', views.get_user_connections, name='user-connections'),
]