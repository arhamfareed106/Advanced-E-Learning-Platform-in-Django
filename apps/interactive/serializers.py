from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.interactive.models import CodeEditor, Flashcard, FlashcardDeck, Whiteboard, InteractiveSession

User = get_user_model()


class CodeEditorSerializer(serializers.ModelSerializer):
    """
    Serializer for CodeEditor model.
    """
    class Meta:
        model = CodeEditor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class FlashcardSerializer(serializers.ModelSerializer):
    """
    Serializer for Flashcard model.
    """
    class Meta:
        model = Flashcard
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class FlashcardDeckSerializer(serializers.ModelSerializer):
    """
    Serializer for FlashcardDeck model.
    """
    flashcards = FlashcardSerializer(many=True, read_only=True)
    
    class Meta:
        model = FlashcardDeck
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class WhiteboardSerializer(serializers.ModelSerializer):
    """
    Serializer for Whiteboard model.
    """
    class Meta:
        model = Whiteboard
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class InteractiveSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for InteractiveSession model.
    """
    class Meta:
        model = InteractiveSession
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)