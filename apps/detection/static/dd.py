import tensorflow as tf
from keras.preprocessing import image
import numpy as np

# 1. Cargar el modelo preentrenado
# Asegúrate de reemplazar 'path_to_your_model.h5' con la ubicación real de tu modelo guardado
model = tf.keras.models.load_model('C:/edema_macular_diabetico/project/models/model9_7.h5')