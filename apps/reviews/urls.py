"""
URL patterns for reviews API.
"""

from django.urls import path
from .views import (
    ReviewListView, ReviewCreateView,
    ReviewUpdateView, ReviewDeleteView
)

app_name = 'reviews'

urlpatterns = [
    path('', ReviewListView.as_view(), name='review_list'),
    path('create/', ReviewCreateView.as_view(), name='review_create'),
    path('<uuid:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('<uuid:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]
