import base64
from PIL import Image
from io import BytesIO
import pymysql
import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
connect_info = 'mysql+pymysql://root@localhost:3306/diabetic_macular_edema'
 #use sqlalchemy to build link-engine
import time
import json
from datetime import datetime
def get_info(id):
    engine = create_engine(connect_info)
    consulta = f"SELECT p.id, p.first_name, p.last_name,p.gender_id,p.blood_type_id,p.birth_date, p.user_id,p.created_at,p.updated_at, p.active, CONCAT('./media/patients/', p.id, '.jpg') AS img,g.name as gender_name,b.type as blood_type_name,a.email FROM `patients`  p inner join gender g on g.id = p.gender_id inner join blood_type b on b.id = p.blood_type_id inner join auth_user a on a.id = p.user_id WHERE p.user_id = '{id}'"
    df = pd.read_sql_query(sql=consulta, con=engine)

    # Convert epoch milliseconds to datetime
    df['created_at'] = pd.to_datetime(df['created_at'], unit='ms')

    # Format the datetime to a more readable format
    df['created_at'] = df['created_at'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['updated_at'] = pd.to_datetime(df['updated_at'], unit='ms')

    # Format the datetime to a more readable format
    df['updated_at'] = df['updated_at'].apply(lambda x: x.strftime('%Y-%m-%d'))

    data_json = df.to_dict(orient='records')
    return data_json[0]
def add(data,base64_img,user):
    img = ""
    imgResponse = False
    if base64_img:
        imgResponse= True
    now = datetime.now().isoformat()
    consulta = f'insert into patients (first_name,last_name, gender_id, blood_type_id,birth_date,created_at,updated_at, user_id,img,active) VALUES ("{data["first_name"]}","{data["last_name"]}",  "{data["gender_id"]}","{data["blood_type_id"]}","{data["birth_date"]}","{now}","{now}","{user}", "{imgResponse}", 1);'
    conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
    with conexion.cursor() as cursor:  
        cursor.execute(consulta)  
        conexion.commit() 
        if imgResponse:
            format, imgstr = base64_img.split(';base64,') 
            data = base64.b64decode(imgstr)
            img = Image.open(BytesIO(data))
            img.save("./media/patients/{}.jpg".format(str(cursor.lastrowid)))
def edit(data, base64_img, user):
    engine = create_engine(connect_info)
    imgResponse = False
    img_update_sql = ""
    df  = pd.read_sql_query(sql=f"select id from patients where user_id = '{user}'", con=engine)
    patient_id = df["id"][0]
    if base64_img:
        imgResponse = True
        format, imgstr = base64_img.split(';base64,') 
        data_img = base64.b64decode(imgstr)
        img = Image.open(BytesIO(data_img))
        img.save("./media/patients/{}.jpg".format(str(patient_id)))
        img_update_sql = ', img="{}"'.format(imgResponse)

    now = datetime.now().isoformat()
    consulta = f'UPDATE patients SET first_name="{data["first_name"]}", last_name="{data["last_name"]}", gender_id="{data["gender_id"]}", blood_type_id="{data["blood_type_id"]}", birth_date="{data["birth_date"]}", updated_at="{now}", user_id="{user}" {img_update_sql} WHERE id={patient_id};'
    conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
    with conexion.cursor() as cursor:  
        cursor.execute(consulta)  
        conexion.commit() 

