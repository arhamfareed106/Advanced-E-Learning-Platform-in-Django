"""
Serializers for certificates app.
"""

from rest_framework import serializers
from .models import Certificate
from apps.courses.serializers import CourseListSerializer


class CertificateSerializer(serializers.ModelSerializer):
    """Serializer for certificates."""
    
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = Certificate
        fields = [
            'id', 'certificate_id', 'student_name', 'course_name',
            'instructor_name', 'completion_date', 'pdf_file',
            'verification_url', 'course', 'created_at'
        ]
        read_only_fields = ['id', 'certificate_id', 'student_name', 'course_name', 'instructor_name', 'completion_date', 'verification_url', 'created_at']
