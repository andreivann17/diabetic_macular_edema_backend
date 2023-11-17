from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.history.views import HistoryViewSet

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('me/', HistoryViewSet.as_view()),
]
 