from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status 
from channels.layers import get_channel_layer
from ..utils import  address
channel_layer = get_channel_layer()
from ipware import get_client_ip
#from ..registros.static  import registros
from django.contrib.auth import authenticate
class Login(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        client_ip, is_routable = get_client_ip(request)
        # Usar authenticate para verificar las credenciales
        user = authenticate(request, username=request.data.get("username"), password= request.data.get("password"))
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            # El nombre de usuario y la contraseña son correctos
            request.session['0'] = user.id
            #registros.agregando("66", client_ip, user.id, user.id)
            data = {"status": "1", "value":  token.key}
        else:
            # El nombre de usuario o la contraseña son incorrectos
            data = {"status": "0", "value": "Invalid credentials"}

        return Response({
            "data": data
        }, status=status.HTTP_200_OK)
class Correo(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        data = address.comprobar_correo(request.data.get("correo"))
        return Response({"data": data},status=status.HTTP_200_OK)
class Codigo(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        data = address.comprobarcode(request.data.get("code"),request.data.get("clave"))
        return Response({"data": data},status=status.HTTP_200_OK)
class NewPassword(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        clave = request.data.get("clave")
        nueva_contraseña = request.data.get("pass")

        # Autenticar al usuario
        print(clave)
        #tengo que traerme el password de la contrasena viejita
        user = authenticate(request, password=request.data.get("clave"))

        if user is not None:
            # Cambiar la contraseña
            user.set_password(request.data.get("pass"))
            user.save()
            data = {"status": "1", "message": "Password changed successfully"}
        else:
            data = {"status": "0", "message": "Invalid credentials"}
        print(data)
        return Response({"data": data}, status=status.HTTP_200_OK)
