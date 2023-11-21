from keras.models import load_model
import numpy as np
import cv2
import segmentation_models as sm
from segmentation_models.metrics import IOUScore, FScore
from PIL import Image
import io
import base64

sm.set_framework('tf.keras')

def convert_to_base64(image):
    # Convertir la imagen a un objeto de bytes en formato PNG
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    # Decodificar para obtener una cadena en base64
    return img_str.decode('utf-8')

def predecir_nueva_imagen(ruta_imagen, img_size):
    model  = load_model('C:/edema_macular_diabetico/project/models/model_microaneurisms.h5')
    img = cv2.imread(ruta_imagen)
    img = cv2.resize(img, (img_size, img_size))  # Asegúrate que este tamaño coincida con el esperado por tu modelo
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    return pred[0]

def prepare_model_microaneurism(new_image_path, img_size):
    predicted_mask = predecir_nueva_imagen(new_image_path, img_size)

    # Asegúrate de que la máscara sea 2D si es necesario
    if predicted_mask.ndim == 3 and predicted_mask.shape[-1] == 1:
        predicted_mask = predicted_mask.reshape(predicted_mask.shape[0], predicted_mask.shape[1])

    # Asegúrate de que los valores estén en el rango de 0 a 255 y sean enteros
    predicted_mask = (predicted_mask * 255).astype('uint8')

    # Convertir la máscara en una imagen PIL
    mask_image = Image.fromarray(predicted_mask)

    # Convertir a base64
    base64_str = convert_to_base64(mask_image)
    return base64_str
