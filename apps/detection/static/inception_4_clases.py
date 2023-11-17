import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
"""
clases


0: mild nonproliferative retinopathy
1: cataract
2: pathological myopia
3: wet age-related macular degeneration
"""
names = ["mild nonproliferative retinopathy","cataract","pathological myopia","wet age-related macular degeneration"]
def load_and_prepare_image(file_path, image_size=224):
    img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (image_size, image_size))
    img = img / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    return img


def prepare_model_4_clases(image_path):
    model_path = 'C:/edema_macular_diabetico/project/models/modelInception4clases.h5' 
    model = load_model(model_path)
    prepared_image = load_and_prepare_image(image_path)
    prediction = model.predict(prepared_image)
    predicted_class = np.argmax(prediction, axis=1)
    print(predicted_class[0])
    return names[predicted_class[0]]

    
