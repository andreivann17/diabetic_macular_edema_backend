import smtplib
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import random
connect_info = 'mysql+pymysql://root@localhost:3306/diabetic_macular_edema'
from django.contrib.auth.models import User


def send_address(correo,token):
    message = """
Saludos de su equipo de Osmed,

Hemos recibido una solicitud para restablecer la contraseña de la cuenta  asociada a esta dirección de correo electrónico. Copie el código y utilícelo en la aplicación:

""" + str(token)+ """

Si no solicitó el restablecimiento de su contraseña, puede hacer caso omiso de este mensaje de correo electrónico. 

Tenga la tranquilidad de que su cuenta de Osmed es segura.

Osmed nunca le enviará un correo electrónico para pedirle que revele o verifique su contraseña, tarjeta de crédito o número de cuenta bancaria. 

Si recibe algún correo electrónico sospechoso que contenga un enlace para actualizar la información de su cuenta, no haga clic en él. Sin embargo, no deje de informar de dicho correo electrónico a Osmed para que se investigue.
Para obtener ayuda y asistencia, visite el Centro de Support en https:/DonSimonrestaurante.com/support

Gracias por usar Osmed RRHH.

Atentamente,
El equipo  del departamento de innovacion y desarrollo de Osmed
    """
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    smtp_obj.login('andreivann17@gmail.com', 'p h y z l t x e s j s j r s a d')
    smtp_obj.sendmail('andreivann17@gmail.com', correo, message.encode('utf-8'))
    smtp_obj.quit()
def generate_token(length=10):
    """Genera un token aleatorio de números de la longitud especificada"""
    return ''.join(random.choices('0123456789', k=length))
def comprobarcode(code,id):
    engine = create_engine(connect_info) 
    consulta = "SELECT user_id from auth_user_extra  where code = '"+str(code)+"' and user_id='"+str(id)+"'"
    df = pd.read_sql_query(sql=consulta, con=engine)
    if len(df)>0:
        return {"status":True}
    
    return {"status":False}
def establecercode(id):
    token = generate_token()
    conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
    with conexion.cursor() as cursor:
        consulta = "UPDATE auth_user_extra SET code  = '"+str(token)+"' where user_id='"+str(id)+"'"
        cursor.execute(consulta)
        conexion.commit()
    return token

def comprobar_correo(correo):
    usuario_existe = User.objects.filter(email=correo).exists()

    if usuario_existe:
        usuario = User.objects.get(email=correo)
        token = establecercode(usuario.id)
        send_address(correo, token)
        return {"status": True, "clave": usuario.id}

    return {"status": False}