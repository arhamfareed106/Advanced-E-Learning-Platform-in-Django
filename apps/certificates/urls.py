"""
URL patterns for certificates API.
"""

from django.urls import path
from .views import (
    CertificateListView, CertificateGenerateView,
    CertificateDetailView, CertificateVerifyView
)

app_name = 'certificates'

urlpatterns = [
    path('', CertificateListView.as_view(), name='certificate_list'),
    path('<uuid:pk>/', CertificateDetailView.as_view(), name='certificate_detail'),
    path('generate/<uuid:course_id>/', CertificateGenerateView.as_view(), name='certificate_generate'),
    path('verify/<uuid:certificate_id>/', CertificateVerifyView.as_view(), name='certificate_verify'),
]
