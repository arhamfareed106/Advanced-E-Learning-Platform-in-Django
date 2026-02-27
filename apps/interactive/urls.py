"""
URL patterns for interactive app API.
"""

from django.urls import path
from .views import (
    CodeEditorListCreateView, CodeEditorDetailView,
    FlashcardListCreateView, FlashcardDetailView,
    FlashcardDeckListCreateView, FlashcardDeckDetailView,
    WhiteboardListCreateView, WhiteboardDetailView,
    InteractiveSessionListCreateView, InteractiveSessionDetailView,
    create_code_editor_snapshot, run_code, get_deck_cards,
    update_whiteboard_data
)

app_name = 'interactive'

urlpatterns = [
    path('code-editor/', CodeEditorListCreateView.as_view(), name='code_editor_list'),
    path('code-editor/<uuid:pk>/', CodeEditorDetailView.as_view(), name='code_editor_detail'),
    path('flashcards/', FlashcardListCreateView.as_view(), name='flashcard_list'),
    path('flashcards/<uuid:pk>/', FlashcardDetailView.as_view(), name='flashcard_detail'),
    path('flashcard-decks/', FlashcardDeckListCreateView.as_view(), name='flashcard_deck_list'),
    path('flashcard-decks/<uuid:pk>/', FlashcardDeckDetailView.as_view(), name='flashcard_deck_detail'),
    path('whiteboards/', WhiteboardListCreateView.as_view(), name='whiteboard_list'),
    path('whiteboards/<uuid:pk>/', WhiteboardDetailView.as_view(), name='whiteboard_detail'),
    path('sessions/', InteractiveSessionListCreateView.as_view(), name='interactive_session_list'),
    path('sessions/<uuid:pk>/', InteractiveSessionDetailView.as_view(), name='interactive_session_detail'),
    path('code-editor/snapshot/', create_code_editor_snapshot, name='code_editor_snapshot'),
    path('code-editor/run/', run_code, name='code_editor_run'),
    path('flashcard-decks/<uuid:deck_id>/cards/', get_deck_cards, name='get_deck_cards'),
    path('whiteboards/<uuid:whiteboard_id>/update/', update_whiteboard_data, name='update_whiteboard_data'),
]
