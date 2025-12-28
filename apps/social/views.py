from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from apps.social.models import Discussion, Comment, StudyGroup, StudyGroupMembership, GroupPost, UserConnection
from apps.social.serializers import (
    DiscussionSerializer, CommentSerializer, StudyGroupSerializer, 
    GroupPostSerializer, UserConnectionSerializer
)


class DiscussionListCreateView(generics.ListCreateAPIView):
    """
    List all discussions or create a new discussion.
    """
    serializer_class = DiscussionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter discussions by course or lesson if provided in query params
        course_id = self.request.query_params.get('course_id')
        lesson_id = self.request.query_params.get('lesson_id')
        
        queryset = Discussion.objects.all()
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DiscussionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific discussion.
    """
    serializer_class = DiscussionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Discussion.objects.all()


class CommentListCreateView(generics.ListCreateAPIView):
    """
    List all comments for a discussion or create a new comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        discussion_id = self.kwargs['discussion_id']
        return Comment.objects.filter(discussion_id=discussion_id)

    def perform_create(self, serializer):
        discussion_id = self.kwargs['discussion_id']
        discussion = get_object_or_404(Discussion, id=discussion_id)
        serializer.save(author=self.request.user, discussion=discussion)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()


class StudyGroupListCreateView(generics.ListCreateAPIView):
    """
    List all study groups or create a new study group.
    """
    serializer_class = StudyGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter by course if provided in query params
        course_id = self.request.query_params.get('course_id')
        user_id = self.request.query_params.get('user_id')
        
        queryset = StudyGroup.objects.all()
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if user_id:
            queryset = queryset.filter(members__id=user_id)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class StudyGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific study group.
    """
    serializer_class = StudyGroupSerializer
    permission_classes = [IsAuthenticated]
    queryset = StudyGroup.objects.all()


class StudyGroupMembershipView(generics.GenericAPIView):
    """
    Join or leave a study group.
    """
    permission_classes = [IsAuthenticated]
    queryset = StudyGroup.objects.all()

    def post(self, request, *args, **kwargs):
        study_group = self.get_object()
        
        # Check if group has reached max members
        if study_group.members.count() >= study_group.max_members:
            return Response(
                {'error': 'Study group has reached maximum number of members'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is already a member
        membership, created = StudyGroupMembership.objects.get_or_create(
            study_group=study_group,
            user=request.user,
            defaults={'role': 'member'}
        )
        
        if created:
            return Response(
                {'message': 'Successfully joined study group'}, 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'Already a member of this study group'}, 
                status=status.HTTP_200_OK
            )

    def delete(self, request, *args, **kwargs):
        study_group = self.get_object()
        
        try:
            membership = StudyGroupMembership.objects.get(
                study_group=study_group,
                user=request.user
            )
            membership.delete()
            return Response(
                {'message': 'Successfully left study group'}, 
                status=status.HTTP_200_OK
            )
        except StudyGroupMembership.DoesNotExist:
            return Response(
                {'error': 'Not a member of this study group'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class GroupPostListCreateView(generics.ListCreateAPIView):
    """
    List all posts for a study group or create a new post.
    """
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        study_group_id = self.kwargs['study_group_id']
        return GroupPost.objects.filter(study_group_id=study_group_id)

    def perform_create(self, serializer):
        study_group_id = self.kwargs['study_group_id']
        study_group = get_object_or_404(StudyGroup, id=study_group_id)
        
        # Check if user is a member of the study group
        if not StudyGroupMembership.objects.filter(
            study_group=study_group, 
            user=self.request.user,
            is_active=True
        ).exists():
            raise permissions.PermissionDenied("You must be a member of this study group to post.")
        
        serializer.save(author=self.request.user, study_group=study_group)


class GroupPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific group post.
    """
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]
    queryset = GroupPost.objects.all()


class UserConnectionListCreateView(generics.ListCreateAPIView):
    """
    List all connections for the user or create a new connection.
    """
    serializer_class = UserConnectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get all connections where the current user is either the from_user or to_user
        return UserConnection.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )

    def perform_create(self, serializer):
        to_user_id = self.request.data.get('to_user')
        to_user = get_object_or_404(User, id=to_user_id)
        
        # Check if connection already exists
        existing_connection = UserConnection.objects.filter(
            from_user=self.request.user,
            to_user=to_user
        ).first()
        
        if existing_connection:
            return Response(
                {'error': 'Connection already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save(from_user=self.request.user, to_user=to_user)


class UserConnectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific connection.
    """
    serializer_class = UserConnectionSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserConnection.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_connection(request, connection_id):
    """
    Accept a connection request.
    """
    try:
        connection = UserConnection.objects.get(
            id=connection_id, 
            to_user=request.user,
            status='pending'
        )
        connection.status = 'accepted'
        connection.save()
        return Response({'message': 'Connection accepted'}, status=status.HTTP_200_OK)
    except UserConnection.DoesNotExist:
        return Response(
            {'error': 'Connection request not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    """
    Like or unlike a comment.
    """
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        
        if request.user in comment.upvotes.all():
            comment.upvotes.remove(request.user)
            action = 'unliked'
        else:
            comment.upvotes.add(request.user)
            action = 'liked'
            
        return Response(
            {'message': f'Comment {action}', 'upvotes_count': comment.upvotes.count()}, 
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_group_post(request, post_id):
    """
    Like or unlike a group post.
    """
    try:
        post = get_object_or_404(GroupPost, id=post_id)
        
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            action = 'unliked'
        else:
            post.likes.add(request.user)
            action = 'liked'
            
        return Response(
            {'message': f'Post {action}', 'likes_count': post.likes.count()}, 
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_connections(request):
    """
    Get all connections for the current user.
    """
    connections = UserConnection.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        status='accepted'
    )
    
    # Get the connected users
    connected_users = []
    for conn in connections:
        if conn.from_user == request.user:
            connected_users.append({
                'id': conn.to_user.id,
                'username': conn.to_user.username,
                'email': conn.to_user.email,
                'first_name': conn.to_user.first_name,
                'last_name': conn.to_user.last_name
            })
        else:
            connected_users.append({
                'id': conn.from_user.id,
                'username': conn.from_user.username,
                'email': conn.from_user.email,
                'first_name': conn.from_user.first_name,
                'last_name': conn.from_user.last_name
            })
    
    return Response(connected_users, status=status.HTTP_200_OK)