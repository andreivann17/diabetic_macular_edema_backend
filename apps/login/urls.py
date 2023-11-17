from django.urls import path
from .views import  Codigo,Correo,Login,NewPassword
urlpatterns = [
    path('codigo/', Codigo.as_view()),
    path('correo/', Correo.as_view()),
    path('', Login.as_view()),
    path('new-password/', NewPassword.as_view()),
]