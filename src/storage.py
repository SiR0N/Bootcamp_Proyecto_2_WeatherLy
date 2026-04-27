import json  # Librería para trabajar con archivos JSON
import os    # Librería para trabajar con archivos y rutas del sistema

# Ruta donde está el archivo JSON
FILE_PATH = "data/weather.json"


def load_data():   #Función para leer el histórico guardado en el archivo JSON
    # Comprobar si el archivo NO existe
    if not os.path.exists(FILE_PATH):
        # Si no existe, devolvemos una lista vacía, sin romper el programa
        return []

    try:
        # Abrimos el archivo en modo lectura
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            # Cargamos el contenido del JSON y lo convertimos a un objeto de Python
            data = json.load(file)

        # Comprobamos que lo que hemos leído es una lista
        if isinstance(data, list):
            # Si es lista, la devolvemos
            return data

        # Si no es lista, devolvemos lista vacía (evitamos errores)
        return []

    except (json.JSONDecodeError, FileNotFoundError):
        # Si el JSON está mal formado o hay algún error al leerlo
        # devolvemos una lista vacía para no romper el programa
        return []

  
 
    
