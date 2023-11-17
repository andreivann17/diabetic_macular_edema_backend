from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image

# Directorio donde guardaste el modelo y el procesador
modelo_directorio = "C:/edema_macular_diabetico/project/models/vit-base-patch16-224"
url = f"C:/edema_macular_diabetico/project/backend/media/detections/12.jpg"
image = Image.open(url)

# Cargar el procesador y el modelo desde el directorio local
processor = ViTImageProcessor.from_pretrained(modelo_directorio)
model = ViTForImageClassification.from_pretrained(modelo_directorio)

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits

# model predicts one of the 1000 ImageNet classes
predicted_class_idx = logits.argmax(-1).item()

print( "Predicted class: " + str(model.config.id2label[predicted_class_idx]))