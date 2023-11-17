
import numpy as np
import cv2
import math
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf

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
def print_pred(array_of_classes):
    xx = array_of_classes
    s1,s2 = xx.shape
    for i in range(s1):
        for j in range(s2):
            print('%.3f ' % xx[i,j],end='')
        print('')
def show_Nimages(imgs,scale=1):

    N=len(imgs)
    fig = plt.figure(figsize=(25/scale, 16/scale))
    for i, img in enumerate(imgs):
        ax = fig.add_subplot(1, N, i + 1, xticks=[], yticks=[])
        show_image(img)
# 3. Generar y visualizar el mapa de calor
def gen_heatmap_img(img, model0, layer_name='last_conv_layer', viz_img=None, orig_img=None):
    # Convertir la imagen a un tensor y asegurarse de que se esté observando para calcular gradientes
    img_tensor = tf.convert_to_tensor(img, dtype=tf.float32)
    
    viz_layer = model0.get_layer(layer_name)
    
    with tf.GradientTape() as tape:
        tape.watch(img_tensor)
        
        # Establecer el modelo en modo de entrenamiento
        model0.trainable = True
        for layer in model0.layers:
            layer.trainable = True
        
        # Obtener las predicciones hasta la capa de interés
        intermediate_output = viz_layer(img_tensor[tf.newaxis, ...])
        
        # Obtener la predicción final
        preds_raw = model0(img_tensor[tf.newaxis, ...])
        class_idx = tf.argmax(preds_raw[0])
        class_channel = preds_raw[:, class_idx]
    
    # Obtener los gradientes con respecto a la salida intermedia
    grads = tape.gradient(class_channel, intermediate_output)
    
    # ... (resto de tu código)



    
    pooled_grads = tf.keras.backend.mean(grads, axis=(0,1,2))
    iterate = tf.keras.backend.function([model0.input], [pooled_grads, viz_layer.output[0]])
    pooled_grad_value, viz_layer_out_value = iterate([img[np.newaxis]])
    
    for i in range(pooled_grad_value.shape[0]):
        viz_layer_out_value[:,:,i] *= pooled_grad_value[i]
    
    heatmap = np.mean(viz_layer_out_value, axis=-1)
    heatmap = np.maximum(heatmap,0)
    heatmap /= np.max(heatmap)

    viz_img = cv2.resize(viz_img, (img.shape[1], img.shape[0]))
    heatmap = cv2.resize(heatmap, (viz_img.shape[1], viz_img.shape[0]))
    heatmap_color = cv2.applyColorMap(np.uint8(heatmap*255), cv2.COLORMAP_SPRING)/255
    heated_img = heatmap_color*0.5 + viz_img*0.5
    
    print('raw output from model : ')
    print_pred(preds_raw)
    
    if orig_img is None:
        show_Nimages([img, viz_img, heatmap_color, heated_img])
    else:
        show_Nimages([orig_img, img, viz_img, heatmap_color, heated_img])
    
    plt.show()
    return heated_img
def preprocess_image(image_path, desired_size=224):
    im = Image.open(image_path)
    im = im.resize((desired_size, )*2, resample=Image.LANCZOS)
    return np.array(im)


def transform_image_ben(img):  
    image = cv2.addWeighted(img, 4, cv2.GaussianBlur(img, (0,0), 10), -4, 128)
    return image/255

from albumentations import *
import time

IMG_SIZE = (224,224)

'''Use case from https://www.kaggle.com/alexanderliao/image-augmentation-demo-with-albumentation/'''
def albaugment(aug0, img):
    return aug0(image=img)['image']
idx=8
path = 'C:/edema_macular_diabetico/project/datasets/eye-tracking-code/ODIR-5K/ODIR-5K/myodir-crop/5_left.jpg'
image1 = preprocess_image(path)

'''1. Rotate or Flip'''
aug1 = OneOf([
    Rotate(p=0.99, limit=160, border_mode=0,value=0), # value=black
    Flip(p=0.5)
    ],p=1)

'''2. Adjust Brightness or Contrast'''
aug2 = RandomBrightnessContrast(brightness_limit=0.45, contrast_limit=0.45,p=1)
h_min=np.round(IMG_SIZE[1]*0.72).astype(int)
h_max= np.round(IMG_SIZE[1]*0.9).astype(int)
print(h_min,h_max)

'''3. Random Crop and then Resize'''
#w2h_ratio = aspect ratio of cropping
aug3 = RandomSizedCrop((h_min, h_max),IMG_SIZE[1],IMG_SIZE[0], w2h_ratio=IMG_SIZE[0]/IMG_SIZE[1],p=1)

'''4. CutOut Augmentation'''
max_hole_size = int(IMG_SIZE[1]/10)
aug4 = Cutout(p=1,max_h_size=max_hole_size,max_w_size=max_hole_size,num_holes=8 )#default num_holes=8

'''5. SunFlare Augmentation'''
aug5 = RandomSunFlare(src_radius=max_hole_size,
                      num_flare_circles_lower=10,
                      num_flare_circles_upper=20,
                      p=1)#default flare_roi=(0,0,1,0.5),

'''6. Ultimate Augmentation -- combine everything'''
final_aug = Compose([
    aug1,aug2,aug3,aug4,aug5
],p=1)


img1 = albaugment(aug1,image1)
img2 = albaugment(aug1,image1)
print('Rotate or Flip')
show_Nimages([image1,img1,img2],scale=2)
# time.sleep(1)

img1 = albaugment(aug2,image1)
img2 = albaugment(aug2,image1)
img3 = albaugment(aug2,image1)
print('Brightness or Contrast')
show_Nimages([img3,img1,img2],scale=2)
# time.sleep(1)

img1 = albaugment(aug3,image1)
img2 = albaugment(aug3,image1)
img3 = albaugment(aug3,image1)
print('Rotate and Resize')
show_Nimages([img3,img1,img2],scale=2)
print(img1.shape,img2.shape)
# time.sleep(1)

img1 = albaugment(aug4,image1)
img2 = albaugment(aug4,image1)
img3 = albaugment(aug4,image1)
print('CutOut')
show_Nimages([img3,img1,img2],scale=2)
# time.sleep(1)

img1 = albaugment(aug5,image1)
img2 = albaugment(aug5,image1)
img3 = albaugment(aug5,image1)
print('Sun Flare')
show_Nimages([img3,img1,img2],scale=2)
# time.sleep(1)

img1 = albaugment(final_aug,image1)
img2 = albaugment(final_aug,image1)
img3 = albaugment(final_aug,image1)
print('All above combined')
show_Nimages([img3,img1,img2],scale=2)
print(img1.shape,img2.shape)




model = tf.keras.models.load_model('C:/edema_macular_diabetico/project/models/heatmap.h5')
aug_list = [aug5, aug2, aug3, aug4, aug1, final_aug]
aug_name = ['SunFlare', 'brightness or contrast', 'crop and resized', 'CutOut', 'rotate or flip', 'Everything Combined']

idx=8
layer_name = 'relu' #'conv5_block16_concat'
for i in range(len(aug_list)):
    path='C:/edema_macular_diabetico/project/datasets/eye-tracking-code/ODIR-5K/ODIR-5K/myodir-crop/5_left.jpg'
    input_img = np.empty((1,224, 224, 3), dtype=np.uint8)
    input_img[0,:,:,:] = preprocess_image(path)
    aug_img = albaugment(aug_list[i],input_img[0,:,:,:])
    ben_img = transform_image_ben(aug_img)
    
    print('test pic no.%d -- augmentation: %s' % (i+1, aug_name[i]))
    _ = gen_heatmap_img(aug_img,
                        model, layer_name=layer_name,viz_img=ben_img,orig_img=input_img[0])
    
