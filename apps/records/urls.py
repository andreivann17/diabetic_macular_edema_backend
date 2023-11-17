from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.detection.views import DetectionsViewSet


urlpatterns = [
    path('', DetectionsViewSet.as_view()),
]
