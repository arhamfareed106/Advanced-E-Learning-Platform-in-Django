"""
Seed database with sample data for testing and demonstration.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Profile
from apps.courses.models import Category, Course, Lesson
from apps.quizzes.models import Quiz, Question, Answer
from decimal import Decimal

User = get_user_model()


def create_users():
    """Create sample users."""
    print("Creating users...")
    
    # Create admin
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_email_verified': True,
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"✓ Created admin user: admin / admin123")
    
    # Create instructor
    instructor, created = User.objects.get_or_create(
        username='instructor',
        defaults={
            'email': 'instructor@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'instructor',
            'is_email_verified': True,
        }
    )
    if created:
        instructor.set_password('instructor123')
        instructor.save()
        print(f"✓ Created instructor user: instructor / instructor123")
    
    # Create student
    student, created = User.objects.get_or_create(
        username='student',
        defaults={
            'email': 'student@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'student',
            'is_email_verified': True,
        }
    )
    if created:
        student.set_password('student123')
        student.save()
        print(f"✓ Created student user: student / student123")
    
    return admin, instructor, student


def create_categories():
    """Create sample categories."""
    print("\nCreating categories...")
    
    categories_data = [
        {'name': 'Web Development', 'icon': 'fa-code'},
        {'name': 'Data Science', 'icon': 'fa-chart-bar'},
        {'name': 'Mobile Development', 'icon': 'fa-mobile-alt'},
        {'name': 'Design', 'icon': 'fa-palette'},
        {'name': 'Business', 'icon': 'fa-briefcase'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'icon': cat_data['icon']}
        )
        categories.append(category)
        if created:
            print(f"✓ Created category: {category.name}")
    
    return categories


def create_courses(instructor, categories):
    """Create sample courses."""
    print("\nCreating courses...")
    
    courses_data = [
        {
            'title': 'Full Stack Web Development Bootcamp',
            'description': 'Learn to build modern web applications from scratch using the latest technologies.',
            'category': categories[0],
            'price': Decimal('49.99'),
            'difficulty': 'beginner',
            'status': 'published',
            'duration_hours': 40,
            'what_you_will_learn': [
                'HTML, CSS, and JavaScript fundamentals',
                'React and modern frontend development',
                'Node.js and Express backend',
                'Database design with PostgreSQL',
                'Deployment and DevOps basics'
            ],
            'requirements': [
                'Basic computer skills',
                'Willingness to learn'
            ]
        },
        {
            'title': 'Python for Data Science',
            'description': 'Master data analysis and machine learning with Python.',
            'category': categories[1],
            'price': Decimal('59.99'),
            'difficulty': 'intermediate',
            'status': 'published',
            'duration_hours': 35,
            'what_you_will_learn': [
                'Python programming basics',
                'NumPy and Pandas for data manipulation',
                'Data visualization with Matplotlib',
                'Machine learning with Scikit-learn',
                'Real-world data science projects'
            ],
            'requirements': [
                'Basic programming knowledge',
                'High school mathematics'
            ]
        },
        {
            'title': 'React Native Mobile Development',
            'description': 'Build cross-platform mobile apps with React Native.',
            'category': categories[2],
            'price': Decimal('0.00'),
            'difficulty': 'intermediate',
            'status': 'published',
            'duration_hours': 30,
            'what_you_will_learn': [
                'React Native fundamentals',
                'Navigation and routing',
                'State management with Redux',
                'API integration',
                'Publishing to App Store and Play Store'
            ],
            'requirements': [
                'JavaScript knowledge',
                'React basics'
            ]
        }
    ]
    
    courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults={
                **course_data,
                'instructor': instructor
            }
        )
        courses.append(course)
        if created:
            print(f"✓ Created course: {course.title}")
            
            # Create sample lessons
            create_lessons(course)
            
            # Create sample quiz
            create_quiz(course)
    
    return courses


def create_lessons(course):
    """Create sample lessons for a course."""
    lessons_data = [
        {
            'title': 'Introduction and Setup',
            'description': 'Get started with the course and set up your development environment.',
            'lesson_type': 'video',
            'chapter_number': 1,
            'order': 1,
            'duration_minutes': 15,
            'is_preview': True,
        },
        {
            'title': 'Core Concepts',
            'description': 'Learn the fundamental concepts you need to know.',
            'lesson_type': 'video',
            'chapter_number': 1,
            'order': 2,
            'duration_minutes': 30,
        },
        {
            'title': 'Hands-on Project',
            'description': 'Build your first project step by step.',
            'lesson_type': 'video',
            'chapter_number': 2,
            'order': 1,
            'duration_minutes': 45,
        },
        {
            'title': 'Advanced Techniques',
            'description': 'Master advanced techniques and best practices.',
            'lesson_type': 'video',
            'chapter_number': 2,
            'order': 2,
            'duration_minutes': 40,
        },
        {
            'title': 'Final Project',
            'description': 'Apply everything you learned in a comprehensive project.',
            'lesson_type': 'video',
            'chapter_number': 3,
            'order': 1,
            'duration_minutes': 60,
        },
    ]
    
    for lesson_data in lessons_data:
        Lesson.objects.get_or_create(
            course=course,
            title=lesson_data['title'],
            defaults=lesson_data
        )


def create_quiz(course):
    """Create a sample quiz for a course."""
    quiz, created = Quiz.objects.get_or_create(
        course=course,
        title='Final Assessment',
        defaults={
            'description': 'Test your knowledge of the course material.',
            'time_limit_minutes': 30,
            'passing_score': 70,
            'is_final_quiz': True,
        }
    )
    
    if created:
        # Create sample questions
        questions_data = [
            {
                'question_text': 'What is the main purpose of this course?',
                'question_type': 'mcq',
                'points': 10,
                'order': 1,
                'explanation': 'This course teaches practical skills for real-world applications.',
                'answers': [
                    {'answer_text': 'To learn practical skills', 'is_correct': True},
                    {'answer_text': 'To get a certificate', 'is_correct': False},
                    {'answer_text': 'To pass time', 'is_correct': False},
                ]
            },
            {
                'question_text': 'Is hands-on practice important for learning?',
                'question_type': 'true_false',
                'points': 10,
                'order': 2,
                'explanation': 'Practice is essential for mastering new skills.',
                'answers': [
                    {'answer_text': 'True', 'is_correct': True},
                    {'answer_text': 'False', 'is_correct': False},
                ]
            },
        ]
        
        for q_data in questions_data:
            answers_data = q_data.pop('answers')
            question = Question.objects.create(
                quiz=quiz,
                **q_data
            )
            
            for idx, a_data in enumerate(answers_data):
                Answer.objects.create(
                    question=question,
                    order=idx,
                    **a_data
                )


def main():
    """Main function to seed the database."""
    print("=" * 50)
    print("Seeding database with sample data...")
    print("=" * 50)
    
    admin, instructor, student = create_users()
    categories = create_categories()
    courses = create_courses(instructor, categories)
    
    print("\n" + "=" * 50)
    print("✓ Database seeding completed successfully!")
    print("=" * 50)
    print("\nSample Accounts:")
    print("  Admin:      admin / admin123")
    print("  Instructor: instructor / instructor123")
    print("  Student:    student / student123")
    print("\nYou can now log in and explore the platform!")


if __name__ == '__main__':
    main()
