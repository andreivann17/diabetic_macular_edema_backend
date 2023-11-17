import os
from core import settings
def agregando(file_obj, name):
    ruta_destino = os.path.join(settings.MEDIA_ROOT,name)
    with open(ruta_destino, 'wb') as destino:
        destino.write(file_obj.read())

def editando(file_obj, name, ruta_archivo_actual):
    eliminando(ruta_archivo_actual)
    agregando(file_obj,name)

def eliminando(ruta_archivo_actual):
    # Eliminar el archivo actual
    ruta_actual = os.path.join(settings.MEDIA_ROOT, ruta_archivo_actual)
    if os.path.exists(ruta_actual):
        os.remove(ruta_actual)