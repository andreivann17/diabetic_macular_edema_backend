from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Patient, BloodType, Gender
from .serializers import PatientSerializer, BloodTypeSerializer, GenderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .static import dashboard
from rest_framework import generics
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .static import patients
from ..detection.static import detection
class GenderViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

class BloodTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BloodType.objects.all()
    serializer_class = BloodTypeSerializer


class PatientViewSet(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        return Response(patients.get_info(request.user.id),status=status.HTTP_200_OK)

    def post(self, request):
        patients.add(request.data.get("data"),request.data.get("img"),request.user.id)
        return Response({"msj":"correcto" },status=status.HTTP_200_OK)
    
    def patch(self, request):
        patients.edit(request.data.get("data"),request.data.get("img"),request.user.id)
        return Response({"msj":"correcto" },status=status.HTTP_200_OK)


class PatientDashboardViewSet(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, startDate,endDate):
        data = dashboard.dashboard(request.user.id, startDate,endDate)  
     
        return Response(data, status=status.HTTP_200_OK)
class PatientMalignusViewSet(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        data = detection.get_info(request.user.id,True,"-","-")  
     
        return Response(data, status=status.HTTP_200_OK)
