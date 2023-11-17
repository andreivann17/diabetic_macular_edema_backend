import requests
import os

# Directorio donde deseas guardar los archivos del modelo
directorio_destino = "vit-base-patch16-224"

# Asegurarse de que el directorio existe
if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

# Lista de URLs de los archivos del modelo
urls = [
    "https://huggingface.co/google/vit-base-patch16-224/resolve/main/config.json",
    "https://huggingface.co/google/vit-base-patch16-224/resolve/main/pytorch_model.bin",
    # Puedes agregar más URLs aquí si el modelo tiene otros archivos.
]

for url in urls:
    response = requests.get(url)
    filename = os.path.join(directorio_destino, url.split("/")[-1])
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Descargado {filename}")

print("¡Descarga completada!")

