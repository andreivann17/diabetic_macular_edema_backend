from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .static import history


class HistoryViewSet(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        return Response(history.get_info(request.user.id),status=status.HTTP_200_OK)

    def post(self, request):
        history.add(request.data.get("data"),request.user.id)
        return Response({"msj":"correcto" },status=status.HTTP_200_OK)
    
 

