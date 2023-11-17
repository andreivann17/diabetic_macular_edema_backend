import tensorflow as tf
from keras.preprocessing import image
import numpy as np

# 1. Cargar el modelo preentrenado
# Asegúrate de reemplazar 'path_to_your_model.h5' con la ubicación real de tu modelo guardado
#model = tf.keras.models.load_model('C:/edema_macular_diabetico/project/models/model9_7.h5')

def predict_image_retinopathy(img_path):
    # 2. Preprocesar la nueva imagen
    img = image.load_img(img_path, target_size=(512, 512))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalizar la imagen
    img_batch = np.expand_dims(img_array, axis=0)

    # 3. Hacer una predicción
    prediction = model.predict(img_batch)

    # Aquí, devolvemos la clase predicha. Si necesitas las probabilidades en lugar de la clase,
    # puedes retornar `prediction` directamente.
    return np.argmax(prediction, axis=1)[0]




