"""
Serializers for quizzes app.
"""

from rest_framework import serializers
from .models import Quiz, Question, Answer, Attempt


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for answer choices."""
    
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct', 'order']
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        """Hide is_correct field for students."""
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Hide correct answer unless it's the instructor or after submission
        if request and hasattr(request, 'user'):
            if not (request.user.is_instructor or request.user.is_admin_user):
                hide_answer = self.context.get('hide_correct_answer', True)
                if hide_answer:
                    data.pop('is_correct', None)
        
        return data


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for questions."""
    
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'points', 'order', 'explanation', 'answers']
        read_only_fields = ['id']


class QuizListSerializer(serializers.ModelSerializer):
    """Serializer for quiz list."""
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'time_limit_minutes',
            'passing_score', 'is_final_quiz', 'total_questions',
            'total_points', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class QuizDetailSerializer(serializers.ModelSerializer):
    """Serializer for quiz detail with questions."""
    
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'time_limit_minutes',
            'passing_score', 'randomize_questions', 'show_answers_after_submission',
            'is_final_quiz', 'max_attempts', 'total_questions', 'total_points',
            'questions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AttemptSerializer(serializers.ModelSerializer):
    """Serializer for quiz attempts."""
    
    quiz = QuizListSerializer(read_only=True)
    
    class Meta:
        model = Attempt
        fields = [
            'id', 'quiz', 'answers', 'score', 'total_points',
            'earned_points', 'passed', 'started_at', 'submitted_at',
            'time_taken_seconds'
        ]
        read_only_fields = ['id', 'score', 'total_points', 'earned_points', 'passed', 'started_at', 'submitted_at']


class AttemptSubmitSerializer(serializers.Serializer):
    """Serializer for submitting quiz attempt."""
    
    quiz_id = serializers.UUIDField()
    answers = serializers.JSONField()  # {question_id: answer_id or answer_text}
