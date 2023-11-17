from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .static import dicom

class DicomViewSet(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, id_patient):
        dicom_image = dicom.get(id_patient)
        return Response({"data": dicom_image}, status=status.HTTP_200_OK)

    def post(self, request):
        id_patient = request.data.get("id_patient")
        patient_name = request.data.get("patient_name")
        patient_id = request.data.get("patient_id")

        if not all([id_patient, patient_name, patient_id]):
            return Response({"msj": "Falta uno o más parámetros requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        dicom_image = dicom.create(id_patient, patient_name, patient_id)

        # Convierte el archivo DICOM en base64 para enviarlo en la respuesta
        dicom_image_base64 = dicom.dicom_to_base64(dicom_image)
        
        return Response({"msj": "correcto", "dcm": dicom_image_base64 },status=status.HTTP_200_OK)
