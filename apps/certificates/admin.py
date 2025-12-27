"""
Admin configuration for certificates app.
"""

from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_id', 'student_name', 'course_name', 'completion_date', 'created_at']
    list_filter = ['completion_date', 'created_at']
    search_fields = ['certificate_id', 'student_name', 'course_name', 'student__username']
    readonly_fields = ['certificate_id', 'student_name', 'course_name', 'instructor_name', 'completion_date', 'verification_url', 'created_at']
