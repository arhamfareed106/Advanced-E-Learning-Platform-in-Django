"""
Test suite for the E-Learning Platform.
Run with: pytest
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from apps.users.models import User, Profile
from apps.courses.models import Category, Course, Lesson
from apps.enrollment.models import Enrollment
from apps.quizzes.models import Quiz, Question, Answer

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthentication:
    """Test user authentication endpoints."""

    def test_user_registration(self):
        """Test user can register."""
        client = APIClient()
        url = reverse('users:register')
        
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='test@example.com').exists()

    def test_user_login(self):
        """Test user can login."""
        client = APIClient()
        
        # Create user
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            role='student'
        )
        
        url = reverse('users:login')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_user_profile(self):
        """Test user can get their profile."""
        client = APIClient()
        
        # Create and authenticate user
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            role='student'
        )
        Profile.objects.create(user=user)
        
        client.force_authenticate(user=user)
        
        url = reverse('users:user_profile')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'test@example.com'


@pytest.mark.django_db
class TestCourses:
    """Test course endpoints."""

    def test_create_category(self):
        """Test category creation."""
        client = APIClient()
        
        # Create admin user
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        client.force_authenticate(user=admin)
        
        url = reverse('courses:category-list')
        data = {
            'name': 'Programming',
            'description': 'Programming courses',
            'icon': 'fa-code'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name='Programming').exists()

    def test_list_courses(self):
        """Test listing published courses."""
        client = APIClient()
        
        # Create category and course
        category = Category.objects.create(name='Programming')
        instructor = User.objects.create_user(
            email='instructor@example.com',
            password='instructor123',
            role='instructor'
        )
        
        course = Course.objects.create(
            instructor=instructor,
            category=category,
            title='Python Course',
            description='Learn Python',
            status='published',
            price=99.99
        )
        
        url = reverse('courses:course-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_course_detail(self):
        """Test course detail view."""
        client = APIClient()
        
        category = Category.objects.create(name='Programming')
        instructor = User.objects.create_user(
            email='instructor@example.com',
            password='instructor123',
            role='instructor'
        )
        
        course = Course.objects.create(
            instructor=instructor,
            category=category,
            title='Python Course',
            description='Learn Python',
            status='published',
            price=99.99
        )
        
        url = reverse('courses:course-detail', kwargs={'slug': course.slug})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Python Course'


@pytest.mark.django_db
class TestEnrollment:
    """Test enrollment endpoints."""

    def test_enroll_in_free_course(self):
        """Test enrolling in a free course."""
        client = APIClient()
        
        # Create student and course
        student = User.objects.create_user(
            email='student@example.com',
            password='student123',
            role='student'
        )
        client.force_authenticate(user=student)
        
        category = Category.objects.create(name='Programming')
        instructor = User.objects.create_user(
            email='instructor@example.com',
            password='instructor123',
            role='instructor'
        )
        
        course = Course.objects.create(
            instructor=instructor,
            category=category,
            title='Free Python Course',
            description='Learn Python',
            status='published',
            price=0  # Free course
        )
        
        url = reverse('enrollment:enrollment_create')
        data = {'course_id': str(course.id)}
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Enrollment.objects.filter(student=student, course=course).exists()

    def test_enroll_in_paid_course_without_payment(self):
        """Test enrolling in a paid course without payment."""
        client = APIClient()
        
        student = User.objects.create_user(
            email='student@example.com',
            password='student123',
            role='student'
        )
        client.force_authenticate(user=student)
        
        category = Category.objects.create(name='Programming')
        instructor = User.objects.create_user(
            email='instructor@example.com',
            password='instructor123',
            role='instructor'
        )
        
        course = Course.objects.create(
            instructor=instructor,
            category=category,
            title='Paid Python Course',
            description='Learn Python',
            status='published',
            price=99.99  # Paid course
        )
        
        url = reverse('enrollment:enrollment_create')
        data = {'course_id': str(course.id)}
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_402_PAYMENT_REQUIRED


@pytest.mark.django_db
class TestQuizzes:
    """Test quiz endpoints."""

    def test_create_quiz(self):
        """Test quiz creation."""
        client = APIClient()
        
        instructor = User.objects.create_user(
            email='instructor@example.com',
            password='instructor123',
            role='instructor'
        )
        client.force_authenticate(user=instructor)
        
        category = Category.objects.create(name='Programming')
        course = Course.objects.create(
            instructor=instructor,
            category=category,
            title='Python Course',
            description='Learn Python',
            status='published'
        )
        
        url = reverse('quizzes:quiz_list')
        data = {
            'course_id': str(course.id),
            'title': 'Python Quiz',
            'description': 'Test your Python knowledge',
            'time_limit_minutes': 30,
            'passing_score': 70
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Quiz.objects.filter(title='Python Quiz').exists()

    def test_submit_quiz_attempt(self):
        """Test submitting a quiz attempt."""
        client = APIClient()
        
        student = User.objects.create_user(
            email='student@example.com',
            password='student123',
            role='student'
        )
        client.force_authenticate(user=student)
        
        category = Category.objects.create(name='Programming')
        instructor = User.objects.create_user(
            email='instructor@example.com',
            password='instructor123',
            role='instructor'
        )
        
        course = Course.objects.create(
            instructor=instructor,
            category=category,
            title='Python Course',
            description='Learn Python',
            status='published'
        )
        
        # Create enrollment
        Enrollment.objects.create(student=student, course=course)
        
        # Create quiz
        quiz = Quiz.objects.create(
            course=course,
            title='Python Quiz',
            passing_score=70
        )
        
        # Create question and answer
        question = Question.objects.create(
            quiz=quiz,
            question_text='What is Python?',
            question_type='mcq',
            points=10
        )
        
        correct_answer = Answer.objects.create(
            question=question,
            answer_text='A programming language',
            is_correct=True
        )
        
        Answer.objects.create(
            question=question,
            answer_text='A snake',
            is_correct=False
        )
        
        url = reverse('quizzes:attempt_submit')
        data = {
            'quiz_id': str(quiz.id),
            'answers': {str(question.id): correct_answer.id}
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['passed'] is True


@pytest.mark.django_db
class TestReviews:
    """Test review endpoints."""

    def test_create_review(self):
        """Test creating a course review."""
        client = APIClient()
        
        student = User.objects.create_user(
            email='student@example.com',
            password='student123',
            role='student'
        )
        client.force_authenticate(user=student)
        
        category = Category.objects.create(name='Programming')
        instructor = User.objects.create_user(
            email='instructor@example.com',
            password='instructor123',
            role='instructor'
        )
        
        course = Course.objects.create(
            instructor=instructor,
            category=category,
            title='Python Course',
            description='Learn Python',
            status='published'
        )
        
        # Create enrollment
        Enrollment.objects.create(student=student, course=course)
        
        url = reverse('reviews:review_create')
        data = {
            'course_id': str(course.id),
            'rating': 5,
            'review_text': 'Excellent course!'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['rating'] == 5
