# 1. Cargar la nueva imagen
import numpy as np
import cv2
import math
from PIL import Image
import matplotlib.pyplot as plt
import keras.backend as K
import keras
import tensorflow as tf
new_image_path = 'C:/edema_macular_diabetico/project/datasets/eye-tracking-code/ODIR-5K/ODIR-5K/myodir-crop/5_left.jpg' # Aquí, reemplaza 'path_to_your_new_image.jpg' con la ruta a tu imagen.
def get_pad_width(im, new_shape, is_rgb=True):
    pad_diff = new_shape - im.shape[0], new_shape - im.shape[1]
    t, b = math.floor(pad_diff[0]/2), math.ceil(pad_diff[0]/2)
    l, r = math.floor(pad_diff[1]/2), math.ceil(pad_diff[1]/2)
    if is_rgb:
        pad_width = ((t,b), (l,r), (0, 0))
    else:
        pad_width = ((t,b), (l,r))
    return pad_width
def print_pred(array_of_classes):
    xx = array_of_classes
    s1,s2 = xx.shape
    for i in range(s1):
        for j in range(s2):
            print('%.3f ' % xx[i,j],end='')
        print('')
def show_image(image,figsize=None,title=None):
    
    if figsize is not None:
        fig = plt.figure(figsize=figsize)
#     else: # crash!!
#         fig = plt.figure()
        
    if image.ndim == 2:
        plt.imshow(image,cmap='gray')
    else:
        plt.imshow(image)
        
    if title is not None:
        plt.title(title)
def show_Nimages(imgs,scale=1):

    N=len(imgs)
    fig = plt.figure(figsize=(25/scale, 16/scale))
    for i, img in enumerate(imgs):
        ax = fig.add_subplot(1, N, i + 1, xticks=[], yticks=[])
        show_image(img)
def preprocess_image(image_path, desired_size=224):
    im = Image.open(image_path)
    im = im.resize((desired_size, )*2, resample=Image.LANCZOS)
#     im = im.resize((desired_size, )*2)
    
    return im

def transform_image_ben(img,resize=True,crop=False,norm255=True,keras=False):  
    image=cv2.addWeighted( img,4, cv2.GaussianBlur( img , (0,0) ,  10) ,-4 ,128)
    
    # NOTE plt.imshow can accept both int (0-255) or float (0-1), but deep net requires (0-1)
    if norm255:
        return image/255
    elif keras:
        image = np.expand_dims(image, axis=0)
        return preprocess_image(image)[0]
    else:
        return image.astype(np.int16)
    
    return image
def gen_heatmap_img(img, model0, layer_name='last_conv_layer', viz_img=None, orig_img=None):
    with tf.GradientTape() as tape:
        # Asegurarse de que la imagen se esté observando para calcular gradientes
        img_tensor = tf.convert_to_tensor(img, dtype=tf.float32)
        tape.watch(img_tensor)
        preds_raw = model0(img[np.newaxis])
        class_idx = (preds_raw > 0.5).numpy().astype(int).sum(axis=1) - 1
        class_output_tensor = model0.output



    
    viz_layer = model0.get_layer(layer_name)
    grads = tape.gradient(class_output_tensor, viz_layer.output)
    
    
    pooled_grads=K.mean(grads,axis=(0,1,2))
    iterate=K.function([model0.input],[pooled_grads, viz_layer.output[0]])
    
    pooled_grad_value, viz_layer_out_value = iterate([img[np.newaxis]])
    
    for i in range(pooled_grad_value.shape[0]):
        viz_layer_out_value[:,:,i] *= pooled_grad_value[i]
    
    heatmap = np.mean(viz_layer_out_value, axis=-1)
    heatmap = np.maximum(heatmap,0)
    heatmap /= np.max(heatmap)

    viz_img=cv2.resize(viz_img,(img.shape[1],img.shape[0]))
    heatmap=cv2.resize(heatmap,(viz_img.shape[1],viz_img.shape[0]))
    
    heatmap_color = cv2.applyColorMap(np.uint8(heatmap*255), cv2.COLORMAP_SPRING)/255
    heated_img = heatmap_color*0.5 + viz_img*0.5
    
    print('raw output from model : ')
    print_pred(preds_raw)
    
    if orig_img is None:
        show_Nimages([img,viz_img,heatmap_color,heated_img])
    else:
        show_Nimages([orig_img,img,viz_img,heatmap_color,heated_img])
    
    plt.show()
    return heated_img
new_image = preprocess_image(new_image_path)

# 2. Preprocesar la imagen

input_img = np.empty((1, 224, 224, 3), dtype=np.uint8)
input_img[0, :, :, :] = new_image

from keras.layers import Dropout

model = keras.models.load_model('C:/edema_macular_diabetico/project/models/heatmap.h5', custom_objects={'FixedDropout': Dropout})
pred = model.predict(input_img)
print("Raw prediction:", pred)

# 4. Generar y visualizar el mapa de calor

# (Nota: la función `gen_heatmap_img` ya está definida en el código que proporcionaste)
layer_name = 'relu' 
ben_img = transform_image_ben(input_img[0])
_ = gen_heatmap_img(input_img[0], model, layer_name=layer_name, viz_img=ben_img, orig_img=input_img[0])
