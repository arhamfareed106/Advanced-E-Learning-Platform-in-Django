"""
Comprehensive seed data script for the e-learning platform.
Creates sample users, courses, lessons, quizzes, enrollments, and more.

Usage:
    python manage.py shell < scripts/seed_data.py
    OR
    python manage.py runscript seed_data  (if django-extensions is installed)
"""

import os
import sys
import django
from datetime import timedelta
from decimal import Decimal
from random import choice, randint, uniform

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()

# Import all models
from apps.users.models import Profile
from apps.courses.models import Category, Course, Lesson
from apps.enrollment.models import Enrollment, LessonProgress
from apps.quizzes.models import Quiz, Question, Answer, Attempt
from apps.certificates.models import Certificate
from apps.payments.models import PaymentTransaction
from apps.notifications.models import Notification
from apps.reviews.models import Review
from apps.gamification.models import Badge, UserBadge, Achievement, Leaderboard, PointsTransaction, LearningStreak
from apps.interactive.models import CodeEditor, Flashcard, FlashcardDeck, Whiteboard
from apps.social.models import Discussion, Comment, StudyGroup, GroupPost, UserConnection
from apps.personalization.models import UserPreference, LearningPath, Recommendation
from apps.accessibility.models import AccessibilityPreference, AccessibilityFeature
from apps.analytics.models import LearningAnalytics, DashboardWidget


def clear_data():
    """Clear all existing data."""
    print("Clearing existing data...")
    
    # Delete in reverse order of dependencies
    LearningAnalytics.objects.all().delete()
    DashboardWidget.objects.all().delete()
    AccessibilityPreference.objects.all().delete()
    AccessibilityFeature.objects.all().delete()
    Recommendation.objects.all().delete()
    LearningPath.objects.all().delete()
    UserPreference.objects.all().delete()
    GroupPost.objects.all().delete()
    StudyGroup.objects.all().delete()
    UserConnection.objects.all().delete()
    Comment.objects.all().delete()
    Discussion.objects.all().delete()
    Whiteboard.objects.all().delete()
    FlashcardDeck.objects.all().delete()
    Flashcard.objects.all().delete()
    CodeEditor.objects.all().delete()
    LearningStreak.objects.all().delete()
    PointsTransaction.objects.all().delete()
    Leaderboard.objects.all().delete()
    Achievement.objects.all().delete()
    UserBadge.objects.all().delete()
    Badge.objects.all().delete()
    Review.objects.all().delete()
    Notification.objects.all().delete()
    PaymentTransaction.objects.all().delete()
    Certificate.objects.all().delete()
    Attempt.objects.all().delete()
    Question.objects.all().delete()
    Quiz.objects.all().delete()
    LessonProgress.objects.all().delete()
    Enrollment.objects.all().delete()
    Lesson.objects.all().delete()
    Course.objects.all().delete()
    Category.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.all().delete()
    
    print("Data cleared successfully!")


def create_users():
    """Create sample users."""
    print("\nCreating users...")
    
    # Admin user
    admin = User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_email_verified=True
    )
    Profile.objects.create(user=admin, bio='Platform administrator')
    print(f"  ✓ Created admin: {admin.email} / admin123")
    
    # Instructor users
    instructors_data = [
        {'email': 'instructor@example.com', 'username': 'instructor', 'password': 'instructor123',
         'first_name': 'John', 'last_name': 'Doe', 'bio': 'Senior Python Developer & Instructor'},
        {'email': 'sarah@example.com', 'username': 'sarah_instructor', 'password': 'instructor123',
         'first_name': 'Sarah', 'last_name': 'Johnson', 'bio': 'Web Development Expert'},
        {'email': 'mike@example.com', 'username': 'mike_instructor', 'password': 'instructor123',
         'first_name': 'Mike', 'last_name': 'Wilson', 'bio': 'Data Science & ML Specialist'},
    ]
    
    instructors = []
    for data in instructors_data:
        bio = data.pop('bio')
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            role='instructor',
            is_email_verified=True,
            **data
        )
        Profile.objects.create(user=user, bio=bio)
        instructors.append(user)
        print(f"  ✓ Created instructor: {user.email} / instructor123")
    
    # Student users
    students_data = [
        {'email': 'student@example.com', 'username': 'student', 'password': 'student123',
         'first_name': 'Alice', 'last_name': 'Smith'},
        {'email': 'bob@example.com', 'username': 'bob_student', 'password': 'student123',
         'first_name': 'Bob', 'last_name': 'Brown'},
        {'email': 'emma@example.com', 'username': 'emma_student', 'password': 'student123',
         'first_name': 'Emma', 'last_name': 'Davis'},
        {'email': 'charlie@example.com', 'username': 'charlie_student', 'password': 'student123',
         'first_name': 'Charlie', 'last_name': 'Miller'},
        {'email': 'diana@example.com', 'username': 'diana_student', 'password': 'student123',
         'first_name': 'Diana', 'last_name': 'Garcia'},
    ]
    
    students = []
    for data in students_data:
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            role='student',
            is_email_verified=True,
            **data
        )
        Profile.objects.create(user=user)
        students.append(user)
        print(f"  ✓ Created student: {user.email} / student123")
    
    return admin, instructors, students


def create_categories():
    """Create course categories."""
    print("\nCreating categories...")
    
    categories_data = [
        {'name': 'Programming', 'icon': 'fa-code', 'description': 'Programming and software development courses'},
        {'name': 'Web Development', 'icon': 'fa-globe', 'description': 'Frontend and backend web development'},
        {'name': 'Data Science', 'icon': 'fa-chart-line', 'description': 'Data analysis, ML, and AI courses'},
        {'name': 'Mobile Development', 'icon': 'fa-mobile-alt', 'description': 'iOS and Android app development'},
        {'name': 'DevOps', 'icon': 'fa-server', 'description': 'CI/CD, Docker, Kubernetes, and cloud'},
        {'name': 'Design', 'icon': 'fa-paint-brush', 'description': 'UI/UX and graphic design courses'},
        {'name': 'Business', 'icon': 'fa-briefcase', 'description': 'Business and entrepreneurship'},
        {'name': 'Marketing', 'icon': 'fa-bullhorn', 'description': 'Digital marketing and SEO'},
    ]
    
    categories = []
    for data in categories_data:
        category, _ = Category.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        categories.append(category)
        print(f"  ✓ Created category: {category.name}")
    
    return categories


def create_courses(instructors, categories):
    """Create sample courses."""
    print("\nCreating courses...")
    
    courses_data = [
        {
            'title': 'Complete Python Bootcamp: From Zero to Hero',
            'description': 'Learn Python programming from scratch with hands-on projects. Master variables, functions, OOP, and more.',
            'price': Decimal('89.99'),
            'difficulty': 'beginner',
            'duration_hours': 24,
            'language': 'English',
            'requirements': ['No programming experience needed', 'A computer with internet access'],
            'what_you_will_learn': ['Python fundamentals', 'Object-oriented programming', 'File handling', 'Error handling'],
        },
        {
            'title': 'Django Web Development Masterclass',
            'description': 'Build production-ready web applications with Django. Learn models, views, templates, REST APIs, and deployment.',
            'price': Decimal('99.99'),
            'difficulty': 'intermediate',
            'duration_hours': 32,
            'language': 'English',
            'requirements': ['Basic Python knowledge', 'HTML/CSS fundamentals'],
            'what_you_will_learn': ['Django ORM', 'Class-based views', 'REST API development', 'Authentication'],
        },
        {
            'title': 'React.js - The Complete Guide',
            'description': 'Master React.js including hooks, context, Redux, and modern React patterns. Build real-world projects.',
            'price': Decimal('79.99'),
            'difficulty': 'intermediate',
            'duration_hours': 28,
            'language': 'English',
            'requirements': ['JavaScript fundamentals', 'ES6+ knowledge'],
            'what_you_will_learn': ['React hooks', 'State management', 'Component patterns', 'React Router'],
        },
        {
            'title': 'Machine Learning A-Z: Hands-On Python & R',
            'description': 'Learn to create ML algorithms with Python and R. Covers supervised and unsupervised learning.',
            'price': Decimal('109.99'),
            'difficulty': 'advanced',
            'duration_hours': 44,
            'language': 'English',
            'requirements': ['Basic statistics', 'Python or R programming'],
            'what_you_will_learn': ['Regression', 'Classification', 'Clustering', 'Neural networks'],
        },
        {
            'title': 'Docker and Kubernetes: The Complete Guide',
            'description': 'Master containerization with Docker and orchestration with Kubernetes. Deploy scalable applications.',
            'price': Decimal('94.99'),
            'difficulty': 'intermediate',
            'duration_hours': 20,
            'language': 'English',
            'requirements': ['Basic Linux knowledge', 'Understanding of web applications'],
            'what_you_will_learn': ['Docker containers', 'Kubernetes pods', 'Service deployment', 'CI/CD pipelines'],
        },
        {
            'title': 'UI/UX Design Masterclass',
            'description': 'Learn to design beautiful user interfaces and experiences. Master Figma, design principles, and prototyping.',
            'price': Decimal('69.99'),
            'difficulty': 'beginner',
            'duration_hours': 18,
            'language': 'English',
            'requirements': ['No design experience needed'],
            'what_you_will_learn': ['Design principles', 'Figma tools', 'Prototyping', 'User research'],
        },
        {
            'title': 'JavaScript: The Advanced Concepts',
            'description': 'Deep dive into JavaScript. Master closures, prototypes, async programming, and design patterns.',
            'price': Decimal('74.99'),
            'difficulty': 'advanced',
            'duration_hours': 26,
            'language': 'English',
            'requirements': ['JavaScript basics', 'Some programming experience'],
            'what_you_will_learn': ['Closures', 'Prototypes', 'Async/await', 'Design patterns'],
        },
        {
            'title': 'AWS Certified Solutions Architect',
            'description': 'Prepare for AWS certification. Learn EC2, S3, Lambda, VPC, and cloud architecture best practices.',
            'price': Decimal('119.99'),
            'difficulty': 'advanced',
            'duration_hours': 36,
            'language': 'English',
            'requirements': ['Basic cloud concepts', 'Some IT experience'],
            'what_you_will_learn': ['EC2 & S3', 'Lambda functions', 'VPC networking', 'Security best practices'],
        },
    ]
    
    courses = []
    for i, data in enumerate(courses_data):
        instructor = instructors[i % len(instructors)]
        category = categories[i % len(categories)]
        
        course = Course.objects.create(
            instructor=instructor,
            category=category,
            status='published',
            published_at=timezone.now() - timedelta(days=randint(10, 100)),
            **data
        )
        courses.append(course)
        print(f"  ✓ Created course: {course.title}")
    
    return courses


def create_lessons(courses):
    """Create lessons for each course."""
    print("\nCreating lessons...")
    
    lessons_data = {
        'Python': [
            {'title': 'Introduction to Python', 'type': 'video', 'duration': 15, 'chapter': 1, 'is_preview': True},
            {'title': 'Installing Python', 'type': 'video', 'duration': 10, 'chapter': 1},
            {'title': 'Your First Python Program', 'type': 'video', 'duration': 20, 'chapter': 1},
            {'title': 'Variables and Data Types', 'type': 'video', 'duration': 25, 'chapter': 2},
            {'title': 'Strings and String Methods', 'type': 'video', 'duration': 30, 'chapter': 2},
            {'title': 'Lists and Tuples', 'type': 'video', 'duration': 35, 'chapter': 3},
            {'title': 'Dictionaries', 'type': 'video', 'duration': 30, 'chapter': 3},
            {'title': 'Functions', 'type': 'video', 'duration': 40, 'chapter': 4},
            {'title': 'Lambda Functions', 'type': 'video', 'duration': 20, 'chapter': 4},
            {'title': 'Classes and Objects', 'type': 'video', 'duration': 45, 'chapter': 5},
        ],
        'Django': [
            {'title': 'Introduction to Django', 'type': 'video', 'duration': 20, 'chapter': 1, 'is_preview': True},
            {'title': 'Setting Up Django', 'type': 'video', 'duration': 15, 'chapter': 1},
            {'title': 'Django Project Structure', 'type': 'video', 'duration': 25, 'chapter': 1},
            {'title': 'Models and Databases', 'type': 'video', 'duration': 40, 'chapter': 2},
            {'title': 'Django Admin', 'type': 'video', 'duration': 30, 'chapter': 2},
            {'title': 'Views and URLs', 'type': 'video', 'duration': 35, 'chapter': 3},
            {'title': 'Templates', 'type': 'video', 'duration': 40, 'chapter': 3},
            {'title': 'Forms', 'type': 'video', 'duration': 45, 'chapter': 4},
            {'title': 'Authentication', 'type': 'video', 'duration': 50, 'chapter': 4},
            {'title': 'REST APIs with DRF', 'type': 'video', 'duration': 55, 'chapter': 5},
        ],
        'React': [
            {'title': 'Introduction to React', 'type': 'video', 'duration': 18, 'chapter': 1, 'is_preview': True},
            {'title': 'Setting Up React', 'type': 'video', 'duration': 12, 'chapter': 1},
            {'title': 'JSX Basics', 'type': 'video', 'duration': 25, 'chapter': 1},
            {'title': 'Components and Props', 'type': 'video', 'duration': 35, 'chapter': 2},
            {'title': 'State and Events', 'type': 'video', 'duration': 40, 'chapter': 2},
            {'title': 'useState Hook', 'type': 'video', 'duration': 30, 'chapter': 3},
            {'title': 'useEffect Hook', 'type': 'video', 'duration': 35, 'chapter': 3},
            {'title': 'Context API', 'type': 'video', 'duration': 45, 'chapter': 4},
            {'title': 'React Router', 'type': 'video', 'duration': 40, 'chapter': 4},
            {'title': 'Redux Basics', 'type': 'video', 'duration': 50, 'chapter': 5},
        ],
    }
    
    lessons = []
    for course in courses:
        course_key = course.title.split()[0]  # Get first word of title
        course_lessons = lessons_data.get(course_key, lessons_data['Python'])
        
        for lesson_data in course_lessons:
            lesson = Lesson.objects.create(
                course=course,
                title=lesson_data['title'],
                lesson_type=lesson_data['type'],
                duration_minutes=lesson_data['duration'],
                chapter_number=lesson_data['chapter'],
                is_preview=lesson_data.get('is_preview', False),
                order=lesson_data['chapter'] * 100 + len(lessons) % 100,
            )
            lessons.append(lesson)
    
    print(f"  ✓ Created {len(lessons)} lessons across all courses")
    return lessons


def create_enrollments_and_progress(students, courses, lessons):
    """Create enrollments and lesson progress."""
    print("\nCreating enrollments and progress...")
    
    enrollments = []
    for student in students:
        # Each student enrolls in 2-4 random courses
        enrolled_courses = choice(courses[2:6])  # Skip first 2 for variety
        
        enrollment = Enrollment.objects.create(
            student=student,
            course=enrolled_courses,
            progress_percentage=uniform(10, 90),
        )
        enrollments.append(enrollment)
        
        # Create lesson progress for some lessons
        course_lessons = list(enrolled_courses.lessons.all())[:5]
        for lesson in course_lessons:
            is_completed = choice([True, False])
            LessonProgress.objects.create(
                enrollment=enrollment,
                lesson=lesson,
                is_completed=is_completed,
                watch_time_seconds=randint(60, lesson.duration_minutes * 60) if is_completed else randint(0, 300),
            )
    
    print(f"  ✓ Created {len(enrollments)} enrollments")
    return enrollments


def create_quizzes_and_attempts(courses, students):
    """Create quizzes and attempts."""
    print("\nCreating quizzes and attempts...")
    
    quizzes = []
    for course in courses[:4]:  # Add quizzes to first 4 courses
        quiz = Quiz.objects.create(
            course=course,
            title=f"{course.title.split()[-1]} Assessment",
            description=f"Test your knowledge of {course.title}",
            time_limit_minutes=30,
            passing_score=70,
            is_final_quiz=(course == courses[3]),
        )
        
        # Create questions
        for i in range(5):
            question = Question.objects.create(
                quiz=quiz,
                question_text=f"Question {i+1}: What is the correct way to...",
                question_type=choice(['mcq', 'mcq', 'true_false']),
                points=10,
                order=i,
            )
            
            # Create answers
            correct_answer = Answer.objects.create(
                question=question,
                answer_text="This is the correct answer",
                is_correct=True,
                order=0,
            )
            
            for j in range(3):
                Answer.objects.create(
                    question=question,
                    answer_text=f"Incorrect option {j+1}",
                    is_correct=False,
                    order=j+1,
                )
        
        quizzes.append(quiz)
        
        # Create attempts for some students
        for student in students[:2]:
            attempt = Attempt.objects.create(
                quiz=quiz,
                student=student,
                score=uniform(60, 100),
                passed=choice([True, False]),
                submitted_at=timezone.now() - timedelta(days=randint(1, 30)),
            )
    
    print(f"  ✓ Created {len(quizzes)} quizzes with questions")
    return quizzes


def create_reviews(students, courses, enrollments):
    """Create course reviews."""
    print("\nCreating reviews...")
    
    reviews = []
    for enrollment in enrollments[:6]:
        if enrollment.progress_percentage > 50:
            review = Review.objects.create(
                student=enrollment.student,
                course=enrollment.course,
                rating=randint(3, 5),
                review_text=choice([
                    "Excellent course! Learned a lot.",
                    "Great content and well explained.",
                    "Good course but could use more examples.",
                    "Amazing instructor, highly recommended!",
                    "Very comprehensive and up-to-date.",
                ]),
                is_verified_purchase=not enrollment.course.is_free,
            )
            reviews.append(review)
    
    print(f"  ✓ Created {len(reviews)} reviews")
    return reviews


def create_gamification_data(students):
    """Create gamification data (badges, achievements, leaderboard)."""
    print("\nCreating gamification data...")
    
    # Create badges
    badges_data = [
        {'name': 'First Course', 'description': 'Complete your first course', 'icon': 'fa-trophy', 'color': 'gold'},
        {'name': 'Quiz Master', 'description': 'Pass 10 quizzes', 'icon': 'fa-star', 'color': 'blue'},
        {'name': 'Fast Learner', 'description': 'Complete 5 lessons in a day', 'icon': 'fa-bolt', 'color': 'yellow'},
        {'name': 'Dedicated', 'description': '7-day learning streak', 'icon': 'fa-fire', 'color': 'red'},
        {'name': 'Expert', 'description': 'Complete an advanced course', 'icon': 'fa-crown', 'color': 'purple'},
    ]
    
    badges = []
    for data in badges_data:
        badge = Badge.objects.create(**data)
        badges.append(badge)
    
    # Award badges to students
    for student in students[:3]:
        UserBadge.objects.create(user=student, badge=choice(badges))
    
    # Create achievements
    for student in students:
        Achievement.objects.create(
            user=student,
            title="Course Enrolled",
            description="Enrolled in your first course",
            points=50,
            achievement_type='enrollment',
        )
    
    # Create leaderboard entries
    for student in students:
        Leaderboard.objects.create(
            user=student,
            points=randint(100, 1000),
            level=randint(1, 10),
        )
    
    # Create learning streaks
    for student in students:
        LearningStreak.objects.create(
            user=student,
            current_streak=randint(0, 30),
            longest_streak=randint(5, 50),
            last_activity_date=timezone.now().date(),
        )
    
    print(f"  ✓ Created badges, achievements, and leaderboard")


def create_social_data(students, courses):
    """Create social data (discussions, study groups, connections)."""
    print("\nCreating social data...")
    
    # Create discussions
    for i, student in enumerate(students[:3]):
        course = courses[i % len(courses)]
        discussion = Discussion.objects.create(
            title=f"Question about {course.title}",
            content="Can someone explain this concept in more detail?",
            author=student,
            course=course,
        )
        
        # Add comments
        for other_student in students[1:3]:
            Comment.objects.create(
                discussion=discussion,
                content="Great question! Here's my understanding...",
                author=other_student,
            )
    
    # Create study groups
    for course in courses[:3]:
        group = StudyGroup.objects.create(
            name=f"{course.title} Study Group",
            description=f"Study group for {course.title} students",
            creator=students[0],
            course=course,
            max_members=10,
        )
        
        # Add members
        for student in students[:3]:
            from apps.social.models import StudyGroupMembership
            StudyGroupMembership.objects.create(
                study_group=group,
                user=student,
                role='member' if student != students[0] else 'admin',
            )
    
    # Create user connections
    for i, student in enumerate(students[1:], 1):
        UserConnection.objects.create(
            from_user=students[0],
            to_user=student,
            status='accepted',
        )
    
    print(f"  ✓ Created discussions, study groups, and connections")


def create_personalization_data(students, courses):
    """Create personalization data (preferences, learning paths, recommendations)."""
    print("\nCreating personalization data...")
    
    for student in students:
        # Create preferences
        UserPreference.objects.create(
            user=student,
            learning_style=choice(['visual', 'auditory', 'kinesthetic']),
            difficulty_level='intermediate',
            study_time_preference=choice(['morning', 'afternoon', 'evening']),
        )
        
        # Create learning path
        learning_path = LearningPath.objects.create(
            user=student,
            title=f"{student.first_name}'s Learning Path",
            description="Personalized learning journey",
        )
        learning_path.courses.add(*courses[:2])
        
        # Create recommendations
        for course in courses[:3]:
            Recommendation.objects.create(
                user=student,
                content_type='course',
                content_id=course.id,
                title=course.title,
                description=f"Recommended based on your interests",
                confidence_score=uniform(0.6, 0.95),
            )
    
    print(f"  ✓ Created preferences, learning paths, and recommendations")


def create_accessibility_data():
    """Create accessibility features."""
    print("\nCreating accessibility data...")
    
    features_data = [
        {'name': 'Screen Reader Support', 'description': 'Full screen reader compatibility'},
        {'name': 'Keyboard Navigation', 'description': 'Navigate without a mouse'},
        {'name': 'High Contrast Mode', 'description': 'Enhanced contrast for better visibility'},
        {'name': 'Text-to-Speech', 'description': 'Audio narration for content'},
        {'name': 'Closed Captions', 'description': 'Subtitles for all video content'},
    ]
    
    for data in features_data:
        AccessibilityFeature.objects.create(**data)
    
    print(f"  ✓ Created accessibility features")


def create_analytics_data(students, courses):
    """Create analytics data."""
    print("\nCreating analytics data...")
    
    from apps.analytics.models import LearningAnalytics, UserBehaviorTracking, DashboardWidget
    
    for student in students:
        for course in courses[:2]:
            LearningAnalytics.objects.create(
                user=student,
                course=course,
                time_spent_seconds=randint(3600, 36000),
                page_views=randint(10, 100),
                video_views=randint(5, 50),
                video_completion_rate=uniform(30, 100),
                quiz_attempts=randint(1, 5),
                quiz_average_score=uniform(60, 100),
                course_completion_rate=uniform(10, 90),
                lessons_completed=randint(1, 10),
                total_lessons=10,
                performance_score=uniform(50, 100),
                engagement_score=uniform(40, 100),
            )
    
    # Create some behavior tracking
    for student in students[:2]:
        UserBehaviorTracking.objects.create(
            user=student,
            event_type='page_view',
            content_type='course',
            content_id=courses[0].id,
            page_url=f'/courses/{courses[0].slug}/',
        )
    
    # Create dashboard widgets
    DashboardWidget.objects.create(
        title='My Progress',
        widget_type='progress',
        data_source='/api/analytics/summary/',
        position=1,
        owner=students[0],
    )
    
    print(f"  ✓ Created analytics data")


def main():
    """Main seed function."""
    print("=" * 60)
    print("E-LEARNING PLATFORM - SEED DATA SCRIPT")
    print("=" * 60)
    
    # Ask for confirmation
    response = input("\nThis will clear all existing data and create new sample data. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Seed operation cancelled.")
        return
    
    # Clear existing data
    clear_data()
    
    # Create all data
    admin, instructors, students = create_users()
    categories = create_categories()
    courses = create_courses(instructors, categories)
    lessons = create_lessons(courses)
    enrollments = create_enrollments_and_progress(students, courses, lessons)
    quizzes = create_quizzes_and_attempts(courses, students)
    reviews = create_reviews(students, courses, enrollments)
    create_gamification_data(students)
    create_social_data(students, courses)
    create_personalization_data(students, courses)
    create_accessibility_data()
    create_analytics_data(students, courses)
    
    print("\n" + "=" * 60)
    print("SEED DATA CREATED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📊 Summary:")
    print(f"   • Users: {User.objects.count()} (1 admin, {len(instructors)} instructors, {len(students)} students)")
    print(f"   • Categories: {Category.objects.count()}")
    print(f"   • Courses: {Course.objects.count()}")
    print(f"   • Lessons: {Lesson.objects.count()}")
    print(f"   • Enrollments: {Enrollment.objects.count()}")
    print(f"   • Quizzes: {Quiz.objects.count()}")
    print(f"   • Reviews: {Review.objects.count()}")
    print("\n🔐 Sample Login Credentials:")
    print("   Admin:      admin@example.com / admin123")
    print("   Instructor: instructor@example.com / instructor123")
    print("   Student:    student@example.com / student123")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
