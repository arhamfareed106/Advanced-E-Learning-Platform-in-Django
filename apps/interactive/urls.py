from django.urls import path
from . import views

urlpatterns = [
    # Code Editor URLs
    path('code-editors/', views.CodeEditorListCreateView.as_view(), name='code-editor-list-create'),
    path('code-editors/<uuid:pk>/', views.CodeEditorDetailView.as_view(), name='code-editor-detail'),
    path('code-editors/<uuid:pk>/snapshot/', views.create_code_editor_snapshot, name='code-editor-snapshot'),
    path('code-editors/<uuid:pk>/run/', views.run_code, name='run-code'),
    
    # Flashcard URLs
    path('flashcards/', views.FlashcardListCreateView.as_view(), name='flashcard-list-create'),
    path('flashcards/<uuid:pk>/', views.FlashcardDetailView.as_view(), name='flashcard-detail'),
    
    # Flashcard Deck URLs
    path('flashcard-decks/', views.FlashcardDeckListCreateView.as_view(), name='flashcard-deck-list-create'),
    path('flashcard-decks/<uuid:pk>/', views.FlashcardDeckDetailView.as_view(), name='flashcard-deck-detail'),
    path('flashcard-decks/<uuid:deck_id>/cards/', views.get_deck_cards, name='deck-cards'),
    
    # Whiteboard URLs
    path('whiteboards/', views.WhiteboardListCreateView.as_view(), name='whiteboard-list-create'),
    path('whiteboards/<uuid:pk>/', views.WhiteboardDetailView.as_view(), name='whiteboard-detail'),
    path('whiteboards/<uuid:whiteboard_id>/update/', views.update_whiteboard_data, name='update-whiteboard'),
    
    # Interactive Session URLs
    path('sessions/', views.InteractiveSessionListCreateView.as_view(), name='interactive-session-list-create'),
    path('sessions/<uuid:pk>/', views.InteractiveSessionDetailView.as_view(), name='interactive-session-detail'),
]