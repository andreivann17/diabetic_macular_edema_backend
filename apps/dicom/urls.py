from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.dicom.views import DicomViewSet


urlpatterns = [
    path('', DicomViewSet.as_view()),
]
