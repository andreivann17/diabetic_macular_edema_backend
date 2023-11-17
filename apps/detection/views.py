from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .static import detection
import json

    
class DetectionsViewSet(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    def get(self, request, startDate,endDate):
        data = detection.get_info(request.user.id,True, startDate,endDate)
        return Response(data,status=status.HTTP_200_OK)

    def post(self, request):
        imgs = request.data.get("images")
    
        # Si imgs es un string, intenta convertirlo a un diccionario
        if isinstance(imgs, str):
            try:
                imgs = json.loads(imgs)
            except json.JSONDecodeError:
                return Response({"error": "Invalid image data format"}, status=status.HTTP_400_BAD_REQUEST)
    
        if imgs is not None:
            if "web" == request.data.get("type"):
                results = []
                for img_key, img_data in imgs.items():
                    result = detection.add(img_data, request.user.id)
                    results.append(result)
                return Response(results, status=status.HTTP_200_OK)
            else:
                result = detection.add_mobile(request.data.get("img"), request.user.id)
                return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No image found"}, status=status.HTTP_400_BAD_REQUEST)
