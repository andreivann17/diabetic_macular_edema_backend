from django.contrib.auth.models import User
from rest_framework import  viewsets,status
from rest_framework.response import Response
from .models import AuthUserExtra
from .serializers import AuthUserExtraSerializer ,UserSerializer

class AuthUserExtraViewSet(viewsets.ModelViewSet):
    queryset = AuthUserExtra.objects.all()
    serializer_class = AuthUserExtraSerializer 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False  
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    