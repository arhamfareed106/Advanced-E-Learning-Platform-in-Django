"""
Quick seed script - runs without confirmation
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from scripts.seed_data import (
    clear_data, create_users, create_categories, create_courses,
    create_lessons, create_enrollments_and_progress,
    create_quizzes_and_attempts, create_reviews, create_gamification_data,
    create_social_data, create_personalization_data,
    create_accessibility_data, create_analytics_data
)

print("=" * 60)
print("SEEDING DATABASE...")
print("=" * 60)

clear_data()
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
print("✅ SEED DATA CREATED SUCCESSFULLY!")
print("=" * 60)
print("\n📊 Summary:")
from apps.users.models import User
from apps.courses.models import Course, Category
from apps.enrollment.models import Enrollment
print(f"   • Users: {User.objects.count()}")
print(f"   • Categories: {Category.objects.count()}")
print(f"   • Courses: {Course.objects.count()}")
print(f"   • Enrollments: {Enrollment.objects.count()}")
print("\n🔐 Sample Login Credentials:")
print("   Admin:      admin@example.com / admin123")
print("   Instructor: instructor@example.com / instructor123")
print("   Student:    student@example.com / student123")
print("\n🌐 Server running at: http://127.0.0.1:8000")
print("=" * 60)
