"""
Views for quizzes app.
"""

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
import random

from .models import Quiz, Question, Answer, Attempt
from apps.courses.models import Course
from apps.enrollment.models import Enrollment
from .serializers import (
    QuizListSerializer, QuizDetailSerializer, QuestionSerializer,
    AttemptSerializer, AttemptSubmitSerializer
)
from apps.users.permissions import IsStudent, IsInstructorOrAdmin


class QuizListView(generics.ListAPIView):
    """List quizzes for a course."""
    
    serializer_class = QuizListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Quiz.objects.filter(course_id=course_id)
        return Quiz.objects.none()


class QuizDetailView(generics.RetrieveAPIView):
    """Get quiz details with questions."""
    
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Hide correct answers for students before submission
        context['hide_correct_answer'] = True
        return context
    
    def retrieve(self, request, *args, **kwargs):
        quiz = self.get_object()
        
        # Check if student is enrolled
        if request.user.is_student:
            enrollment_exists = Enrollment.objects.filter(
                student=request.user,
                course=quiz.course
            ).exists()
            
            if not enrollment_exists:
                return Response({
                    'error': 'You must be enrolled in this course to access quizzes.'
                }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(quiz)
        data = serializer.data
        
        # Randomize questions if enabled
        if quiz.randomize_questions and 'questions' in data:
            questions = data['questions']
            random.shuffle(questions)
            data['questions'] = questions
        
        return Response(data)


class AttemptSubmitView(views.APIView):
    """Submit quiz attempt and get results."""
    
    permission_classes = [IsAuthenticated, IsStudent]
    
    def post(self, request):
        serializer = AttemptSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quiz_id = serializer.validated_data['quiz_id']
        answers = serializer.validated_data['answers']
        
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        # Check enrollment
        try:
            enrollment = Enrollment.objects.get(
                student=request.user,
                course=quiz.course
            )
        except Enrollment.DoesNotExist:
            return Response({
                'error': 'You are not enrolled in this course.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check max attempts
        if quiz.max_attempts > 0:
            attempt_count = Attempt.objects.filter(
                student=request.user,
                quiz=quiz
            ).count()
            
            if attempt_count >= quiz.max_attempts:
                return Response({
                    'error': f'Maximum attempts ({quiz.max_attempts}) reached for this quiz.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create attempt
        attempt = Attempt.objects.create(
            quiz=quiz,
            student=request.user,
            answers=answers
        )
        
        # Calculate score
        attempt.calculate_score()
        attempt.submitted_at = timezone.now()
        attempt.save()
        
        # Prepare response
        response_data = AttemptSerializer(attempt).data
        
        # Add detailed results if show_answers_after_submission is enabled
        if quiz.show_answers_after_submission:
            results = []
            for question in quiz.questions.all():
                question_id = str(question.id)
                student_answer = answers.get(question_id)
                
                question_result = {
                    'question_id': question_id,
                    'question_text': question.question_text,
                    'student_answer': student_answer,
                    'correct': False,
                    'explanation': question.explanation,
                    'correct_answers': []
                }
                
                if question.question_type in ['mcq', 'true_false']:
                    correct_answers = question.answers.filter(is_correct=True)
                    question_result['correct_answers'] = [
                        {'id': str(ans.id), 'text': ans.answer_text}
                        for ans in correct_answers
                    ]
                    
                    if student_answer:
                        try:
                            answer = question.answers.get(id=student_answer)
                            question_result['correct'] = answer.is_correct
                        except Answer.DoesNotExist:
                            pass
                
                elif question.question_type == 'short_answer':
                    correct_answers = question.answers.filter(is_correct=True)
                    question_result['correct_answers'] = [ans.answer_text for ans in correct_answers]
                    
                    if student_answer:
                        student_answer_lower = str(student_answer).lower().strip()
                        for correct in correct_answers:
                            if correct.answer_text.lower().strip() == student_answer_lower:
                                question_result['correct'] = True
                                break
                
                results.append(question_result)
            
            response_data['detailed_results'] = results
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class AttemptListView(generics.ListAPIView):
    """List all attempts for the current user."""
    
    serializer_class = AttemptSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        queryset = Attempt.objects.filter(student=self.request.user)
        quiz_id = self.request.query_params.get('quiz_id')
        if quiz_id:
            queryset = queryset.filter(quiz_id=quiz_id)
        return queryset.order_by('-started_at')


class AttemptDetailView(generics.RetrieveAPIView):
    """Get attempt details."""
    
    serializer_class = AttemptSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_student:
            return Attempt.objects.filter(student=self.request.user)
        return Attempt.objects.all()
