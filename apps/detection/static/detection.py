import base64
from PIL import Image
from io import BytesIO
import pymysql
import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
connect_info = 'mysql+pymysql://root@localhost:3306/diabetic_macular_edema'
import time
from transformers import ViTImageProcessor, ViTForImageClassification
import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from  .vessels  import prepare_model
from .inception_4_clases import prepare_model_4_clases
from .retinopathy_model import predict_image_retinopathy
import io
import io
import base64
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
connect_info = 'mysql+pymysql://root@localhost:3306/diabetic_macular_edema'
def get_info(id, malignus, startDate, endDate):
    engine = create_engine(connect_info)
    date_txt = ""
    if startDate != "-":
        date_txt = f" AND DATE(d.datetime) between CAST('{startDate}' AS DATE) and  CAST('{endDate}' AS DATE)  "

    if malignus:
        consulta = f"""
        SELECT
    d.id,
    d.datetime,
    d.patient_id,
    d.active,
    CONCAT('/media/detections/', d.id, '.jpg') AS detection_img,
    dis.nombre AS disease_name,
    CONCAT('/media/detection_prediction/', dis.id, '.jpg')  AS disease_img
FROM detections d
INNER JOIN patients p ON p.id = d.patient_id
LEFT JOIN detections_predictions dp ON d.id = dp.detection_id
LEFT JOIN diseases dis ON dp.disease_id = dis.id
        WHERE p.id = '{id}' {date_txt}
        """
        
        df = pd.read_sql_query(sql=consulta, con=engine)

        # Convert epoch milliseconds to datetime
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

        # Format the datetime to a more readable format
        df['datetime'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))

        # Group by the desired columns and aggregate the diseases and images as records
        df_grouped = df.groupby(['id', 'datetime', 'patient_id', 'active', 'detection_img'])[['disease_name', 'disease_img']].apply(lambda x: x.to_dict('records')).reset_index()
        df_grouped.rename(columns={0: 'diseases'}, inplace=True)  # renaming '0' to 'diseases'

        data_json = df_grouped.to_dict(orient='records')
        return data_json

    else:
        # Handle the case where malignus is False.
        consulta = f"""
        SELECT 
            d.id,  
            d.datetime, 
            d.patient_id, 
            d.active, 
            CONCAT('./media/detections/', d.id, '.jpg') AS detection_img
        FROM detections d 
        INNER JOIN patients p ON p.id = d.patient_id 
        WHERE p.id = '{id}' {date_txt}
        """
        
        df = pd.read_sql_query(sql=consulta, con=engine)

        # Convert epoch milliseconds to datetime
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

        # Format the datetime to a more readable format
        df['datetime'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
        
        data_json = df.to_dict(orient='records')
        return data_json

def add(base64_img,user):
    format, imgstr = base64_img.split(';base64,') 
    ext = format.split('/')[-1] 
    data = base64.b64decode(imgstr)
    img = Image.open(BytesIO(data))

    detectionid = ""

    consulta = f'insert into detections ( prediction_details, img, datetime, patient_id, active) VALUES ( "mobilenet", "true", "{time.strftime("%Y-%m-%d H:%M:%S")}", "{1}", 1);'
    conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
    with conexion.cursor() as cursor:  
        cursor.execute(consulta)  
        conexion.commit() 
        detectionid = cursor.lastrowid
        img.save("./media/detections/{}.jpg".format(str(cursor.lastrowid)))
        consulta = f'insert into detections_predictions (detection_id,disease_id,prediction_probability) VALUES ( "{detectionid}","1","0.92");'
      
        conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
        with conexion.cursor() as cursor:  
            cursor.execute(consulta)  
            conexion.commit() 
            result_vessels = get_vessels(str(detectionid))
            prediction = get_prediction_odir_4_clases(str(detectionid))
            info_prediction = get_info_prediction(prediction)
            #return {"vessels":result_vessels,"prediction":prediction}
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue())
            img_base64_str = img_base64.decode('utf-8')  # Convertir a string
            
            # Retornar la imagen en base64
            return {"original": f"data:image/jpeg;base64,{img_base64_str}", "vessels":result_vessels,"prediction":prediction,"description":info_prediction[0],"reference":info_prediction[1]}

def get_info_prediction(prediction):
    engine = create_engine(connect_info)
    consulta = f"SELECT description,reference FROM `diseases`  WHERE name = '{prediction}'"
    df = pd.read_sql_query(sql=consulta, con=engine)
    return [df["description"][0],df["reference"][0]]

def add_mobile(base64_img,url,user):
    format, imgstr = base64_img.split(';base64,') 
    ext = format.split('/')[-1] 
    data = base64.b64decode(imgstr)
    img = Image.open(BytesIO(data))
    img = img.rotate(-90, expand=True)

    detectionid = ""

    consulta = f'insert into detections ( prediction_details, img, datetime, patient_id, active) VALUES ( "mobilenet", "{url}", "{time.strftime("%Y-%m-%d H:%M:%S")}", "{1}", 1);'
    conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
    with conexion.cursor() as cursor:  
        cursor.execute(consulta)  
        conexion.commit() 
        detectionid = cursor.lastrowid
        consulta = f'insert into detections_predictions (detection_id,disease_id,prediction_probability) VALUES ( "{detectionid}","1","0.92");'
        conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
        with conexion.cursor() as cursor:  
            cursor.execute(consulta)  
            conexion.commit() 
            img.save("./media/detections/{}.jpg".format(str(cursor.lastrowid)))
            result = ModelAIObject(str(cursor.lastrowid))
            
            return result
def ModelAIObject(name):

    modelo_directorio = "C:/edema_macular_diabetico/project/models/vit-base-patch16-224"
    url = f"./media/detections/{name}.jpg"
    image = Image.open(url)
    
    # Cargar el procesador y el modelo desde el directorio local
    processor = ViTImageProcessor.from_pretrained(modelo_directorio)
    model = ViTForImageClassification.from_pretrained(modelo_directorio)
    
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    
    # model predicts one of the 1000 ImageNet classes
    predicted_class_idx = logits.argmax(-1).item()
    return {"data":str(model.config.id2label[predicted_class_idx])}
def ModelAI(name):
    base_model = InceptionV3(weights='imagenet', include_top=False)
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    predictions = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)
    
    # Aquí deberías cargar los pesos de tu modelo ya entrenado si los tienes
    # model.load_weights('ruta_a_tus_pesos.h5')
    
    # Cargar y procesar una imagen
    img_width, img_height = 299, 299
    img_path = f"./media/detections/{name}.jpg"
    img = image.load_img(img_path, target_size=(img_width, img_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # Normalización
    
    # Realizar la predicción
    predictions = model.predict(x)
    
    # Puedes imprimir la predicción o procesarla según tus necesidades
    print(predictions)
    return {"data":predictions}


def predict_image_sign(name):
    # Cargar el modelo completo desde el archivo .h5
    model = load_model("C:/edema_macular_diabetico/project/models/modelsign.h5")
    # Cargar y procesar una imagen
    img_path = f"./media/detections/{name}.jpg"
    img = image.load_img(img_path, target_size=(28, 28), color_mode='grayscale')
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # Normalización
    
    # Realizar la predicción
    predictions = model.predict(x)
    predicted_class = np.argmax(predictions)

    predicted_letter = chr(97 + predicted_class)  # 97 es el código ASCII para 'a'
    print(predicted_letter)
    
    return predicted_letter

def get_vessels(name):
    url = f"./media/detections/{name}.jpg"
    img = prepare_model(url, 512)

    # Asumiendo que `prepare_model` devuelve una imagen en formato de array NumPy.
    # Convertir el array NumPy a imagen usando PIL
    pil_img = Image.fromarray((img * 255).astype(np.uint8))

    # Guardar esta imagen en un objeto BytesIO para evitar escribir en el disco
    buffered = io.BytesIO()
    pil_img.save(buffered, format="png")  # Puedes cambiar el formato si lo necesitas

    # Convertir la imagen a base64
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')  # Codificar como UTF-8

    # Crear una cadena base64 que pueda ser usada directamente en HTML o como respuesta JSON
    img_data = f"data:image/png;base64,{img_str}"
    return img_data


def show_image_from_base64(base64_string):
    # Eliminar el prefijo de la cadena base64 si está presente
    if base64_string.startswith('data:image/jpeg;base64,'):
        base64_string = base64_string.replace('data:image/jpeg;base64,', '')
    elif base64_string.startswith('data:image/png;base64,'):
        base64_string = base64_string.replace('data:image/png;base64,', '')

    # Decodificar la imagen desde base64
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))

    # Convertir la imagen PIL a un array NumPy
    image_np = np.array(image)

    # Visualizar la imagen con Matplotlib
    plt.imshow(image_np)
    plt.axis('off')  # Ocultar los ejes
    plt.show()
def get_prediction_retinopathy(name):
    url = f"./media/detections/{name}.jpg"
    prediction = predict_image_retinopathy(url)
    
    return prediction
def get_prediction_odir_4_clases(name):
    url = f"./media/detections/{name}.jpg"
    prediction = prepare_model_4_clases(url)
    
    return prediction

