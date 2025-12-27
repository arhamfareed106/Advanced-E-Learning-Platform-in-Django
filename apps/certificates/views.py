"""
Views for certificates app.
"""

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Certificate
from apps.enrollment.models import Enrollment
from apps.quizzes.models import Quiz, Attempt
from .serializers import CertificateSerializer
from .services import generate_certificate_pdf
from apps.users.permissions import IsStudent


class CertificateListView(generics.ListAPIView):
    """List all certificates for the current user."""
    
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user).select_related('course')


class CertificateGenerateView(views.APIView):
    """Generate certificate for a completed course."""
    
    permission_classes = [IsAuthenticated, IsStudent]
    
    def post(self, request, course_id):
        # Check if enrollment exists and is completed
        try:
            enrollment = Enrollment.objects.get(
                student=request.user,
                course_id=course_id,
                is_completed=True
            )
        except Enrollment.DoesNotExist:
            return Response({
                'error': 'You must complete all lessons before generating a certificate.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if final quiz is passed (if exists)
        final_quiz = Quiz.objects.filter(
            course_id=course_id,
            is_final_quiz=True
        ).first()
        
        if final_quiz:
            passed_attempt = Attempt.objects.filter(
                student=request.user,
                quiz=final_quiz,
                passed=True
            ).exists()
            
            if not passed_attempt:
                return Response({
                    'error': 'You must pass the final quiz before generating a certificate.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if certificate already exists
        certificate, created = Certificate.objects.get_or_create(
            student=request.user,
            course=enrollment.course
        )
        
        if created or not certificate.pdf_file:
            # Generate PDF
            pdf_content = generate_certificate_pdf(certificate)
            certificate.pdf_file.save(
                f'certificate_{certificate.certificate_id}.pdf',
                pdf_content,
                save=True
            )
            
            # Set verification URL
            certificate.verification_url = f"{settings.FRONTEND_URL}/certificates/verify/{certificate.id}/"
            certificate.save()
        
        return Response(
            CertificateSerializer(certificate).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class CertificateDetailView(generics.RetrieveAPIView):
    """Get certificate details."""
    
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_student:
            return Certificate.objects.filter(student=self.request.user)
        return Certificate.objects.all()


class CertificateVerifyView(views.APIView):
    """Public endpoint to verify certificate authenticity."""
    
    permission_classes = [AllowAny]
    
    def get(self, request, certificate_id):
        try:
            certificate = Certificate.objects.get(id=certificate_id)
            return Response({
                'valid': True,
                'certificate_id': certificate.certificate_id,
                'student_name': certificate.student_name,
                'course_name': certificate.course_name,
                'instructor_name': certificate.instructor_name,
                'completion_date': certificate.completion_date,
            })
        except Certificate.DoesNotExist:
            return Response({
                'valid': False,
                'error': 'Certificate not found.'
            }, status=status.HTTP_404_NOT_FOUND)
