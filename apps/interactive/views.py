from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.interactive.models import CodeEditor, Flashcard, FlashcardDeck, Whiteboard, InteractiveSession
from apps.interactive.serializers import (
    CodeEditorSerializer, FlashcardSerializer, FlashcardDeckSerializer, 
    WhiteboardSerializer, InteractiveSessionSerializer
)


class CodeEditorListCreateView(generics.ListCreateAPIView):
    """
    List all code editors for the authenticated user or create a new code editor.
    """
    serializer_class = CodeEditorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CodeEditor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CodeEditorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific code editor.
    """
    serializer_class = CodeEditorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CodeEditor.objects.filter(user=self.request.user)


class FlashcardListCreateView(generics.ListCreateAPIView):
    """
    List all flashcards for the authenticated user or create a new flashcard.
    """
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Flashcard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlashcardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific flashcard.
    """
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Flashcard.objects.filter(user=self.request.user)


class FlashcardDeckListCreateView(generics.ListCreateAPIView):
    """
    List all flashcard decks for the authenticated user or create a new flashcard deck.
    """
    serializer_class = FlashcardDeckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FlashcardDeck.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlashcardDeckDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific flashcard deck.
    """
    serializer_class = FlashcardDeckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FlashcardDeck.objects.filter(user=self.request.user)


class WhiteboardListCreateView(generics.ListCreateAPIView):
    """
    List all whiteboards for the authenticated user or create a new whiteboard.
    """
    serializer_class = WhiteboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Whiteboard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WhiteboardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific whiteboard.
    """
    serializer_class = WhiteboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Whiteboard.objects.filter(user=self.request.user)


class InteractiveSessionListCreateView(generics.ListCreateAPIView):
    """
    List all interactive sessions for the authenticated user or create a new interactive session.
    """
    serializer_class = InteractiveSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InteractiveSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InteractiveSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific interactive session.
    """
    serializer_class = InteractiveSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InteractiveSession.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_code_editor_snapshot(request):
    """
    Create a snapshot of the current code editor state.
    """
    try:
        code_editor_id = request.data.get('code_editor_id')
        code_editor = get_object_or_404(CodeEditor, id=code_editor_id, user=request.user)
        
        # Create a snapshot from the current code
        snapshot = {
            'code': code_editor.code,
            'language': code_editor.language,
            'title': code_editor.title,
            'created_at': code_editor.updated_at
        }
        
        return Response(snapshot, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_code(request):
    """
    Run code in the code editor.
    """
    try:
        code_editor_id = request.data.get('code_editor_id')
        code_editor = get_object_or_404(CodeEditor, id=code_editor_id, user=request.user)
        
        # In a real implementation, this would connect to a code execution service
        # For now, we'll just return a mock response
        result = {
            'output': 'Code executed successfully',
            'error': None,
            'execution_time': 0.1
        }
        
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deck_cards(request, deck_id):
    """
    Get all flashcards in a specific deck.
    """
    try:
        deck = get_object_or_404(FlashcardDeck, id=deck_id, user=request.user)
        flashcards = Flashcard.objects.filter(deck=deck)
        serializer = FlashcardSerializer(flashcards, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_whiteboard_data(request, whiteboard_id):
    """
    Update whiteboard drawing data.
    """
    try:
        whiteboard = get_object_or_404(Whiteboard, id=whiteboard_id, user=request.user)
        drawing_data = request.data.get('drawing_data')
        
        whiteboard.drawing_data = drawing_data
        whiteboard.save()
        
        return Response({'message': 'Whiteboard updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)