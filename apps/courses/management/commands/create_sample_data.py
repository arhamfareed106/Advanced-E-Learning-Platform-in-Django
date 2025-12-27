"""
Django management command to create sample data for the e-learning platform.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.users.models import User
from apps.courses.models import Category, Course, Lesson
from apps.enrollment.models import Enrollment
from apps.reviews.models import Review


class Command(BaseCommand):
    help = 'Creates sample data for the e-learning platform'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {'name': 'Web Development', 'description': 'Learn web development'},
            {'name': 'Data Science', 'description': 'Master data science'},
            {'name': 'Mobile Development', 'description': 'Build mobile apps'},
            {'name': 'Design', 'description': 'Learn design principles'},
            {'name': 'Business', 'description': 'Business and entrepreneurship'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create instructors
        instructors = []
        for i in range(1, 4):
            instructor, created = User.objects.get_or_create(
                email=f'instructor{i}@example.com',
                defaults={
                    'username': f'instructor{i}',
                    'first_name': f'Instructor',
                    'last_name': f'{i}',
                    'role': 'instructor',
                }
            )
            if created:
                instructor.set_password('password123')
                instructor.save()
                self.stdout.write(f'Created instructor: {instructor.email}')
            instructors.append(instructor)

        # Create students
        students = []
        for i in range(1, 6):
            student, created = User.objects.get_or_create(
                email=f'student{i}@example.com',
                defaults={
                    'username': f'student{i}',
                    'first_name': f'Student',
                    'last_name': f'{i}',
                    'role': 'student',
                }
            )
            if created:
                student.set_password('password123')
                student.save()
                self.stdout.write(f'Created student: {student.email}')
            students.append(student)

        # Create courses
        courses_data = [
            {
                'title': 'Full Stack Web Development',
                'description': 'Learn to build full-stack web applications using modern technologies. Master frontend and backend development.',
                'category': categories[0],
                'instructor': instructors[0],
                'price': 49.99,
                'difficulty': 'intermediate',
                'duration_hours': 40,
            },
            {
                'title': 'Python for Data Science',
                'description': 'Learn data science fundamentals using Python and popular libraries like pandas, numpy, and matplotlib.',
                'category': categories[1],
                'instructor': instructors[1],
                'price': 59.99,
                'difficulty': 'beginner',
                'duration_hours': 30,
            },
            {
                'title': 'React Native Mobile Apps',
                'description': 'Create iOS and Android apps using React Native. Build cross-platform mobile applications.',
                'category': categories[2],
                'instructor': instructors[2],
                'price': 69.99,
                'difficulty': 'intermediate',
                'duration_hours': 35,
            },
            {
                'title': 'UI/UX Design Fundamentals',
                'description': 'Master the fundamentals of user interface and user experience design. Learn design principles and tools.',
                'category': categories[3],
                'instructor': instructors[0],
                'price': 39.99,
                'difficulty': 'beginner',
                'duration_hours': 25,
            },
            {
                'title': 'Digital Marketing Mastery',
                'description': 'Learn all aspects of digital marketing from SEO to social media. Complete marketing course.',
                'category': categories[4],
                'instructor': instructors[1],
                'is_free': True,
                'difficulty': 'beginner',
                'duration_hours': 20,
            },
        ]

        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    **course_data,
                    'slug': slugify(course_data['title']),
                    'status': 'published',
                }
            )
            courses.append(course)
            if created:
                self.stdout.write(f'Created course: {course.title}')
                
                # Create lessons for each course
                for i in range(1, 6):
                    Lesson.objects.create(
                        course=course,
                        title=f'Lesson {i}: Introduction to Module {i}',
                        description=f'Learn about module {i} in this comprehensive lesson.',
                        chapter_number=1,
                        order=i,
                        duration_minutes=30,
                    )
                self.stdout.write(f'  Created 5 lessons for {course.title}')

        # Create enrollments
        for student in students[:3]:
            for course in courses[:2]:
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course
                )
                if created:
                    self.stdout.write(f'Enrolled {student.email} in {course.title}')

        # Create reviews
        reviews_data = [
            {'course': courses[0], 'student': students[0], 'rating': 5, 'review_text': 'Excellent course! Learned so much.'},
            {'course': courses[0], 'student': students[1], 'rating': 4, 'review_text': 'Great content, well structured.'},
            {'course': courses[1], 'student': students[2], 'rating': 5, 'review_text': 'Perfect for beginners!'},
        ]
        
        for review_data in reviews_data:
            review, created = Review.objects.get_or_create(
                course=review_data['course'],
                student=review_data['student'],
                defaults={
                    'rating': review_data['rating'],
                    'review_text': review_data['review_text'],
                }
            )
            if created:
                self.stdout.write(f'Created review for {review_data["course"].title}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('\nTest accounts:')
        self.stdout.write('Instructors: instructor1@example.com, instructor2@example.com, instructor3@example.com')
        self.stdout.write('Students: student1@example.com, student2@example.com, student3@example.com')
        self.stdout.write('Password for all accounts: password123')
