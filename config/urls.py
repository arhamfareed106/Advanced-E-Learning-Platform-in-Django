"""
URL configuration for elearning_platform project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Landing page
    path('', TemplateView.as_view(template_name='landing/index.html'), name='home'),
    
    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/enrollment/', include('apps.enrollment.urls')),
    path('api/quizzes/', include('apps.quizzes.urls')),
    path('api/certificates/', include('apps.certificates.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    
    # Allauth URLs
    path('accounts/', include('allauth.urls')),
    
    # Template views
    path('auth/', include('apps.users.template_urls')),
    path('courses/', include('apps.courses.template_urls')),
    path('student/', include('apps.enrollment.template_urls')),
    # path('instructor/', include('apps.courses.instructor_urls')),
    # path('certificates/', include('apps.certificates.template_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

# Custom admin site headers
admin.site.site_header = "E-Learning Platform Administration"
admin.site.site_title = "E-Learning Admin"
admin.site.index_title = "Welcome to E-Learning Platform Admin"
