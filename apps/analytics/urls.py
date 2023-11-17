from django.urls import path
from apps.analytics.views import AnalyticsViewSet

urlpatterns = [
    path('<str:startDate>/<str:endDate>', AnalyticsViewSet.as_view()),
]
 