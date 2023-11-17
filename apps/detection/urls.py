from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.detection.views import DetectionsViewSet


urlpatterns = [
    path('me/<str:startDate>/<str:endDate>', DetectionsViewSet.as_view()),
    path('me/', DetectionsViewSet.as_view()),
]
