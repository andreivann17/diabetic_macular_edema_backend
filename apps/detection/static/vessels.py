import tensorflow as tf
import numpy as np
import tensorflow_io as tfio
import keras
from keras.layers import Dropout

def predict_image(model, image_path, img_size):
    img = read_files(image_path, img_size)
    img = tf.expand_dims(img, axis=0)
    mask_pred = model.predict(img)
    mask_pred = (mask_pred > 0.5).astype(np.uint8)  # Esto producirá una imagen binaria (blanco y negro)
    return mask_pred[0, :, :, 0]
def read_files(image_path,img_size, mask=False):
    image = tf.io.read_file(image_path)
    
    if mask:
        image = tf.io.decode_gif(image)
        image = tf.squeeze(image)
        image = tf.image.rgb_to_grayscale(image)
        image = tf.divide(image, 128)
        image.set_shape([None, None, 1])
        image = tf.image.resize(images=image, size=[img_size, img_size])
        image = tf.cast(image, tf.int32)
    else:
        try:
            image = tfio.experimental.image.decode_tiff(image)
        except:
            image = tf.image.decode_image(image)
        image = image[:,:,:3]
        image.set_shape([None, None, 3])
        image = tf.image.resize(images=image, size=[img_size, img_size])
        image = image / 255.

    return image

def prepare_model(new_image_path,img_size):
    loaded_model = keras.models.load_model('C:/edema_macular_diabetico/project/models/modelvessels.h5', custom_objects={'FixedDropout': Dropout})
    predicted_mask = predict_image(loaded_model, new_image_path,img_size)
    return predicted_mask

