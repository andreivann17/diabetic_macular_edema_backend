from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.patients.views import PatientViewSet, PatientDashboardViewSet,PatientMalignusViewSet

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('me/', PatientViewSet.as_view()),
    path('dashboard/me/<str:startDate>/<str:endDate>', PatientDashboardViewSet.as_view()),
    path('malignus/me/', PatientMalignusViewSet.as_view()),
]
 