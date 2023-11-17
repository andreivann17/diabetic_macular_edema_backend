import tensorflow as tf
import numpy as np
import cv2
import segmentation_models as sm
from keras.models import load_model
import matplotlib.pyplot as plt
# Configura el modelo y la función de preprocesamiento
BACKBONE = 'efficientnetb4'
preprocess_input = sm.get_preprocessing(BACKBONE)

# Función para cargar y preprocesar una nueva imagen
def load_and_preprocess_image(image_path, img_size=(512, 512)):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, img_size)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image

# Función para cargar el modelo y realizar predicciones en una nueva imagen
def predict_new_image(model_path, image_path):
    # Carga el modelo
    model = load_model(model_path, compile=False)

    # Carga y preprocesa la imagen
    preprocessed_image = load_and_preprocess_image(image_path)

    # Realiza la predicción
    prediction = model.predict(preprocessed_image)
    return prediction

# Ejemplo de uso
model_path = 'C:/edema_macular_diabetico/project/models/model_disc_optic.h5'  # Ruta al modelo guardado
new_image_path = 'C:/edema_macular_diabetico/project/datasets/IDRiD_17.jpg'  # Ruta a la nueva imagen a predecir



def show_segmentation(original_image_path, predicted_mask):
    # Carga la imagen original
    original_image = cv2.imread(original_image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Asegúrate de que la máscara tiene la forma correcta
    if predicted_mask.ndim == 4:
        predicted_mask = predicted_mask[0, :, :, 0]

    # Escala la máscara predicha al rango [0, 1] si es necesario
    if np.max(predicted_mask) > 1:
        predicted_mask = predicted_mask / 255.0

    # Mostrar la imagen original
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(original_image)
    plt.axis('off')

    # Mostrar la imagen con la máscara de segmentación aplicada
    plt.subplot(1, 2, 2)
    plt.title("Segmented Image")
    plt.imshow(original_image)
    plt.imshow(predicted_mask, cmap='jet', alpha=0.5) # El alpha controla la transparencia
    plt.axis('off')

    plt.show()

# Sigue el mismo proceso para la predicción y luego llama a show_segmentation
predicted_mask = predict_new_image(model_path, new_image_path)
show_segmentation(new_image_path, predicted_mask)

